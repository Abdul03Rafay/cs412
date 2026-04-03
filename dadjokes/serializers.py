# dadjokes/serializers.py
# Author: Abdul Rafay (rafaya@bu.edu), 4/2/2026
# Description: Serializers for the dadjokes REST API.

from rest_framework import serializers
from .models import Joke, Picture

# Create your serializers here.

class JokeSerializer(serializers.ModelSerializer):
    '''Serializer for the Joke model.'''
    class Meta:
        model = Joke
        fields = '__all__'

class PictureSerializer(serializers.ModelSerializer):
    '''Serializer for the Picture model.'''
    class Meta:
        model = Picture
        fields = '__all__'
