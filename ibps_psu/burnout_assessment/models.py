from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from bs4 import BeautifulSoup


# Create your models here.


class College(models.Model):
    code = models.CharField(max_length=5, default="None")
    college_name = models.CharField(max_length=55)
    is_assessment_enabled = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.college_name}"

    class Meta:
        verbose_name_plural = "colleges"


class Program(models.Model):
    program_name = models.CharField(max_length=50)
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.program_name}"

    class Meta:
        verbose_name_plural = "programs"


class Student(models.Model):
    gender_choice = [("Female", "Female"), ("Male", "Male")]
    status = [
        ("Single", "Single"),
        ("Married", "Married"),
        ("Widowed", "Widowed"),
        ("Separated", "Separated"),
    ]
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    # password = models.CharField(max_length=128)
    student_id = models.CharField(max_length=20, unique=True, help_text="Format: ####-######-#####")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    gender = models.CharField(max_length=6, choices=gender_choice, default=gender_choice[0][0])
    birthdate = models.DateField(default=None, null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    civil_status = models.CharField(max_length=10, choices=status)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    is_password_updated = models.BooleanField(default=False, blank=True, null=True)
    assessment_exists = models.BooleanField(default=False, blank=True, null=True)
    # email_verification_code = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        if not self.first_name and not self.last_name and not self.middle_name:
            return f"{self.student_id}"
        if self.middle_name:
            # DELACRUZ, Juan Pedro P.
            return f'{self.last_name.upper()}, {self.first_name.title()} {"".join(m[0].upper() for m in self.middle_name.strip().split(" "))}.'
        # DELACRUZ, Juan
        return f"{self.last_name.upper()}, {self.first_name.title()}"

    def full_name(self):
        if self.middle_name:
            return f'{self.last_name.upper()}, {self.first_name.title()} {"".join(m[0].upper() for m in self.middle_name.split(" "))}.'
        return f"{self.last_name.upper()}, {self.first_name.title()}"

    class Meta:
        verbose_name_plural = "students"


class Counselor(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    # password = models.CharField(max_length=128)
    counselor_id = models.CharField(max_length=20, unique=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.counselor_id}"

    class Meta:
        verbose_name_plural = "counselors"


class SurveyQuestion(models.Model):
    code = models.CharField(max_length=45, blank=True, null=True)
    question = models.TextField(max_length=100)

    def __str__(self):
        return f"{self.question}"

    class Meta:
        verbose_name_plural = "survey questions"


class SurveyQuestionChoice(models.Model):
    choice = models.CharField(max_length=100)
    value = models.PositiveSmallIntegerField(default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.choice}"

    class Meta:
        verbose_name_plural = "survey question choices"


class StudentSurveyQuestion(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    answer = models.ForeignKey(SurveyQuestionChoice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.last_name}, {self.student.first_name} {self.student.middle_name}"

    class Meta:
        verbose_name_plural = "student survey questions"
        ordering = ["-id"]  # Order by id in descending order

    def scrape_question_text(self):
        soup = BeautifulSoup(self.question.question, "html.parser")

        # Extract the text content
        question_text = soup.get_text()

        return question_text


class BurnoutProfile(models.Model):
    pic = models.ImageField(
        blank=True, null=True, upload_to="static/img/burnout_profiles/"
    )
    profile = models.CharField(max_length=45)
    description = models.TextField()
    remarks = models.TextField()

    def __str__(self):
        return f"{self.profile}"

    class Meta:
        verbose_name_plural = "burnout profiles"


class CriticalBoundary(models.Model):
    ex_boundary = models.FloatField(default=None, null=True, blank=True)
    cy_boundary = models.FloatField(default=None, null=True, blank=True)
    ef_boundary = models.FloatField(default=None, null=True, blank=True)

    class Meta:
        verbose_name_plural = "critical boundaries"


class Assessment(models.Model):
    created_date = models.DateTimeField(default=timezone.now, editable=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    ef1_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    ef2_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    ef3_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    ef4_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    ef5_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    ef6_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    cy1_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    cy2_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    cy3_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    cy4_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    ex1_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    ex2_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    ex3_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    ex4_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    ex5_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    ex_mean = models.FloatField(default=None, null=True, blank=True)
    cy_mean = models.FloatField(default=None, null=True, blank=True)
    ef_mean = models.FloatField(default=None, null=True, blank=True)
    ex_high = models.BooleanField(default=None, null=True, blank=True)
    cy_high = models.BooleanField(default=None, null=True, blank=True)
    ef_high = models.BooleanField(default=None, null=True, blank=True)
    profile = models.ForeignKey(
        BurnoutProfile, on_delete=models.CASCADE, null=True, blank=True
    )
    is_email_sent = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.student.last_name}, {self.student.first_name} {self.student.middle_name}"

    class Meta:
        verbose_name_plural = "assessment"


class StudentAssessmentHistory(models.Model):
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, default=None, null=True, blank=True
    )
    ef1_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    ef2_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    ef3_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    ef4_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    ef5_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    ef6_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    cy1_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    cy2_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    cy3_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    cy4_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    ex1_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    ex2_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    ex3_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    ex4_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    ex5_score = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    ex_mean = models.FloatField(default=None, null=True, blank=True)
    cy_mean = models.FloatField(default=None, null=True, blank=True)
    ef_mean = models.FloatField(default=None, null=True, blank=True)
    ex_high = models.BooleanField(default=None, null=True, blank=True)
    cy_high = models.BooleanField(default=None, null=True, blank=True)
    ef_high = models.BooleanField(default=None, null=True, blank=True)
    profile = models.ForeignKey(
        BurnoutProfile, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.student.last_name}, {self.student.first_name} {self.student.middle_name}"

    class Meta:
        verbose_name_plural = "student assessment history"


class BurnoutFactor(models.Model):
    factor = models.CharField(max_length=50)
    count = models.IntegerField(default=None)

    def __str__(self):
        return f"{self.factor}"

    class Meta:
        verbose_name_plural = "burnout factors"
        

class ForgotPasswordRequest(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, default=None, blank=True, null=True
    )
    # email = models.EmailField(max_length=100, default=None, blank=True, null=True)
    forget_pass_token = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return self.user.email

    def is_expired(self):
        return timezone.now() >= self.expiration_time

    class Meta:
        verbose_name_plural = "Forgot Password Requests"
