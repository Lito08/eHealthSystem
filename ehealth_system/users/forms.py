from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from hostels.models import Hostel, Room

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)
    matric_id = forms.CharField(max_length=20, required=False, label="Matric ID", widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    email = forms.EmailField(required=False, label="Email", widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    name = forms.CharField(max_length=100, required=False, label="Full Name")
    phone_number = forms.CharField(max_length=15, required=False)
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
        fields = ['role', 'matric_id', 'email', 'name', 'phone_number', 'hostel_block', 'room', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        # Exclude 'superadmin' from role choices
        self.fields['role'].choices = [(r[0], r[1]) for r in self.fields['role'].choices if r[0] != 'superadmin']

        # Dynamically populate rooms based on selected hostel block
        if 'hostel_block' in self.data:
            try:
                hostel_id = int(self.data.get('hostel_block'))
                self.fields['room'].queryset = Room.objects.filter(hostel_id=hostel_id)
            except (ValueError, TypeError):
                self.fields['room'].queryset = Room.objects.none()

        # Hide the name field for 'superadmin' role only
        if 'role' in self.data and self.data.get('role') == 'superadmin':
            self.fields['name'].widget = forms.HiddenInput()
            self.fields['name'].required = False
        else:
            self.fields['name'].required = True
