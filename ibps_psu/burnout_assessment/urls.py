from django.urls import path, re_path
from . import views


app_name = "burnout_assessment"

urlpatterns = [
    path('survey/<str:student_id>/', views.student_survey, name='student-survey'),
    path('result/<str:student_id>/', views.student_result, name='student-result'),
    # path('sort_students/', views.sort_students_by_profile, name='sort_students'),
    
]