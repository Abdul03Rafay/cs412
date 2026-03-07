# File: mini_insta/forms.py
# Author: Abdul Rafay (rafaya@bu.edu), 2/20/2026 - 3/6/2026
# Description: Python file to define forms which are used for create/update/delete operations

from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

class CreateProfileForm(forms.ModelForm):
    '''A form to create a new Profile.'''
    class Meta:
        model = Profile
        fields = ['user_name', 'display_name', 'bio_text', 'profile_image_url']

class RegistrationForm(UserCreationForm):
    '''A form to create a new User and Profile.'''
    
    display_name = forms.CharField(max_length=100, help_text="Enter your display name.")
    bio_text = forms.CharField(widget=forms.Textarea, help_text="Tell us about yourself.")
    profile_image_url = forms.URLField(required=False, help_text="Link to your profile picture (optional).")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

class CommentForm(forms.ModelForm):
    '''A form to create a new Comment.'''
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'}),
        }