# forms.py
from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'available_seat', 'type', 'available_date', 'floor']




