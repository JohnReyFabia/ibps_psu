from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from burnout_assessment.models import Student, Counselor

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        UserModel = get_user_model()

        try:
            user = None

            # Authenticate as a Student
            try:
                student = Student.objects.get(email=username)
                user = student.account
            except Student.DoesNotExist:
                pass

            # Authenticate as a Counselor
            try:
                counselor = Counselor.objects.get(email=username)
                user = counselor.account
            except Counselor.DoesNotExist:
                pass

            if user and user.check_password(password):
                return user

        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
