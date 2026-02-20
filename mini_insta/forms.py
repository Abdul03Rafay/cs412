# File: mini_insta/forms/py
# Author: Abdul Rafay (rafaya@bu.edu), 2/20/2026
# Description: Python file to to define forms which are used for create/update/delete operations

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''A form to create an post to the database.'''
    
    # extra field for photos.
    image_url = forms.URLField( 
        label="Image URL",
        required = False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://.....jpg',
            'class': 'form-control'
        })
    )
    
    class Meta: 
        '''Associate this form with a model from our database.'''
        model = Post
        fields = ['caption']