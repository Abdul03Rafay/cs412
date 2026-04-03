# File: dadjokes/models.py
# Author: Abdul Rafay (rafaya@bu.edu), 4/2/2026
# Description: Data models for the dadjokes app.

from django.db import models
from django.urls import reverse

# Create your models here.

class Joke(models.Model):
    '''Encapsulates the idea of a dad joke.'''

    # data attributes of a Joke:
    text = models.TextField(blank=False)
    contributor = models.TextField(blank=False)
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return a string representation of this Joke object.'''
        return f'{self.text[:60]} by {self.contributor}'

    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('joke', kwargs={'pk': self.pk})


class Picture(models.Model):
    '''Encapsulates the idea of a silly image or GIF.'''

    # data attributes of a Picture:
    image_url = models.URLField(blank=False)
    contributor = models.TextField(blank=False)
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return a string representation of this Picture object.'''
        return f'Picture by {self.contributor} ({self.image_url[:40]})'

    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('picture', kwargs={'pk': self.pk})
