from django.contrib.auth.backends import ModelBackend
from .models import User

class MatricIDBackend(ModelBackend):
    def authenticate(self, request, matric_id=None, password=None, **kwargs):
        try:
            user = User.objects.get(matric_id=matric_id)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None