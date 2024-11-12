from django.urls import path, re_path
from django.contrib.auth.views import LogoutView
from . import views

import nltk
app_name = "landingpage"

urlpatterns = [
    path("test/", views.test, name="test"),
    # user landing page
    path("", views.home, name="home"),
    # authentication
    path("student/register/", views.student_register, name="student-register"),
    path("counselor/register/", views.counselor_register, name="counselor-register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("reset_pass/", views.forget_password, name="forget-pass"),
    path("reset_password/<hashed_token>/", views.reset_password, name="reset-password"),
    path("password/change/", views.change_password, name="change-password"),
    path("feedback/", views.send_email_form, name="feedback"),
    # admin functions
    path("dashboard", views.admin_dashboard, name="admin-dashboard"),
    path("assessment/update/", views.enable_assessment, name="enable-assessment"),
    path("list/college/<code>/", views.admin_college_list, name="college-list"),
    path("list/student/takers/", views.admin_student_takers_list, name="student-takers-list"),
    path("list/student/", views.admin_student_list, name="student-list"),
    path("list/students/all/", views.admin_all_student_list, name="all-student-list"),
    path('students/upload/', views.upload_students, name='upload-students'),
    path("list/student/burnedout/", views.student_burnout_list, name="burnedout-student-list-no-college"),
    path("list/student/overextended/", views.student_overextended_list, name="overextended-student-list-no-college"),
    path("list/student/disengaged/", views.student_disengaged_list, name="disengaged-student-list-no-college"),
    path("list/student/ineffective/", views.student_ineffective_list, name="ineffective-student-list-no-college"),
    path("list/student/overextendedanddisengaged/", views.student_oandd_list, name="oandd-student-list-no-college"),
    path("list/student/overextendedandineffective/", views.student_oandi_list, name="oandi-student-list-no-college"),
    path("list/student/disengagedandineffective/", views.student_dandi_list, name="dandi-student-list-no-college"),
    path("list/student/engaged/", views.student_engaged_list, name="engaged-student-list-no-college"),
    path("list/student/burnedout/<college_name>/", views.student_burnout_list, name="burnedout-student-list"),
    path("list/student/overextended/<college_name>/", views.student_overextended_list, name="overextended-student-list"),
    path("list/student/disengaged/<college_name>/", views.student_disengaged_list, name="disengaged-student-list"),
    path("list/student/ineffective/<college_name>/", views.student_ineffective_list, name="ineffective-student-list"),
    path("list/student/overextendedanddisengaged/<college_name>/", views.student_oandd_list, name="oandd-student-list"),
    path("list/student/overextendedandineffective/<college_name>/", views.student_oandi_list, name="oandi-student-list"),
    path("list/student/disengagedandineffective/<college_name>/", views.student_dandi_list, name="dandi-student-list"),
    path("list/student/engaged/<college_name>/", views.student_engaged_list, name="engaged-student-list"),
    path("excel/download/", views.admin_download_excel, name='admin_download_excel'),
    # counselor functions
    path("counselor/dashboard/", views.counselor_dashboard, name="counselor-dashboard"),
    path("counselor/list/student/all/", views.counselor_all_student_list, name="counselor-all-student-list"),
    path("counselor/list/student/", views.counselor_student_list, name="counselor-student-list"),
    path("counselor/list/student/takers/", views.counselor_student_takers_list, name="counselor-student-takers-list"),
    path("counselor/list/student/burnedout/", views.counselor_student_burnout_list, name="counselor-burnedout-student-list"),
    path("counselor/list/student/overextended/", views.counselor_student_overextended_list, name="counselor-overextended-student-list"),
    path("counselor/list/student/disengaged/", views.counselor_student_disengaged_list, name="counselor-disengaged-student-list"),
    path("counselor/list/student/ineffective/", views.counselor_student_ineffective_list, name="counselor-ineffective-student-list"),
    path("counselor/list/student/overextendedanddisengaged/", views.counselor_student_oandd_list, name="counselor-oandd-student-list"),
    path("counselor/list/student/overextendedandineffective/", views.counselor_student_oandi_list, name="counselor-oandi-student-list"),
    path("counselor/list/student/disengagedandineffective/", views.counselor_student_dandi_list, name="counselor-dandi-student-list"),
    path("counselor/list/student/engaged/", views.counselor_student_engaged_list, name="counselor-engaged-student-list"),
    path("excel/download/counselor/", views.counselor_download_excel, name='counselor_download_excel'),
    # student functions
    path("student/dashboard/", views.student_dashboard, name="student-dashboard"),
    path("student/assessment/", views.student_assessment1, name="student-assessment1"),
    path("student/test/take/", views.student_assessment2, name="student-assessment2"),
    path("student/profile/edit/", views.student_edit_profile, name="edit-profile"),
    # admin and counselor student profile view
    path("profile/student/<student_id>/", views.student_profile, name="student-profile"),
    # template views
    path("service/terms/", views.tos, name="tos"),
    path("policy/privacy/", views.privacy_policy, name="privacy-policy"),
    # other function
    path("get-counselor-email/<student_id>/", views.get_counselor_email, name="get_counselor_email"),
    # path('get_keywords_and_counts/', views.get_keywords_and_counts, name='get_keywords_and_counts'),
    # path('update-assessment-exists/', views.update_assessment_exists, name="update_assessment_exists"),
]
