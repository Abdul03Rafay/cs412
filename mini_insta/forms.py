# File: mini_insta/forms/py
# Author: Abdul Rafay (rafaya@bu.edu), 2/20/2026
# Description: Python file to to define forms which are used for create/update/delete operations

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''A form to create an post to the database.'''
    
    class Meta: 
        '''Associate this form with a model from our database.'''
        model = Post
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    '''A form to update a profile to the database.'''

    class Meta:
        '''Associate this form with the Profile model.'''
        model = Profile
        fields = ['display_name', 'bio_text', 'profile_image_url']

class UpdatePostForm(forms.ModelForm):
    '''A form to update a post to the database.'''

    class Meta:
        '''Associate this form with the Post model.'''
        model = Post
        fields = ['caption']