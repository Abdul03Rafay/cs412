# File: mini_insta/urls.py
# Author: Abdul Rafay (rafaya@bu.edu), 2/13/2026
# Description: Python file to handle relevant urls.

from django.urls import path
from .views import * # our view class defintion

app_name = 'mini_insta'

urlpatterns = [
    # map the URL (empty string) to the view
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
    path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('profile/<int:pk>/create_post/', CreatePostView.as_view(), name='create_post')
]
