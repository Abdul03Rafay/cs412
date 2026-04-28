# File: project/forms.py
# Author: Abdul Rafay (rafaya@bu.edu), 4/21/2026
# Description: Defines the forms for the Prayer Times application.

from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    '''Form for creating/updating a user Profile.'''
    class Meta:
        '''Associate this form with the Profile model and its fields.'''
        model = Profile
        fields = ['madhab', 'calculation_method', 'display_language']
        widgets = {
            'display_language': forms.TextInput(attrs={'class': 'form-input'}),
        }
