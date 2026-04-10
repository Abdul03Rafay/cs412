# File: mini_insta/serializers.py
# Author: Abdul Rafay (rafaya@bu.edu), 2/13/2026 - 4/9/2026
# Description: Serializers for mini_insta models to support REST API.

from rest_framework import serializers
from .models import Profile, Post, Photo, Follow, Like, Comment

class PhotoSerializer(serializers.ModelSerializer):
    '''Serializer for the Photo model.'''
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['id', 'image_url', 'timestamp']

    def get_image_url(self, obj):
        '''Return the proper image URL.'''
        return obj.get_image_url()

class PostSerializer(serializers.ModelSerializer):
    '''Serializer for the Post model.'''
    photos = PhotoSerializer(many=True, read_only=True, source='photo_set')
    profile_name = serializers.ReadOnlyField(source='profile.user_name')

    class Meta:
        model = Post
        fields = ['id', 'profile', 'profile_name', 'caption', 'timestamp', 'photos']

class ProfileSerializer(serializers.ModelSerializer):
    '''Serializer for the Profile model.'''
    num_followers = serializers.ReadOnlyField(source='get_num_followers')
    num_following = serializers.ReadOnlyField(source='get_num_following')
    
    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'user_name', 'display_name', 
            'bio_text', 'profile_image_url', 'num_followers', 
            'num_following'
        ]
