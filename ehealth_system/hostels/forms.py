from django import forms
from .models import Hostel, Room

class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = ['name', 'block', 'levels', 'rooms_per_level']

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['resident']
