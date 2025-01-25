from django import forms
from .models import Resident, HealthStatus, QuarantineRoom

class ResidentForm(forms.ModelForm):
    class Meta:
        model = Resident
        fields = ['name', 'resident_id', 'resident_type']
        labels = {
            'resident_id': 'Id',  # Change the label for 'resident_id' to 'Id'
        }

class HealthStatusForm(forms.ModelForm):
    class Meta:
        model = HealthStatus
        fields = ['status']