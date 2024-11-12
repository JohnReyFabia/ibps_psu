from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model, authenticate
import re
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError


# student register email validation 
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.conf import settings

from burnout_assessment.models import Student, Program, College, Counselor

class StudentForm(ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    student_id = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Student ID (####-##-####)"}))
    program = forms.ModelChoiceField(widget=forms.Select(attrs={"placeholder": "Select your Program"}), queryset=Program.objects.all(), initial=1)
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "id": "new-password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm password", "id": "confirm-password"}))

    class Meta:
        model = Student
        fields = ['email', 'student_id', 'program', 'password', 'confirm_password']

    def is_valid_email(self, email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    # def generate_verification_code(self):
    #     import random
    #     return ''.join(random.choice('0123456789') for _ in range(6))

    # def send_verification_email(self, email, verification_code):
    #     subject = 'Email Verification'
    #     message = f'Your verification code is: {verification_code}'
    #     from_email = settings.DEFAULT_FROM_EMAIL
    #     recipient_list = [email]

    #     send_mail(subject, message, from_email, recipient_list)

    #     # Store the verification code in the Student model
    #     self.instance.email_verification_code = verification_code

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not re.match(r'^\d', email) or not email.endswith("@psu.palawan.edu.ph"):
            raise forms.ValidationError("Only PSU student corporate emails are allowed.")

        # Check if the email format is valid
        if not self.is_valid_email(email):
            raise forms.ValidationError("Invalid email format.")

        # # Send a verification email
        # verification_code = self.generate_verification_code()
        # self.send_verification_email(email, verification_code)

        return email

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if not re.match(r'^\d{4}-\w{1,5}-\w{2,6}$', student_id):
            raise forms.ValidationError("Invalid student ID format.")
        return student_id

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match.")
        return confirm_password

    def save(self, commit=True):
        student = super().save(commit=False)
        student_id = self.cleaned_data.get('student_id')
        
        # Create a user
        user = get_user_model().objects.create_user(username=student_id.replace('-', ''), email=self.cleaned_data['email'], password=self.cleaned_data['password'])
        
        student.account = user
        
        if commit:
            student.save()
        
        return student
    

class CounselorForm(ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    counselor_id = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Counselor ID"}))
    college = forms.ModelChoiceField(widget=forms.Select(attrs={"placeholder": "Select your College"}), queryset=College.objects.all(), initial=1)
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "id": "new-password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm password", "id": "confirm-password"}))

    class Meta:
        model = Counselor
        fields = ['email', 'counselor_id', 'college', 'password', 'confirm_password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith("@psu.palawan.edu.ph"):
            raise forms.ValidationError("Only psu corporate emails are allowed.")
        return email


    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match.")
        return confirm_password

    def save(self, commit=True):
        counselor = super().save(commit=False)
        counselor_id = self.cleaned_data.get('counselor_id')
        
        # Create a user
        user = get_user_model().objects.create_user(username=counselor_id, email=self.cleaned_data['email'], password=self.cleaned_data['password'])
        
        counselor.account = user
        
        if commit:
            counselor.save()
        
        return counselor
    

class LoginForm(forms.Form):
    user_log = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Email or Student No."}))
    user_pass = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "id": "password"}))


class UpdateProfileForm(ModelForm):
    # last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Last name"}))
    # first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "First name"}))
    # middle_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Middle name (Optional)",}), required=False)
    # contact_number = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder": "Enter your Number"}))
    # gender = forms.ChoiceField(widget=forms.Select(attrs={"placeholder": "Select your Gender"}), choices=Student.gender_choice)
    age = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder": "Enter your age"}))
    # civil_status = forms.ChoiceField(widget=forms.Select(attrs={"placeholder": "Select your Status"}), choices=Student.status)
    program = forms.ModelChoiceField(widget=forms.Select(attrs={"placeholder": "Select your Program"}), queryset = Program.objects.all(), initial = 0,)


    class Meta:
        model = Student
        fields = ['age', 'program']
        # fields = ['email', 'student_id', 'gender', 'age', 'civil_status', 'program', 'password', 'confirm_password',]


    # def save(self, commit=True):
    #     student = super().save(commit=False)

    #     # Update the associated user's first name and last name
    #     if student.account:
    #         user = student.account
    #         user.first_name = self.cleaned_data['first_name']
    #         user.last_name = self.cleaned_data['last_name']
    #         user.save()

    #     if commit:
    #         student.save()
    #     return student
    

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your current password', "id": "old-password"}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter a new password', "id": "new-password"}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your new password', "id": "confirm-password"} ))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
    
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        user = self.user

        if not user.check_password(old_password):
            raise forms.ValidationError("The old password input is incorrect.")
        return old_password
    
    def clean_new_password(self):
        old_password = self.cleaned_data.get('old_password')
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        user = self.user

        if old_password and user.check_password(new_password1, old_password):
            raise forms.ValidationError("Your new password cannot be the same as your current password.")

        try:
            validate_password(new_password1, self.user)
        except DjangoValidationError as e:
            raise forms.ValidationError(e.messages[0])
        
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Passwords don't match.")
        return new_password2
    


class ForgotPassForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Email"}))

    

class ChangePassForm(PasswordChangeForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter a new password', "id": "new-password"}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your new password', "id": "confirm-password"}))

    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
    
    def clean_new_password(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        try:
            validate_password(new_password1, self.user)
        except DjangoValidationError as e:
            raise forms.ValidationError(e.messages[0])
        
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Passwords don't match.")
        return new_password2
    
