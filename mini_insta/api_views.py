# File: mini_insta/api_views.py
# Author: Abdul Rafay (rafaya@bu.edu), 4/9/2026
# Description: API views for mini_insta using Django REST Framework.

from rest_framework import generics, permissions, authentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import Profile, Post
from .serializers import ProfileSerializer, PostSerializer

class LoginAPIView(ObtainAuthToken):
    '''Custom Login API View to return Token and Profile ID.'''
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        # Find the profile associated with this user
        profile = Profile.objects.filter(user=user).first()
        
        return Response({
            'token': token.key,
            'profile_id': profile.pk if profile else None,
            'user_name': profile.user_name if profile else user.username
        })

class ProfileListAPIView(generics.ListAPIView):
    '''API view to list all Profiles.'''
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class ProfileDetailAPIView(generics.RetrieveAPIView):
    '''API view to retrieve a single Profile.'''
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class ProfilePostsAPIView(generics.ListAPIView):
    '''API view to list all posts for a specific Profile.'''
    serializer_class = PostSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        '''Filter posts by profile pk from the URL.'''
        profile_pk = self.kwargs.get('pk')
        return Post.objects.filter(profile__pk=profile_pk).order_by('-timestamp')

class ProfileFeedAPIView(generics.ListAPIView):
    '''API view to list post feed for a specific Profile.'''
    serializer_class = PostSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        '''Return the feed for the profile specified in the URL.'''
        profile_pk = self.kwargs.get('pk')
        profile = Profile.objects.get(pk=profile_pk)
        return profile.get_post_feed()

class PostCreateAPIView(generics.CreateAPIView):
    '''API view to create a new Post.'''
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        '''
        Custom save logic. 
        We can optionally auto-assign the profile based on the authenticated user.
        '''
        profile = Profile.objects.filter(user=self.request.user).first()
        serializer.save(profile=profile)
