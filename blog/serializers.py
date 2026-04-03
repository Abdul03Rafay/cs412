# blog/serializers.py

from rest_framework import serializers
from .models import *

# Create your serializers here.

class ArticleSerializer(serializers.ModelSerializer):
    '''Serializer for the Article model.'''
    class Meta:
        model = Article
        fields = '__all__'
