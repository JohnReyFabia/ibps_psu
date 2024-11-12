from bs4 import BeautifulSoup
from django.http import QueryDict

# critical boundary computation
from statistics import stdev

# send email notification
from django.core.mail import send_mail

from .models import (
    Counselor,
    Assessment,
    BurnoutProfile,
    CriticalBoundary,
    StudentAssessmentHistory,
    StudentSurveyQuestion,
    SurveyQuestion,
)


def scrape_question_text(survey_question):
    # Access the question text
    question_text = survey_question.question

    # Assuming the question text is stored in an HTML format
    # Parse the HTML content of the question text
    soup = BeautifulSoup(question_text, "html.parser")

    # Extract the text content
    question_text = soup.get_text()

    return question_text


def insert_survey_data():
    import csv
    import json
    from .models import (
        SurveyQuestionChoice,
        Student,
    )
    from .forms import StudentSurveyForm
    from django.contrib.auth.models import User
    from django.db import transaction
    from .predict_model.prediction_model import (
        predict_burnout_profiles,
        load_trained_model,
    )

    def read_csv_to_dict(file_path):
        data_list = []
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                csv_reader = csv.DictReader(file)
                for n, row in enumerate(csv_reader):
                    date_key = list(row.keys())[0]
                    date_key_Should = "Date"
                    # replace date_key with date_key_Should
                    row[date_key_Should] = row.pop(date_key)
                    data_list.append(dict(row))

        except FileNotFoundError:
            print("File not found. Please provide a valid file path.")

        return data_list

    # Provide the path to your CSV file here
    file_path = r"c:\Users\Ramon Rodriguez\Downloads\MBI-CALCULATION-DG13.csv"
    data = read_csv_to_dict(file_path)

    json_text = json.dumps(data, indent=4)
    # print(json_text)
    output_file_path = "out.json"

    # Save the JSON data to a file
    with open(output_file_path, "w") as json_file:
        json_file.write(json_text)

    def insert_row(d, idx):
        possible_answers = {
            "0": SurveyQuestionChoice.objects.get(value=0).pk,
            "1": SurveyQuestionChoice.objects.get(value=1).pk,
            "2": SurveyQuestionChoice.objects.get(value=2).pk,
            "3": SurveyQuestionChoice.objects.get(value=3).pk,
            "4": SurveyQuestionChoice.objects.get(value=4).pk,
            "5": SurveyQuestionChoice.objects.get(value=5).pk,
            "6": SurveyQuestionChoice.objects.get(value=6).pk,
        }
        user = User.objects.get(email=d["Email Address"])
        student = Student.objects.get(account=user)

        if Assessment.objects.filter(student=student).exists():
            print("\n")
            print("=" * 50)
            print(f"{idx}) Survey already exists for: {user}")
            print("=" * 50)
            print("\n")
            return

        cleaned_data = {
            "question_15": possible_answers.get(d["CY4_SCORE"]),
            "question_14": possible_answers.get(d["CY3_SCORE"]),
            "question_13": possible_answers.get(d["CY2_SCORE"]),
            "question_12": possible_answers.get(d["CY1_SCORE"]),
            "question_11": possible_answers.get(d["EX5_SCORE"]),
            "question_10": possible_answers.get(d["EX4_SCORE"]),
            "question_9": possible_answers.get(d["EX3_SCORE"]),
            "question_8": possible_answers.get(d["EX2_SCORE"]),
            "question_7": possible_answers.get(d["EX1_SCORE"]),
            "question_6": possible_answers.get(d["EF5_SCORE"]),
            "question_5": possible_answers.get(d["EF4_SCORE"]),
            "question_4": possible_answers.get(d["EF3_SCORE"]),
            "question_3": possible_answers.get(d["EF2_SCORE"]),
            "question_2": possible_answers.get(d["EF1_SCORE"]),
            "question_1": possible_answers.get(d["EF6_SCORE"]),
        }

        # print(f"data got: {d}")

        ex_mean = float(d["EX_MEAN "])
        cy_mean = float(d["CY_MEAN"])
        ef_mean = float(d["EF_MEAN"])

        # for field_name, selected_choice_id in cleaned_data.items():
        #     print(f"field name: {field_name}, selected_choice_id: {selected_choice_id}")

        # raise NotImplementedError("Implement the following code")

        def calculate_mean(scores):
            if scores:
                scores = [score for score in scores if score is not None]
                if scores:
                    return round(sum(scores) / len(scores), 2)
                return None

        def save_response(student, question_id, selected_choice_id):
            with transaction.atomic():
                survey_question = SurveyQuestion.objects.get(id=question_id)
                choice = SurveyQuestionChoice.objects.get(id=selected_choice_id)
                response = StudentSurveyQuestion(
                    student=student,
                    question=survey_question,
                    answer=choice,
                )
                response.save()

        def preprocess_data(ex_high, cy_high, ef_high):
            # Convert boolean values to numerical format (1 for True, 0 for False)
            ex_high_numeric = 1 if ex_high else 0
            cy_high_numeric = 1 if cy_high else 0
            ef_high_numeric = 1 if ef_high else 0

            # Arrange the preprocessed values into a structured input (list or array)
            processed_data = [[ex_high_numeric, cy_high_numeric, ef_high_numeric]]

            return processed_data

        def save_to_assessment(student, question_id, selected_choice_id):
            with transaction.atomic():
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

                ex_scores = [
                    getattr(assessment, f"ex{i}_score")
                    for i in range(1, 6)
                    if getattr(assessment, f"ex{i}_score") is not None
                ]
                cy_scores = [
                    getattr(assessment, f"cy{i}_score")
                    for i in range(1, 5)
                    if getattr(assessment, f"cy{i}_score") is not None
                ]
                ef_scores = [
                    getattr(assessment, f"ef{i}_score")
                    for i in range(1, 7)
                    if getattr(assessment, f"ef{i}_score") is not None
                ]

                # Calculate means
                assessment.ex_mean = ex_mean
                assessment.cy_mean = cy_mean
                assessment.ef_mean = ef_mean
                # assessment.ex_mean = calculate_mean(ex_scores)
                # assessment.cy_mean = calculate_mean(cy_scores)
                # assessment.ef_mean = calculate_mean(ef_scores)

                # # views.create_critical_boundaries()
                # Use the preprocess function to format the survey responses for prediction
                preprocessed_data = preprocess_data(
                    assessment.ex_high, assessment.cy_high, assessment.ef_high
                )

                # Get the global critical boundaries
                critical_boundaries = CriticalBoundary.objects.get(id=1)
                print(critical_boundaries)

                if (
                    assessment.ex_mean is not None
                    and assessment.cy_mean is not None
                    and assessment.ef_mean is not None
                ):
                    print("EX_MEAN: ", assessment.ex_mean)
                    print("EX_BOUNDARY: ", critical_boundaries.ex_boundary)
                    print("CY_MEAN: ", assessment.cy_mean)
                    print("CY_BOUNDARY: ", critical_boundaries.cy_boundary)
                    print("EF_MEAN: ", assessment.ef_mean)
                    print("EF_BOUNDARY: ", critical_boundaries.ef_boundary)
                    # Update the high fields based on means and boundaries
                    assessment.ex_high = (
                        assessment.ex_mean > critical_boundaries.ex_boundary
                    )
                    assessment.cy_high = (
                        assessment.cy_mean > critical_boundaries.cy_boundary
                    )
                    assessment.ef_high = (
                        assessment.ef_mean > critical_boundaries.ef_boundary
                    )

                    loaded_weights, loaded_bias = load_trained_model()
                    if loaded_weights is not None and loaded_bias is not None:
                        # Use the loaded parameters for predictions
                        preprocessed_data = preprocess_data(
                            assessment.ex_high, assessment.cy_high, assessment.ef_high
                        )
                        predicted_profiles = predict_burnout_profiles(
                            preprocessed_data, loaded_weights, loaded_bias
                        )
                        try:
                            # Using the first profile in the list if it exists
                            profile_instance = BurnoutProfile.objects.get(
                                profile=predicted_profiles[0]
                            )
                            print("Profile instance found:", profile_instance)
                            assessment.profile = profile_instance
                            # Save the assessment when a profile is predicted
                            assessment.save()
                        except BurnoutProfile.DoesNotExist:
                            print("Profile does not exist in burnout profile")

                else:
                    print("Assessment not saved: Missing mean values")

                assessment.save()

        def save_to_backup(student, assessment):
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

        with transaction.atomic():
            for field_name, selected_choice_id in cleaned_data.items():
                print(
                    f"student: {student}, field name: {field_name}, selected_choice_id: {selected_choice_id}"
                )
                question_id = field_name.split("_")[-1]
                selected_choice_id = int(selected_choice_id)
                save_response(
                    student=student,
                    question_id=question_id,
                    selected_choice_id=selected_choice_id,
                )  # Save to StudentSurveyQuestion
                save_to_assessment(
                    student, question_id, selected_choice_id
                )  # Save to Assessment

            assessment = Assessment.objects.get(student=student)
            save_to_backup(student, assessment)  # Save to Backup

        print("\n")
        print("=" * 50)
        print(f"{idx}) Survey created succesfully for: {user}")
        print("=" * 50)
        print("\n")

    for i, dd in enumerate(data, start=1):
        # if i >= 2:
        #     return
        insert_row(dd, i)



# ----------------------------------------------------------------
# CALCULATE THE CRITICAL BOUNDARIES
# ----------------------------------------------------------------
def create_critical_boundaries():
    # Get all student assessment data
    assessments = Assessment.objects.all()
    ex_scores = []
    cy_scores = []
    ef_scores = []

    for assessment in assessments:
        ex_scores.extend([assessment.ex1_score, assessment.ex2_score, assessment.ex3_score, assessment.ex4_score, assessment.ex5_score])
        cy_scores.extend([assessment.cy1_score, assessment.cy2_score, assessment.cy3_score, assessment.cy4_score])
        ef_scores.extend([assessment.ef1_score, assessment.ef2_score, assessment.ef3_score, assessment.ef4_score, assessment.ef5_score, assessment.ef6_score])

    # Calculate the global critical boundaries based on all student data
    ex_avg = sum(ex_scores) / len(ex_scores) 
    cy_avg = sum(cy_scores) / len(cy_scores) 
    ef_avg = sum(ef_scores) / len(ef_scores) 

    ex_stdev = stdev(ex_scores) 
    cy_stdev = stdev(cy_scores)
    ef_stdev = stdev(ef_scores) 

    ex_boundary = round(ex_avg + (ex_stdev * 0.5), 2)
    cy_boundary = round(cy_avg + (cy_stdev * 1.25), 2)
    ef_boundary = round(ef_avg + (ef_stdev * 0.1), 2)

    # Update the critical boundaries
    critical_boundaries, created = CriticalBoundary.objects.get_or_create(id=1)
    critical_boundaries.ex_boundary = ex_boundary
    critical_boundaries.cy_boundary = cy_boundary
    critical_boundaries.ef_boundary = ef_boundary
    critical_boundaries.save()


# ----------------------------------------------------------------
# SEND ALARMING STUDENTS TO COUNSELOR EMAIL
# ----------------------------------------------------------------
    
def notify_counselor(instance):
    print("Entering notify_counselor")

    # Profiles that trigger notification
    burnout_profiles = [
        "Burned Out", "Overextended", "Disengaged", "Ineffective",
        "Overextended and Disengaged", "Overextended and Ineffective",
        "Disengaged and Ineffective"
    ]
    # Check if student's burnout profile matches any of the specified profiles
    if instance.profile.profile in burnout_profiles:
        if not instance.is_email_sent:
            print("I am here!")
            college = instance.student.program.college
            counselor = Counselor.objects.filter(college=college).first()

            if counselor:
                first_name = instance.student.first_name
                last_name = instance.student.last_name
                student_name = f"{last_name}, {first_name}" 
                student_program = instance.student.program
                student_email = instance.student.email
                # Email message
                email_subject = f'{instance.profile.profile} Burnout Profile in {counselor.college}'
                email_body = (
                    f'Dear Counselor,\n\n'
                    f'We have detected potential signs of burnout in {counselor.college}.\n\n'
                    f'{student_name.upper()} ({student_email}) of {student_program} has been identified with a burnout profile of {instance.profile.profile.upper()}.\n\n'
                    f'Please take appropriate actions to provide support.\n\n'
                    f'Best regards,\nIBPS PSU'
                )
                # Send email to counselor
                try:
                    send_mail(
                        email_subject,
                        email_body,
                        None, 
                        [counselor.email],
                        fail_silently=False,
                    )
                    print(f"Email notification sent successfully to {counselor.email}")
                    instance.is_email_sent = True
                    instance.save(update_fields=['is_email_sent'])
                except Exception as e:
                    print(f"Failed to send email notification to {counselor.email}: {e}")
