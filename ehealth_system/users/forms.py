from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from hostels.models import Hostel, Room

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)
    email = forms.EmailField()
    matric_id = forms.CharField(max_length=20, required=False)
    hostel_block = forms.ModelChoiceField(
        queryset=Hostel.objects.all(),
        empty_label="Select Hostel",
        required=True,
    )
    room = forms.ModelChoiceField(
        queryset=Room.objects.none(),
        empty_label="Select Room",
        required=True,
    )

    class Meta:
        model = CustomUser
        fields = ['role', 'username', 'email', 'matric_id', 'phone_number', 'hostel_block', 'room', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['role'].choices = [(r[0], r[1]) for r in self.fields['role'].choices if r[0] != 'superadmin']
        if 'hostel_block' in self.data:
            try:
                hostel_id = int(self.data.get('hostel_block'))
                self.fields['room'].queryset = Room.objects.filter(hostel_id=hostel_id)
            except (ValueError, TypeError):
                self.fields['room'].queryset = Room.objects.none()