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
        queryset=CustomUser.objects.none(),  # Dynamically populated in `__init__`
        required=False,
        label="Assigned Resident",
    )

    clear_resident = forms.BooleanField(
        required=False, label="Clear Assigned Resident", initial=False
    )

    class Meta:
        model = Room
        fields = ['resident']

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)

        # Check if editing an existing room
        if self.instance and self.instance.resident:
            self.fields['resident'].queryset = CustomUser.objects.filter(
                models.Q(role='student') & 
                (models.Q(rooms_assigned=None) | models.Q(id=self.instance.resident.id))
            )
            self.fields['resident'].initial = self.instance.resident
        else:
            self.fields['resident'].queryset = CustomUser.objects.filter(role='student', rooms_assigned=None)

        self.fields['resident'].label_from_instance = lambda obj: f"{obj.matric_id} - {obj.full_name or 'N/A'}"

    def save(self, commit=True):
        room = super(RoomForm, self).save(commit=False)

        # Handle clearing the assigned resident
        if self.cleaned_data.get('clear_resident'):
            room.resident = None
        else:
            room.resident = self.cleaned_data.get('resident')

        if commit:
            room.save()

            # If assigning a resident, clear their previous room assignment
            if self.cleaned_data.get('resident'):
                self.cleaned_data['resident'].rooms_assigned.clear()
                self.cleaned_data['resident'].rooms_assigned.add(room)

        return room
