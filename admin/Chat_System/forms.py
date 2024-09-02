from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.models import ModelForm
from django.forms.widgets import FileInput
from .models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'image']  # Assuming 'title', 'content', and 'image' are fields in your Post model

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

