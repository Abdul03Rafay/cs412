from .models import Profile
from django.views.generic import ListView, DetailView

# Create your views here.
class ProfileListView(ListView):
    '''Create a subclass of ListView to display all profile records.'''
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html' ## reusing same template
    context_object_name = 'profiles'
    
class ProfileDetailView(DetailView):
    '''Create a subclass of ListView to display all profile records.'''
    model = Profile
    template_name = 'mini_insta/show_profile.html' ## reusing same template
    context_object_name = 'profile'