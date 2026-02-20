# File: mini_insta/views.py
# Author: Abdul Rafay (rafaya@bu.edu), 2/13/2026 - 2/20/2026
# Description: Python file to define views.

from .models import Profile, Post, Photo
from django.views.generic import ListView, DetailView, CreateView
from .forms import CreatePostForm
from django.urls import reverse

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
    
        image_url = form.cleaned_data.get('image_url')
        if image_url:
            Photo.objects.create(
                post=self.object, # newly saved Post
                image_url=image_url,
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
    
   
    
