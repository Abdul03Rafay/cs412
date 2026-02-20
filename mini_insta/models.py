# File: mini_insta/models.py
# Author: Abdul Rafay (rafaya@bu.edu), 2/13/2026 - 2/20/2026.
# Description: Python file to define relevant models and their data attributes.

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
    
    def get_all_posts(self):
        '''Return all of the Posts related to this profile.'''
        
        posts = Post.objects.filter(profile=self)
        return posts
    
class Post(models.Model):
    '''Encapsulate the idea of Post with relevant data attributes.'''
    
    # data attributes of a Post:
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=False)
    
    def __str__(self):
        '''Return a string representation of this post object.'''
        return f'{self.caption}'
    
    def get_all_photos(self):
        '''Return all of the Photos related to this post.'''
        
        photos = Photo.objects.filter(post=self)
        return photos
    
class Photo(models.Model):
    '''Encapsuate the data attributes of Photo related to Post.'''
    
    # data attributes of a Photo:
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    image_url = models.URLField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        '''Return a string representation of this photo object.'''
        return f'{self.image_url}'
    