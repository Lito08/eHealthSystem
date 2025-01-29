from django import forms
from .models import Hotspot

class HotspotForm(forms.ModelForm):
    class Meta:
        model = Hotspot
        fields = ['name', 'description', 'infected_count', 'recovered_count', 'latitude', 'longitude']

    # Hide latitude & longitude fields (they will be filled by JavaScript)
    latitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    longitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
