from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from hostels.models import Hostel, Room

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)
    matric_id = forms.CharField(
        max_length=20,
        required=False,
        label="Matric ID",
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
    )
    email = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
    )
    full_name = forms.CharField(max_length=100, required=False, label="Full Name")
    phone_number = forms.CharField(max_length=15, required=False)
    hostel_block = forms.ModelChoiceField(
        queryset=Hostel.objects.all(),
        empty_label="Select Hostel (Optional)",
        required=False,
    )
    room = forms.ModelChoiceField(
        queryset=Room.objects.none(),
        empty_label="Select Room (Optional)",
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = ['role', 'matric_id', 'email', 'full_name', 'phone_number', 'hostel_block', 'room', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        # Exclude 'superadmin' from role choices
        self.fields['role'].choices = [(r[0], r[1]) for r in self.fields['role'].choices if r[0] != 'superadmin']

        # Dynamically populate room options based on the selected hostel
        if 'hostel_block' in self.data:
            try:
                hostel_id = int(self.data.get('hostel_block'))
                self.fields['room'].queryset = Room.objects.filter(hostel_id=hostel_id, resident=None)
            except (ValueError, TypeError):
                self.fields['room'].queryset = Room.objects.none()
        elif self.instance.pk:  # If editing an existing user
            if self.instance.room:
                hostel_id = self.instance.room.hostel.id
                self.fields['room'].queryset = Room.objects.filter(
                    hostel_id=hostel_id
                ) | Room.objects.filter(resident=self.instance)
            else:
                self.fields['room'].queryset = Room.objects.none()
        else:
            self.fields['room'].queryset = Room.objects.none()

        # Automatically hide the full_name field for 'superadmin'
        if self.instance.role == 'superadmin':
            self.fields['full_name'].widget = forms.HiddenInput()
            self.fields['full_name'].required = False
        else:
            self.fields['full_name'].required = True
