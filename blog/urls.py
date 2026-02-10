# blog/urls.py

from django.urls import path
from .views import ShowAllView # our view class defintion

urlpatterns = [
    # map the URL (empty string) to the view
    path('', ShowAllView.as_view(), name='show_all'),
]
