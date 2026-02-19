# File: blog/forms/py
# Author: Abdul Rafay (rafaya@bu.edu), 2/19/2026
# Description: Python file to to define forms which are used for create/update/delete operations

from django import forms
from .models import Article, Comment

class CreateArticleForm(forms.ModelForm):
    '''A form to add an Article to the database.'''
    
    class Meta: 
        '''Associate this form with a model from our database.'''
        model = Article
        fields = ['author', 'title', 'text', 'image_url']
        
class CreateCommentForm(forms.ModelForm):
    '''A form to add an Comment to the database.'''
    
    class Meta: 
        '''Associate this form with the comment model; select fields.'''
        model = Comment
        fields = ['author', 'text',]