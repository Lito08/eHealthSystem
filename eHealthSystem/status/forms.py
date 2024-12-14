from django import forms
from .models import InfectedPerson, Hotplace

# Form for Infected Student or Lecturer
class InfectedPersonForm(forms.ModelForm):
    class Meta:
        model = InfectedPerson
        fields = ['name', 'student_or_lecturer', 'infected']

# Form for Hotplace
class HotplaceForm(forms.ModelForm):
    class Meta:
        model = Hotplace
        fields = ['name', 'description']
