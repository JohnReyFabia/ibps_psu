import os
import joblib
from django.utils import timezone
import pytz
from django import forms
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from .models import (
    Student,
    StudentSurveyQuestion,
    SurveyQuestion,
    SurveyQuestionChoice,
    Assessment,
    CriticalBoundary,
    StudentAssessmentHistory,
    BurnoutProfile,
)
# utils functions
from .utils import create_critical_boundaries

# PREPROCESSING THE ASSESSMENT COMPUTATION RESULT BEFORE PASSING TO PREDICTION MODEL
def preprocess_data(ex_high, cy_high, ef_high):
    # Convert boolean values to numerical format (1 for True, 0 for False)
    ex_high_numeric = 1 if ex_high else 0
    cy_high_numeric = 1 if cy_high else 0
    ef_high_numeric = 1 if ef_high else 0

    # Arrange the preprocessed values into a structured input (list or array)
    processed_data = [[ex_high_numeric, cy_high_numeric, ef_high_numeric]]

    return processed_data

def get_model_path(model_folder='model', model_filename='trained_model.joblib'):
    current_file_dir = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(current_file_dir, 'predict_model', model_folder, model_filename))

def load_trained_model():
    return get_model_path(model_filename='trained_model.joblib')


def load_label_encoder():
    return get_model_path(model_filename='label_encoder.joblib')



class StudentSurveyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        student_id = kwargs.pop("student_id")
        self.student_id = student_id
        super(StudentSurveyForm, self).__init__(*args, **kwargs)

        # Retrieve the survey questions for the student
        survey_questions = SurveyQuestion.objects.all().order_by("-pk")

        for question in survey_questions:
            choices = [
                (choice.id, choice.choice)
                for choice in SurveyQuestionChoice.objects.all()
            ]

            field_name = f"question_{question.id}"

            # Create a choice field for each question
            self.fields[field_name] = forms.ChoiceField(
                label=question.question,
                choices=choices,
                widget=forms.RadioSelect,
                required=True,
            )

    def clean(self):
        cleaned_data = super().clean()
        errors = []

        for field_name, selected_choice_id in cleaned_data.items():
            if not selected_choice_id:
                field_name = field_name.replace(
                    "question_", ""
                )  # Extract the question_id
                errors.append(f"You must select an answer for question {field_name}.")

        if errors:
            print(errors)
            raise forms.ValidationError(errors)

    def save_response(self, student, question_id, selected_choice_id):
        with transaction.atomic():
            survey_question = SurveyQuestion.objects.get(id=question_id)
            choice = SurveyQuestionChoice.objects.get(id=selected_choice_id)
            response = StudentSurveyQuestion(
                student=student,
                question=survey_question,
                answer=choice,
            )
            response.save()

    
    def calculate_mean(self, scores):
        if scores:
            scores = [score for score in scores if score is not None]
            if scores:
                return round(sum(scores) / len(scores), 2)
        return None
    
    
    def save_scores(self, student, question_id, selected_choice_id):
            survey_question = SurveyQuestion.objects.get(id=question_id)
            choice = SurveyQuestionChoice.objects.get(id=selected_choice_id)
            question_code = survey_question.code.lower()

            try:
                assessment = Assessment.objects.get(student=student)
            except Assessment.DoesNotExist:
                assessment = Assessment(student=student)

            if choice.value is not None:
                setattr(assessment, question_code + "_score", choice.value)
            else:
                # Set a default score value (e.g., 0) when choice.value is None
                setattr(assessment, question_code + "_score", 0)

            print("Saving the scores")
            assessment.save()


    def save_to_assessment(self, student):
        with transaction.atomic():
            try:
                assessment = Assessment.objects.get(student=student)
            except Assessment.DoesNotExist:
                assessment = Assessment(student=student)

            
            ex_scores = [getattr(assessment, f"ex{i}_score") for i in range(1, 6)]
            cy_scores = [getattr(assessment, f"cy{i}_score") for i in range(1, 5)]
            ef_scores = [getattr(assessment, f"ef{i}_score") for i in range(1, 7)]
            print(ex_scores)
            print(cy_scores)
            print(ef_scores)
            
            # Calculate means
            assessment.ex_mean = self.calculate_mean(ex_scores)
            assessment.cy_mean = self.calculate_mean(cy_scores)
            assessment.ef_mean = self.calculate_mean(ef_scores)

            # Retrieve the critical boundaries
            try:
                print("Getting the critical boundaries")
                critical_boundaries = CriticalBoundary.objects.get(id=1)
            except CriticalBoundary.DoesNotExist:
                # Create critical boundaries if it doesn't exist (this should run only for very first assessment)
                print("Creating critical boundaries")
                create_critical_boundaries()
                critical_boundaries = CriticalBoundary.objects.get(id=1)


            if (
                assessment.ex_mean is not None
                and assessment.cy_mean is not None
                and assessment.ef_mean is not None
                and critical_boundaries.ex_boundary is not None
                and critical_boundaries.cy_boundary is not None
                and critical_boundaries.ef_boundary is not None
            ):
                print("EX_MEAN: ", assessment.ex_mean)
                print("EX_BOUNDARY: ", critical_boundaries.ex_boundary)
                print("CY_MEAN: ", assessment.cy_mean)
                print("CY_BOUNDARY: ", critical_boundaries.cy_boundary)
                print("EF_MEAN: ", assessment.ef_mean)
                print("EF_BOUNDARY: ", critical_boundaries.ef_boundary)
                # Update the high fields based on means and boundaries
                assessment.ex_high = assessment.ex_mean > critical_boundaries.ex_boundary
                assessment.cy_high = assessment.cy_mean > critical_boundaries.cy_boundary
                assessment.ef_high = assessment.ef_mean > critical_boundaries.ef_boundary

                # Use the preprocess function to format the survey responses for prediction
                preprocessed_data = preprocess_data(assessment.ex_high, assessment.cy_high, assessment.ef_high)

                # Load the trained model
                trained_model = joblib.load(load_trained_model())

                # Load the label encoder
                label_encoder = joblib.load(load_label_encoder())

                # Make predictions using the preprocessed data
                predicted_profile_encoded = trained_model.predict(preprocessed_data)[0]

                # Decode the predicted profile
                predicted_profile_decoded = label_encoder.inverse_transform([predicted_profile_encoded])[0]

                # Get the BurnoutProfile instance based on the decoded value
                burnout_profile = BurnoutProfile.objects.get(profile=predicted_profile_decoded)

                # Update the created date of the assessment
                manila_tz = pytz.timezone('Asia/Manila')
                assessment.created_date = timezone.now().astimezone(manila_tz)

                # Update the profile field in the Assessment model with the BurnoutProfile instance
                assessment.profile = burnout_profile
                assessment.is_email_sent = False

            assessment.save()
            student.assessment_exists = True
            student.save()



    def save_to_backup(self, student, assessment):
        with transaction.atomic():
            assessment_data = {
                "student": student,
                "ef1_score": assessment.ef1_score,
                "ef2_score": assessment.ef2_score,
                "ef3_score": assessment.ef3_score,
                "ef4_score": assessment.ef4_score,
                "ef5_score": assessment.ef5_score,
                "ef6_score": assessment.ef6_score,
                "ex1_score": assessment.ex1_score,
                "ex2_score": assessment.ex2_score,
                "ex3_score": assessment.ex3_score,
                "ex4_score": assessment.ex4_score,
                "ex5_score": assessment.ex5_score,
                "cy1_score": assessment.cy1_score,
                "cy2_score": assessment.cy2_score,
                "cy3_score": assessment.cy3_score,
                "cy4_score": assessment.cy4_score,
                "ex_mean": assessment.ex_mean,
                "cy_mean": assessment.cy_mean,
                "ef_mean": assessment.ef_mean,
                "ex_high": assessment.ex_high,
                "cy_high": assessment.cy_high,
                "ef_high": assessment.ef_high,
                "profile": assessment.profile,
            }

            backup = StudentAssessmentHistory(**assessment_data)
            backup.save()

    def save(self, request):
        if isinstance(request, Student):
            student = request
        else:
            student = request.user.student

        with transaction.atomic():
            assessment_data = {}  # Store assessment data
            for field_name, selected_choice_id in self.cleaned_data.items():
                question_id = field_name.split("_")[-1]
                selected_choice_id = int(selected_choice_id)
                self.save_response(student, question_id, selected_choice_id)  # Save to StudentSurveyQuestion
                assessment_data[question_id] = selected_choice_id  # Store assessment data
                print("Assessment data: ", assessment_data) 

            # Save assessment scores after all questions are processed
            for question_id, selected_choice_id in assessment_data.items():
                self.save_scores(student, question_id, selected_choice_id)

            # Save data to assessment and backup table after saving the scores
            assessment = Assessment.objects.get(student=student)
            self.save_to_assessment(student)  # Save to Assessment
            self.save_to_backup(student, assessment)  # Save to Backup

