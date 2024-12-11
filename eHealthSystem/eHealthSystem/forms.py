from django import forms
from .models import Resident, Block, Level, Room, AccountType

class ResidentForm(forms.ModelForm):
    class Meta:
        model = Resident
        fields = ['account_type', 'block', 'level', 'room_number']  # These fields are now handled automatically by the form

    name = forms.CharField(max_length=100, label="Full Name")
    account_type = forms.ChoiceField(choices=AccountType.choices, label="Account Type")
    
    block = forms.ModelChoiceField(queryset=Block.objects.all(), label="Resident Block")
    level = forms.ModelChoiceField(queryset=Level.objects.all(), label="Resident Level")
    room_number = forms.ModelChoiceField(queryset=Room.objects.none(), label="Room Number")  # Empty queryset initially

    # You could use the `__init__` method to dynamically filter the room options based on block and level.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Dynamically filter the room choices based on selected block and level
        if 'block' in self.data and 'level' in self.data:
            try:
                block_id = int(self.data.get('block'))
                level_id = int(self.data.get('level'))
                self.fields['room_number'].queryset = Room.objects.filter(block_id=block_id, level_id=level_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['room_number'].queryset = self.instance.room_number.all()
