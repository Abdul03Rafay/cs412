# File: mini_insta/views.py
# Author: Abdul Rafay (rafaya@bu.edu), 2/13/2006
# Description: Python file to define views.

from .models import Profile, Post
from django.views.generic import ListView, DetailView

# Create your views here.
class ProfileListView(ListView):
    '''Create a subclass of ListView to display all profile records.'''
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html' ## reusing same template
    context_object_name = 'profiles'
    
class ProfileDetailView(DetailView):
    '''Create a subclass of DetailView to display all profile records.'''
    model = Profile
    template_name = 'mini_insta/show_profile.html' ## reusing same template
    context_object_name = 'profile'
    
class PostDetailView(DetailView):
    ''' Create a subclass of DetailView to display all post records.'''
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'