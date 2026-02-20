# File: mini_insta/urls.py
# Author: Abdul Rafay (rafaya@bu.edu), 2/13/2026
# Description: Python file to handle relevant urls.

from django.urls import path
from .views import ProfileListView, ProfileDetailView, PostDetailView # our view class defintion

urlpatterns = [
    # map the URL (empty string) to the view
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
    path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),
]
