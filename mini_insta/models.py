# File: mini_insta/models.py
# Author: Abdul Rafay (rafaya@bu.edu), 2/13/2026
# Description: Python file to define profile records model.

from django.db import models

# Create your models here.
class Profile(models.Model):
    '''Encapsulates the requirment fields for an profile.'''
    
    # data atributes of a profile:
    user_name = models.TextField(blank=False)
    display_name= models.TextField(blank=False)
    bio_text= models.TextField(blank=False)
    join_date= models.DateTimeField(auto_now=True)
    profile_image_url = models.URLField(blank=True)
    
    def __str__(self):
        ''' Return a string representation on this Profile object.'''
        return f'{self.user_name} - {self.display_name}'