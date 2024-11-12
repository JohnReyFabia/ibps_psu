from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# message decorators
from django.contrib import messages

# burnout_assessment models and forms
from .models import Student, Counselor, Assessment, StudentAssessmentHistory, CriticalBoundary, BurnoutProfile
from .forms import StudentSurveyForm

# utils functions
from .utils import create_critical_boundaries, notify_counselor
# for svm model
from sklearn import svm
import numpy as np





# ----------------------------------------------------------------
#  STUDENT ASSESSMENT FUNCTION
# ----------------------------------------------------------------

# STUDENT ASSESSMENT QUESTIONNAIRE FUNCTION
@login_required(login_url='/login')
def student_survey(request, student_id):
    try:
        student = Student.objects.get(email=request.user.email)  # Get the student using email
    except Student.DoesNotExist:
        return HttpResponse("Student not found")

    if request.session.get('just_logged_in', False) and not student.is_profile_updated:
        messages.info(request, 'Please update your profile information.')
        del request.session['just_logged_in']
        

    if request.method == 'POST':
        form = StudentSurveyForm(request.POST, student_id=student_id)
        if form.is_valid():
            form.save(request)
            create_critical_boundaries()
            assessment = Assessment.objects.filter(student=student).first()
            notify_counselor(assessment)
            # sort_students_by_profile()
            return redirect('burnout_assessment:student-result', student_id=student_id)
    else:
        form = StudentSurveyForm(student_id=student_id)

    return render(request, 'student/student-assessment.html', {'form': form, 'student': student, 'student_id': student.student_id})

# STUDENT ASSESSMENT RESULT DISPLAY FUNCTION
@login_required(login_url='/login')
def student_result(request, student_id):
    try:
        student = Student.objects.get(email=request.user.email)  # Get the student using email
        assessment = Assessment.objects.filter(student=student).first()
        burnout_profile = None  

        if assessment:
            burnout_profile = BurnoutProfile.objects.get(id=assessment.profile.id)

    except Student.DoesNotExist:
        return HttpResponse("Student not found")

    context = {
        'student': student,
        'student_id': student.student_id,
        'assessment': assessment,
        'burnout_profile': burnout_profile  
    }

    return render(request, 'student/student-result.html', context)



# ----------------------------------------------------------------
#  OTHER FUNCTIONS
# ----------------------------------------------------------------


# # PREPROCESSING THE ASSESSMENT COMPUTATION RESULT BEFORE PASSING TO PREDICTION MODEL
# def preprocess_data(ex_high, cy_high, ef_high):
#     # Convert boolean values to numerical format (1 for True, 0 for False)
#     ex_high_numeric = 1 if ex_high else 0
#     cy_high_numeric = 1 if cy_high else 0
#     ef_high_numeric = 1 if ef_high else 0

#     # Arrange the preprocessed values into a structured input (list or array)
#     processed_data = [[ex_high_numeric, cy_high_numeric, ef_high_numeric]]

#     return processed_data




# # Function for mapping the burnout profiles to BurnoutProfile instances
# def map_burnout_profile(ex_high, cy_high, ef_high):
#     if ex_high and cy_high and not ef_high:
#         profile_name = 'Burned out'
#     elif ex_high and not cy_high and ef_high:
#         profile_name = 'Overextended'
#     elif not ex_high and cy_high and ef_high:
#         profile_name = 'Disengaged'
#     elif not ex_high and not cy_high and not ef_high:
#         profile_name = 'Ineffective'
#     elif ex_high and cy_high and ef_high:
#         profile_name = 'Overextended and Disengaged'
#     elif ex_high and not cy_high and not ef_high:
#         profile_name = 'Overextended and Ineffective'
#     elif not ex_high and cy_high and not ef_high:
#         profile_name = 'Disengaged and Ineffective'
#     elif not ex_high and not cy_high and ef_high:
#         profile_name = 'Engaged'
#     else:
#         profile_name = 'Unmmatched'

#     try:
#         # Retrieve the corresponding BurnoutProfile instance based on the profile_name
#         profile_instance = BurnoutProfile.objects.get(profile=profile_name)
#     except BurnoutProfile.DoesNotExist:
#         # Handle the case where the corresponding profile instance doesn't exist
#         profile_instance = None

#     return profile_instance


# def sort_students_by_profile():
#     assessments = Assessment.objects.all()

#     for assessment in assessments:
#         ex_high = assessment.ex_high
#         cy_high = assessment.cy_high
#         ef_high = assessment.ef_high
#         profile = map_burnout_profile(ex_high, cy_high, ef_high)
#         assessment.profile = profile
#         assessment.save()
#         student_id = assessment.student 

#         print(f"Student ID: {student_id}, Predicted Burnout Profile: {profile}")

#     # return HttpResponse("Students sorted and printed in the terminal, and profiles saved in StudentAssessmentHistory.")




