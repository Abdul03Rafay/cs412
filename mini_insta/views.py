# File: mini_insta/views.py
# Author: Abdul Rafay (rafaya@bu.edu), 2/13/2026 - 2/20/2026
# Description: Python file to define views.

from .models import Profile, Post, Photo
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
from django.urls import reverse
from django.shortcuts import render
from django.db.models import Q

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

class CreatePostView(CreateView):
    '''A view to create a new comment and save it to the database.'''
    
    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
    
        # calling the superclass method
        context = super().get_context_data(**kwargs)
        
        # find/add the profile to the context data
        # retrive the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        
        # add this profile into the context dictionary:
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        '''This method handles the form submission and saves the new object to the Django database. 
        We need to add the foreign key (of the Profile). to the Post object before saving it to the database.'''
        
        #instrument our code to display form fields:
        print(f"CreateCommentView.form_valid: form.cleaned_data={form.cleaned_data}")
        
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        #attach this profile to the comment
        form.instance.profile = profile # set the FK
        
        # delegate the work to the superclass method form_valid:
        response = super().form_valid(form)
    
        # image_url = form.cleaned_data.get('image_url')
        # if image_url:
        #     Photo.objects.create(
        #         post=self.object, # newly saved Post
        #         image_url=image_url,
        #     )
            
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
        
        
        # create and return a URL:
        # return reverse('show_all')
        
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        # call reverse to generate the URL for this Profile
        return reverse('mini_insta:post_detail', kwargs={'pk': self.object.pk})
    
class UpdateProfileView(UpdateView):
    '''A view to update a profile and save it to the database.'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"
    
class UpdatePostView(UpdateView):
    '''A view to update a post and save it to the database.'''

    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        return reverse('mini_insta:post_detail', kwargs={'pk': self.object.pk})

class DeletePostView(DeleteView):
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

class PostFeedListView(ListView):
    '''A view to show a personalized feed of posts from followed profiles.'''
    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        '''Override get_queryset to return only the feed for the specific profile.'''
        profile_pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=profile_pk)
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        '''Pass the profile object to the context.'''
        context = super().get_context_data(**kwargs)
        profile_pk = self.kwargs['pk']
        context['profile'] = Profile.objects.get(pk=profile_pk)
        return context

class SearchView(ListView):
    '''A view to search for Profiles and Posts based on a text query.'''
    model = Post
    template_name = 'mini_insta/search_results.html'

    def dispatch(self, request, *args, **kwargs):
        '''Intercept the request to show search form if no query is provided.'''
        query = request.GET.get('query')
        if not query:
            # If there's no query, just render the search form page
            profile_pk = self.kwargs['pk']
            profile = Profile.objects.get(pk=profile_pk)
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
        
        profile_pk = self.kwargs['pk']
        context['profile'] = Profile.objects.get(pk=profile_pk)
        
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
