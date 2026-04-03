# File: dadjokes/views.py
# Author: Abdul Rafay (rafaya@bu.edu), 4/2/2026
# Description: Views for the dadjokes app.

from django.views.generic import ListView, DetailView, TemplateView
from .models import Joke, Picture
import random

# Create your views here.

class RandomView(TemplateView):
    '''Display one randomly selected Joke and one randomly selected Picture.'''
    template_name = 'dadjokes/random.html'

    def get_context_data(self, **kwargs):
        '''Return the context dictionary with one random joke and one random picture.'''
        context = super().get_context_data(**kwargs)
        all_jokes = list(Joke.objects.all())
        all_pictures = list(Picture.objects.all())
        context['joke'] = random.choice(all_jokes)
        context['picture'] = random.choice(all_pictures)
        return context

class ShowAllJokesView(ListView):
    '''Display all Jokes in the database.'''
    model = Joke
    template_name = 'dadjokes/jokes.html'
    context_object_name = 'jokes'

class JokeDetailView(DetailView):
    '''Display one Joke by its primary key.'''
    model = Joke
    template_name = 'dadjokes/joke.html'
    context_object_name = 'joke'

class ShowAllPicturesView(ListView):
    '''Display all Pictures in the database.'''
    model = Picture
    template_name = 'dadjokes/pictures.html'
    context_object_name = 'pictures'

class PictureDetailView(DetailView):
    '''Display one Picture by its primary key.'''
    model = Picture
    template_name = 'dadjokes/picture.html'
    context_object_name = 'picture'


#### REST API Views ####

from rest_framework import generics
from .serializers import JokeSerializer, PictureSerializer

class RandomJokeAPIView(generics.RetrieveAPIView):
    '''Return a JSON representation of one Joke selected at random.'''
    serializer_class = JokeSerializer

    def get_object(self):
        '''Return one Joke object chosen at random.'''
        all_jokes = list(Joke.objects.all())
        return random.choice(all_jokes)

class JokeListCreateAPIView(generics.ListCreateAPIView):
    '''Return a JSON representation of all Jokes, or create a new Joke via POST.'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class JokeDetailAPIView(generics.RetrieveAPIView):
    '''Return a JSON representation of one Joke by its primary key.'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class PictureListAPIView(generics.ListAPIView):
    '''Return a JSON representation of all Pictures.'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class PictureDetailAPIView(generics.RetrieveAPIView):
    '''Return a JSON representation of one Picture by its primary key.'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class RandomPictureAPIView(generics.RetrieveAPIView):
    '''Return a JSON representation of one Picture selected at random.'''
    serializer_class = PictureSerializer

    def get_object(self):
        '''Return one Picture object chosen at random.'''
        all_pictures = list(Picture.objects.all())
        return random.choice(all_pictures)
