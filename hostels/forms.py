from django import forms
from django.core.exceptions import ValidationError
from .models import Hostel, Room
from users.models import CustomUser

class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = ['name', 'block', 'levels', 'rooms_per_level', 'is_infected_hostel']  # Added is_infected_hostel checkbox

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        block = cleaned_data.get('block')

        # Check if hostel with the same name and block already exists
        existing_hostel = Hostel.objects.filter(name=name, block=block)

        if self.instance.pk:
            existing_hostel = existing_hostel.exclude(pk=self.instance.pk)

        if existing_hostel.exists():
            raise ValidationError("A hostel with the same name and block already exists.")

        return cleaned_data


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

        # Allowed roles for residents (Students, Lecturers, University Staff)
        allowed_roles = ['student', 'lecturer', 'staff']

        # Fetch users with allowed roles who don't already have a room
        available_residents = CustomUser.objects.filter(role__in=allowed_roles, rooms_assigned__isnull=True)

        # If editing an existing room and it has a resident, allow them to stay in the options
        if self.instance and self.instance.resident:
            available_residents = available_residents | CustomUser.objects.filter(id=self.instance.resident.id)

        self.fields['resident'].queryset = available_residents.distinct()

        self.fields['resident'].label_from_instance = lambda obj: f"{obj.matric_id} - {obj.full_name or 'N/A'}"

    def save(self, commit=True):
        room = super(RoomForm, self).save(commit=False)

        # Handle clearing the assigned resident
        if self.cleaned_data.get('clear_resident'):
            if room.resident:
                room.resident.rooms_assigned.clear()  # Clear previous room assignment
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
