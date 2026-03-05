# File: mini_insta/views.py
# Author: Abdul Rafay (rafaya@bu.edu), 2/13/2026 - 2/20/2026
# Description: Python file to define views.

from .models import Profile, Post, Photo
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm, RegistrationForm
from django.urls import reverse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login

# Create your views here.
class RegisterView(CreateView):
    '''A view to handle user registration and profile creation.'''
    template_name = 'mini_insta/register.html'
    form_class = RegistrationForm

    def form_valid(self, form):
        '''Save the user and then create the associated profile.'''
        # Save the User object
        user = form.save()
        
        # Log the user in
        login(self.request, user)

        # Create the Profile object linked to this user
        Profile.objects.create(
            user=user,
            user_name=user.username,
            display_name=form.cleaned_data.get('display_name'),
            bio_text=form.cleaned_data.get('bio_text'),
            profile_image_url=form.cleaned_data.get('profile_image_url'),
        )

        return redirect(reverse('mini_insta:show_all_profiles'))

    def get_success_url(self) -> str:
        return reverse('mini_insta:show_all_profiles')

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

class LoggedInProfileDetailView(LoginRequiredMixin, DetailView):
    '''A view to show the logged-in user's own profile.'''
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        '''Return the Profile object associated with the logged-in user.'''
        return Profile.objects.filter(user=self.request.user).first()
    
class PostDetailView(DetailView):
    ''' Create a subclass of DetailView to display all post records.'''
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

class CreatePostView(LoginRequiredMixin, CreateView):
    '''A view to create a new post and save it to the database.'''
    
    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"
    
    def get_object(self, queryset=None):
        '''Return the profile of the logged-in user.'''
        return Profile.objects.filter(user=self.request.user).first()

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
    
        # calling the superclass method
        context = super().get_context_data(**kwargs)
        
        # add this profile into the context dictionary:
        context['profile'] = self.get_object()
        return context
    
    def form_valid(self, form):
        '''This method handles the form submission and saves the new object to the Django database. 
        We need to add the foreign key (of the Profile). to the Post object before saving it to the database.'''
        
        #instrument our code to display form fields:
        print(f"CreatePostView.form_valid: form.cleaned_data={form.cleaned_data}")
        
        profile = self.get_object()
        #attach this profile to the post
        form.instance.profile = profile # set the FK
        
        # delegate the work to the superclass method form_valid:
        response = super().form_valid(form)
    
        # read the files from the form:
        files = self.request.FILES.getlist('files')
        for f in files:
            Photo.objects.create(
                post=self.object,
                image_file=f,
            )
            
        return response
    
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        return reverse('mini_insta:post_detail', kwargs={'pk': self.object.pk})
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''A view to update a profile and save it to the database.'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"

    def get_object(self, queryset=None):
        '''Return the Profile object associated with the logged-in user.'''
        return Profile.objects.filter(user=self.request.user).first()
    
class UpdatePostView(LoginRequiredMixin, UpdateView):
    '''A view to update a post and save it to the database.'''

    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        return reverse('mini_insta:post_detail', kwargs={'pk': self.object.pk})

class DeletePostView(LoginRequiredMixin, DeleteView):
    '''A view to delete a post and remove it from the database.'''

    model = Post
    template_name = "mini_insta/delete_post_form.html"

    def get_context_data(self, **kwargs):
        '''Provide context variables for the delete_post_form.html template.'''
        context = super().get_context_data(**kwargs)
        # Adding post and profile to the context
        context['post'] = self.object
        context['profile'] = self.object.profile
        return context

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully deleting the post.'''
        return reverse('mini_insta:show_profile', kwargs={'pk': self.object.profile.pk})
    
class ShowFollowersDetailView(DetailView):
    '''A view to display a list of followers for a profile.'''
    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"

class ShowFollowingDetailView(DetailView):
    '''A view to display a list of profiles a profile is following.'''
    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"

class PostFeedListView(LoginRequiredMixin, ListView):
    '''A view to show a personalized feed of posts from followed profiles.'''
    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        '''Override get_queryset to return only the feed for the logged-in user's profile.'''
        profile = Profile.objects.filter(user=self.request.user).first()
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        '''Pass the profile object to the context.'''
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(user=self.request.user).first()
        return context

class SearchView(LoginRequiredMixin, ListView):
    '''A view to search for Profiles and Posts based on a text query.'''
    model = Post
    template_name = 'mini_insta/search_results.html'

    def dispatch(self, request, *args, **kwargs):
        '''Intercept the request to show search form if no query is provided.'''
        query = request.GET.get('query')
        if not query:
            # If there's no query, just render the search form page
            profile = Profile.objects.filter(user=self.request.user).first()
            return render(request, 'mini_insta/search.html', {'profile': profile})
        # Otherwise, continue with the normal ListView process
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        '''Return Posts matching the query.'''
        query = self.request.GET.get('query')
        if query:
            return Post.objects.filter(caption__icontains=query)
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        '''Provide query text and matching Profiles to the context.'''
        context = super().get_context_data(**kwargs)
        
        context['profile'] = Profile.objects.filter(user=self.request.user).first()
        
        query = self.request.GET.get('query')
        if query:
            context['query'] = query
            # Search across user_name, display_name, or bio_text
            context['profiles'] = Profile.objects.filter(
                Q(user_name__icontains=query) | 
                Q(display_name__icontains=query) | 
                Q(bio_text__icontains=query)
            )
            context['posts'] = self.get_queryset()
            
        return context
