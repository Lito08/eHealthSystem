from django import forms
from .models import Resident, Block, Level, Room
from django.contrib.auth import get_user_model

User = get_user_model()

class ResidentForm(forms.ModelForm):
    # Fields explicitly declared for customization
    matric_id = forms.CharField(max_length=10, required=False, disabled=True, label="Matric ID")  # Read-only field
    account_type = forms.ChoiceField(
        choices=[('STA', 'Staff'), ('LEC', 'Lecturer'), ('STU', 'Student')],
        label="Account Type",
    )
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")
    block = forms.ModelChoiceField(queryset=Block.objects.all(), label="Block")
    level = forms.ModelChoiceField(queryset=Level.objects.all(), label="Level")
    room_number = forms.ModelChoiceField(queryset=Room.objects.all(), label="Room Number")

    class Meta:
        model = Resident
        fields = ['first_name', 'last_name', 'account_type', 'block', 'level', 'room_number']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract user without causing errors
        super().__init__(*args, **kwargs)

        if user:  # Initialize matric_id dynamically based on account type
            # If the user has a corresponding Resident, get account type from there
            try:
                resident = user.resident
                self.fields['matric_id'].initial = self.generate_matric_id(resident.account_type)
            except Resident.DoesNotExist:
                # Handle case where user doesn't have a resident profile (fallback)
                self.fields['matric_id'].initial = self.generate_matric_id('STU')  # Default to 'STU'

        # Dynamically update the room_number queryset based on block and level
        self.fields['room_number'].queryset = self.get_available_rooms()

    @staticmethod
    def generate_matric_id(account_type):
        """
        Generate the next matric_id based on the account_type.
        """
        prefixes = {'STA': 'A24DW', 'LEC': 'L24DW', 'STU': 'S24DW'}
        role_prefix = prefixes.get(account_type, 'S24DW')  # Default to 'Student'

        # Query the latest matric_id for the given account type
        last_user = User.objects.filter(matric_id__startswith=role_prefix).order_by('-matric_id').first()
        if last_user:
            next_number = int(last_user.matric_id[5:]) + 1
        else:
            next_number = 1

        return f"{role_prefix}{str(next_number).zfill(4)}"

    def update_matric_id(self, account_type):
        """
        Update matric_id dynamically when the account_type changes.
        """
        self.fields['matric_id'].initial = self.generate_matric_id(account_type)

    def clean(self):
        cleaned_data = super().clean()
        account_type = cleaned_data.get('account_type')
        block = cleaned_data.get('block')
        level = cleaned_data.get('level')

        # Dynamically update room_number choices based on block and level
        if block and level:
            self.fields['room_number'].queryset = Room.objects.filter(block=block, level=level)
        
        # Ensure matric_id is updated based on the account type
        if account_type:
            self.update_matric_id(account_type)

        return cleaned_data

    def get_available_rooms(self):
        """
        Fetch available rooms based on block and level.
        """
        # Default queryset that will be dynamically updated in clean()
        return Room.objects.none()
