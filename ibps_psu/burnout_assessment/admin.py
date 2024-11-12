from django.contrib import admin
from .models import (
    College, 
    Program, 
    Student, 
    Counselor,
    SurveyQuestion, 
    SurveyQuestionChoice, 
    StudentSurveyQuestion, 
    CriticalBoundary,
    Assessment, 
    StudentAssessmentHistory,
    BurnoutProfile,
    BurnoutFactor,
    ForgotPasswordRequest
    )

# Register your models here.

@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "college_name", "is_assessment_enabled",)
    search_fields = ("id", "code", "college_name", )

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("id", "college" ,"program_name", )
    search_fields = ("id", "college__college_name" ,"program_name",)

@admin.register(Counselor)
class CounselorAdmin(admin.ModelAdmin):
    list_display = ("id","email", "counselor_id", "college",)
    search_fields = ("id","email", "counselor_id", "college__college_name",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id","email", "student_id", "last_name", "first_name", "middle_name", "age", "program",)
    search_fields = ("id","email", "student_id", "last_name", "first_name", "middle_name", "age", "program__program_name",)


@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "code","question",)
    search_fields = ("id","code", "question",)


@admin.register(SurveyQuestionChoice)
class SurveyQuestionChoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "choice", "value",)
    search_fields = ("id","choice", "value",)


@admin.register(StudentSurveyQuestion)
class StudentSurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ("id","student","question", "answer",)
    search_fields = ("id","student__last_name","student__first_name","question__question", "answer",)

@admin.register(BurnoutProfile)
class BurnoutProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "profile","description",)
    search_fields = ("id","profile", "description",)

@admin.register(CriticalBoundary)
class CriticalBoundaryAdmin(admin.ModelAdmin):
    list_display = ("id","ex_boundary", "cy_boundary", "ef_boundary",)
    search_fields = ("id","ex_boundary", "cy_boundary", "ef_boundary",)

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ("id", "created_date", "student", "ex_high", "cy_high", "ef_high","profile",)
    search_fields = ("id", "created_date", "student__last_name","student__first_name", "student__student_id", "profile",)


@admin.register(StudentAssessmentHistory)
class StudentAssessmentHistoryAdmin(admin.ModelAdmin):
    list_display = ("id","timestamp", "student",)
    search_fields = ("id","student__last_name","student__first_name",)


@admin.register(BurnoutFactor)
class BurnoutFactorAdmin(admin.ModelAdmin):
    list_display = ("id","factor", "count",)
    search_fields = ("id","factor","count",)


@admin.register(ForgotPasswordRequest)
class ForgotPasswordRequestAdmin(admin.ModelAdmin):
    list_display = ("id","user", "forget_pass_token",)
    search_fields = ("id","user__username",)