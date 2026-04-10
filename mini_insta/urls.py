# File: mini_insta/urls.py
# Author: Abdul Rafay (rafaya@bu.edu), 2/13/2026 - 4  /9/2026
# Description: Python file to handle relevant urls.

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    ProfileListView, ProfileDetailView, PostDetailView, CreatePostView, 
    UpdateProfileView, UpdatePostView, DeletePostView, ShowFollowersDetailView, 
    ShowFollowingDetailView, PostFeedListView, SearchView, LoggedInProfileDetailView, 
    CreateProfileView, FollowView, UnfollowView, LikeView, UnlikeView,
    LogoutConfirmationView, CreateCommentView
)
from .api_views import (
    ProfileListAPIView, ProfileDetailAPIView, ProfilePostsAPIView, 
    ProfileFeedAPIView, PostCreateAPIView, LoginAPIView
)

app_name = 'mini_insta'

urlpatterns = [
    # map the URL (empty string) to the view
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/', LoggedInProfileDetailView.as_view(), name='show_my_profile'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
    path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('profile/create_post/', CreatePostView.as_view(), name='create_post'),
    path('profile/update', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/feed', PostFeedListView.as_view(), name='post_feed'),
    path('profile/search', SearchView.as_view(), name='search'),
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name='show_followers'),
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name='show_following'),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name='update_post'),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    path('login/', LoginView.as_view(template_name='mini_insta/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='mini_insta:logout_confirmation'), name='logout'),
    path('logout_confirmation/', LogoutConfirmationView.as_view(), name='logout_confirmation'),
    path('profile/<int:pk>/follow', FollowView.as_view(), name='follow'),
    path('profile/<int:pk>/delete_follow', UnfollowView.as_view(), name='unfollow'),
    path('post/<int:pk>/like', LikeView.as_view(), name='like'),
    path('post/<int:pk>/delete_like', UnlikeView.as_view(), name='unlike'),
    path('post/<int:pk>/comment', CreateCommentView.as_view(), name='create_comment'),

    # API endpoints
    path('api/', ProfileListAPIView.as_view(), name='api_root'),
    path('api/profiles/', ProfileListAPIView.as_view(), name='api_profile_list'),
    path('api/profiles/<int:pk>/', ProfileDetailAPIView.as_view(), name='api_profile_detail'),
    path('api/profiles/<int:pk>/posts/', ProfilePostsAPIView.as_view(), name='api_profile_posts'),
    path('api/profiles/<int:pk>/feed/', ProfileFeedAPIView.as_view(), name='api_profile_feed'),
    path('api/posts/', PostCreateAPIView.as_view(), name='api_post_create'),
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
]
