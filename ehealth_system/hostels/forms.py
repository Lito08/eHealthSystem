from django import forms
from .models import Hostel, Room
from users.models import CustomUser

class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = ['name', 'block', 'levels', 'rooms_per_level']

class RoomForm(forms.ModelForm):
    resident = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(rooms_assigned__isnull=True),  # Use `rooms_assigned` instead of `rooms`
        required=False,
        label="Assigned Resident",
    )

    class Meta:
        model = Room
        fields = ['resident']

    def save(self, commit=True):
        room = super(RoomForm, self).save(commit=False)

        # Update is_occupied based on resident
        if self.cleaned_data.get('resident'):
            room.is_occupied = True
        else:
            room.is_occupied = False

        if commit:
            room.save()
            # Update resident's room if assigned
            if self.cleaned_data.get('resident'):
                self.cleaned_data['resident'].rooms_assigned.clear()  # Clear existing room assignments
                self.cleaned_data['resident'].rooms_assigned.add(room)

        return room
