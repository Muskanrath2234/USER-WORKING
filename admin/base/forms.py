# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    user_type = forms.ChoiceField(choices=[('user', 'User'), ('admin', 'Admin')])
