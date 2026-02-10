from django.db import models

# Create your models here.

class Article(models.Model):
    '''Encapsulates the idea of an Article by some author.'''
    
    # data atributes of a Article:
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)
    
    def __str__(self):
        ''' Return a string representation og this Article object.'''
        return f'{self.title} by {self.author}'