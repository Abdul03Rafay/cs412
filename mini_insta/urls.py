# mini_insta/urls.py

from django.urls import path
from .views import ProfileListView # our view class defintion

urlpatterns = [
    # map the URL (empty string) to the view
    path('', ProfileListView.as_view(), name='show_all_profiles'),
]
