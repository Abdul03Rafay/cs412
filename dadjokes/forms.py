# File: dadjokes/forms.py
# Author: Abdul Rafay (rafaya@bu.edu), 4/2/2026
# Description: Forms for the dadjokes app.

from django import forms
from .models import Joke

class CreateJokeForm(forms.ModelForm):
    '''A form to add a Joke to the database.'''

    class Meta:
        '''Associate this form with the Joke model.'''
        model = Joke
        fields = ['text', 'contributor']
