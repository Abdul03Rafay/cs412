# File: mini_insta/urls.py
# Author: Abdul Rafay (rafaya@bu.edu), 2/13/2026
# Description: Python file to handle relevant urls.

from django.urls import path
from .views import ProfileListView, ProfileDetailView, PostDetailView, CreatePostView, UpdateProfileView, UpdatePostView, DeletePostView, ShowFollowersDetailView, ShowFollowingDetailView, PostFeedListView, SearchView # our view class defintion

app_name = 'mini_insta'

urlpatterns = [
    # map the URL (empty string) to the view
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
    path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('profile/<int:pk>/create_post/', CreatePostView.as_view(), name='create_post'),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name='show_followers'),
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name='show_following'),
    path('profile/<int:pk>/feed', PostFeedListView.as_view(), name='post_feed'),
    path('profile/<int:pk>/search', SearchView.as_view(), name='search'),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name='update_post'),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
]
