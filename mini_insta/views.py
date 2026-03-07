# File: mini_insta/views.py
# Author: Abdul Rafay (rafaya@bu.edu), 2/13/2026 - 3/6/2026
# Description: Python file to define views.

from .models import Profile, Post, Photo, Follow, Like, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm, RegistrationForm, CreateProfileForm, CommentForm
from django.urls import reverse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import RedirectView

# Create your views here.
class CreateProfileView(CreateView):
    '''A view to handle user registration and profile creation in one step.'''
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_insta/create_profile_form.html'

    def get_context_data(self, **kwargs):
        '''Add UserCreationForm to the context.'''
        context = super().get_context_data(**kwargs)
        # Store an instance of UserCreationForm in the context
        context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        '''Handle form submission for both User and Profile.'''
        # Reconstruct UserCreationForm instance from POST data
        user_form = UserCreationForm(self.request.POST)

        if user_form.is_valid():
            # Save the new User object
            user = user_form.save()
            
            # Log the user in
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            # Attach the User to the Profile instance
            form.instance.user = user
            
            # Delegate to superclass form_valid to save Profile
            return super().form_valid(form)
        else:
            # If user_form is invalid, re-render the page with errors
            return self.render_to_response(self.get_context_data(form=form, user_form=user_form))

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully creating a profile.'''
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

    def get_context_data(self, **kwargs):
        '''Provide is_following context variable.'''
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            follower_profile = Profile.objects.filter(user=self.request.user).first()
            if follower_profile:
                context['is_following'] = Follow.objects.filter(
                    follower_profile=follower_profile, 
                    profile=self.get_object()
                ).exists()
        return context

class LoggedInProfileDetailView(LoginRequiredMixin, DetailView):
    '''A view to show the logged-in user's own profile.'''
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        '''Return the Profile object associated with the logged-in user.'''
        return Profile.objects.filter(user=self.request.user).first()
    
    def get_login_url(self) -> str:
        '''Return the URL to the application's login page.'''
        return reverse('mini_insta:login')
    
class PostDetailView(DetailView):
    ''' Create a subclass of DetailView to display all post records.'''
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        '''Provide is_liked context variable.'''
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            profile = Profile.objects.filter(user=self.request.user).first()
            if profile:
                context['is_liked'] = Like.objects.filter(
                    profile=profile, 
                    post=self.get_object()
                ).exists()
        context['comment_form'] = CommentForm()
        return context

class CreatePostView(LoginRequiredMixin, CreateView):
    '''A view to create a new post and save it to the database.'''
    
    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"
    
    def get_object(self, queryset=None):
        '''Return the profile of the logged-in user.'''
        return Profile.objects.filter(user=self.request.user).first()

    def get_login_url(self) -> str:
        '''Return the URL to the application's login page.'''
        return reverse('mini_insta:login')

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
    
    def get_login_url(self) -> str:
        '''Return the URL to the application's login page.'''
        return reverse('mini_insta:login')
    
class UpdatePostView(LoginRequiredMixin, UpdateView):
    '''A view to update a post and save it to the database.'''

    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        return reverse('mini_insta:post_detail', kwargs={'pk': self.object.pk})

    def get_login_url(self) -> str:
        '''Return the URL to the application's login page.'''
        return reverse('mini_insta:login')

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
    
    def get_login_url(self) -> str:
        '''Return the URL to the application's login page.'''
        return reverse('mini_insta:login')
    
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

    def get_login_url(self) -> str:
        '''Return the URL to the application's login page.'''
        return reverse('mini_insta:login')

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

    def get_login_url(self) -> str:
        '''Return the URL to the application's login page.'''
        return reverse('mini_insta:login')

class FollowView(LoginRequiredMixin, RedirectView):
    '''A view to create a Follow relationship between two Profiles.'''
    def get_redirect_url(self, *args, **kwargs):
        '''Return the URL to redirect to after following.'''
        pk = self.kwargs.get('pk')
        return reverse('mini_insta:show_profile', kwargs={'pk': pk})

    def dispatch(self, request, *args, **kwargs):
        '''Handle the follow action.'''
        follower_profile = Profile.objects.filter(user=request.user).first()
        profile_to_follow = Profile.objects.get(pk=self.kwargs.get('pk'))
        
        # Avoid self-following
        if follower_profile != profile_to_follow:
            Follow.objects.get_or_create(follower_profile=follower_profile, profile=profile_to_follow)
            
        return super().dispatch(request, *args, **kwargs)

class UnfollowView(LoginRequiredMixin, RedirectView):
    '''A view to delete a Follow relationship between two Profiles.'''
    def get_redirect_url(self, *args, **kwargs):
        '''Return the URL to redirect to after unfollowing.'''
        pk = self.kwargs.get('pk')
        return reverse('mini_insta:show_profile', kwargs={'pk': pk})

    def dispatch(self, request, *args, **kwargs):
        '''Handle the unfollow action.'''
        follower_profile = Profile.objects.filter(user=request.user).first()
        profile_to_unfollow = Profile.objects.get(pk=self.kwargs.get('pk'))
        
        Follow.objects.filter(follower_profile=follower_profile, profile=profile_to_unfollow).delete()
            
        return super().dispatch(request, *args, **kwargs)

class LikeView(LoginRequiredMixin, RedirectView):
    '''A view to create a Like object for a Post.'''
    def get_redirect_url(self, *args, **kwargs):
        '''Return the URL to redirect to after liking.'''
        pk = self.kwargs.get('pk')
        return reverse('mini_insta:post_detail', kwargs={'pk': pk})

    def dispatch(self, request, *args, **kwargs):
        '''Handle the like action.'''
        profile = Profile.objects.filter(user=request.user).first()
        post = Post.objects.get(pk=self.kwargs.get('pk'))
        
        # Avoid liking own post
        if post.profile != profile:
            Like.objects.get_or_create(profile=profile, post=post)
            
        return super().dispatch(request, *args, **kwargs)

class UnlikeView(LoginRequiredMixin, RedirectView):
    '''A view to delete a Like object for a Post.'''
    def get_redirect_url(self, *args, **kwargs):
        '''Return the URL to redirect to after unliking.'''
        pk = self.kwargs.get('pk')
        return reverse('mini_insta:post_detail', kwargs={'pk': pk})

    def dispatch(self, request, *args, **kwargs):
        '''Handle the unlike action.'''
        profile = Profile.objects.filter(user=request.user).first()
        post = Post.objects.get(pk=self.kwargs.get('pk'))
        
        Like.objects.filter(profile=profile, post=post).delete()
            
        return super().dispatch(request, *args, **kwargs)

class LogoutConfirmationView(TemplateView):
    '''A view to display a logout confirmation page.'''
    template_name = 'mini_insta/logged_out.html'

class CreateCommentView(LoginRequiredMixin, CreateView):
    '''A view to create a new comment on a post.'''
    form_class = CommentForm
    template_name = 'mini_insta/create_comment_form.html' # We might not even need a separate template if we embed it, but CreateView usually wants one.

    def form_valid(self, form):
        '''Save the comment and link it to the post and user's profile.'''
        # Get the post based on the pk in URL
        post = Post.objects.get(pk=self.kwargs.get('pk'))
        # Get the current user's profile
        profile = Profile.objects.filter(user=self.request.user).first()
        
        # Link them
        form.instance.post = post
        form.instance.profile = profile
        
        return super().form_valid(form)

    def get_success_url(self):
        '''Return to the post detail page after commenting.'''
        return reverse('mini_insta:post_detail', kwargs={'pk': self.kwargs.get('pk')})
