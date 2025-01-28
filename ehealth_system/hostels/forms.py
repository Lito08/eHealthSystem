from django import forms
from django.db import models
from .models import Hostel, Room
from users.models import CustomUser

class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = ['name', 'block', 'levels', 'rooms_per_level']

class RoomForm(forms.ModelForm):
    resident = forms.ModelChoiceField(
        queryset=CustomUser.objects.none(),  # Default to none, dynamically populated in `__init__`
        required=False,
        label="Assigned Resident",
    )

    class Meta:
        model = Room
        fields = ['resident']

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)

        # Limit the queryset to residents who are eligible for room assignment
        if self.instance and self.instance.resident:
            # Include the current resident to allow editing
            self.fields['resident'].queryset = CustomUser.objects.filter(
                models.Q(role__in=['student', 'staff', 'lecturer']),
                models.Q(rooms_assigned=None) | models.Q(id=self.instance.resident.id)
            )
        else:
            self.fields['resident'].queryset = CustomUser.objects.filter(
                role__in=['student', 'staff', 'lecturer'],
                rooms_assigned=None
            )

        # Customize the display of resident options to include matric ID and full name
        self.fields['resident'].label_from_instance = lambda obj: f"{obj.matric_id} - {obj.full_name}"

    def save(self, commit=True):
        room = super(RoomForm, self).save(commit=False)

        # Update `is_occupied` based on the presence of a resident
        if self.cleaned_data.get('resident'):
            room.is_occupied = True
        else:
            room.is_occupied = False

        if commit:
            room.save()

            # Update the resident's room assignment if applicable
            if self.cleaned_data.get('resident'):
                self.cleaned_data['resident'].rooms_assigned.clear()  # Clear existing room assignments
                self.cleaned_data['resident'].rooms_assigned.add(room)

        return room
