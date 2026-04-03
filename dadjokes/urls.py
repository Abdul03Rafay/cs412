# File: dadjokes/urls.py
# Author: Abdul Rafay (rafaya@bu.edu), 4/2/2026
# Description: URL patterns for the dadjokes app.

from django.urls import path
from .views import *

urlpatterns = [
    path('', RandomView.as_view(), name='random'),
    path('random', RandomView.as_view(), name='random_explicit'),
    path('jokes', ShowAllJokesView.as_view(), name='jokes'),
    path('joke/<int:pk>', JokeDetailView.as_view(), name='joke'),
    path('pictures', ShowAllPicturesView.as_view(), name='pictures'),
    path('picture/<int:pk>', PictureDetailView.as_view(), name='picture'),

    ### REST API views:
    path('api/', RandomJokeAPIView.as_view(), name='api_random_joke'),
    path('api/random', RandomJokeAPIView.as_view(), name='api_random_joke_explicit'),
    path('api/jokes', JokeListCreateAPIView.as_view(), name='api_jokes'),
    path('api/joke/<int:pk>', JokeDetailAPIView.as_view(), name='api_joke'),
    path('api/pictures', PictureListAPIView.as_view(), name='api_pictures'),
    path('api/picture/<int:pk>', PictureDetailAPIView.as_view(), name='api_picture'),
    path('api/random_picture', RandomPictureAPIView.as_view(), name='api_random_picture'),
]
