from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    matric_id = forms.CharField(max_length=20, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'matric_id', 'phone_number', 'hostel_block', 'password1', 'password2']
