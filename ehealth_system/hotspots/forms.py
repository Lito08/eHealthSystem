from django import forms
from .models import Hotspot

class HotspotForm(forms.ModelForm):
    class Meta:
        model = Hotspot
        fields = ['location_name', 'infected_count', 'recovered_count', 'latitude', 'longitude']
