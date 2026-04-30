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
        fields = ['city', 'madhab', 'calculation_method', 'display_language', 'notification_preference']
        widgets = {
            'display_language': forms.TextInput(attrs={'class': 'form-input'}),
        }


class AddCityForm(forms.Form):
    '''Form for searching and adding a city by name.'''
    city_query = forms.CharField(
        label='City',
        max_length=200,
        widget=forms.TextInput(attrs={
            'class':        'form-input',
            'placeholder':  'Search or type a city — e.g. London, United Kingdom',
            'list':         'cities-datalist',
            'autocomplete': 'off',
        })
    )

    def clean_city_query(self):
        '''Strip whitespace and raise a validation error if the field is empty.'''
        value = self.cleaned_data['city_query'].strip()
        if not value:
            raise forms.ValidationError('Please enter a city name.')
        return value
