# File: voter_analytics/urls.py
# Author: Abdul Rafay (rafaya@bu.edu), 3/20/2026
# Description: URL configuration for the voter_analytics app.

from django.urls import path
from . import views

app_name = 'voter_analytics'

urlpatterns = [
    path('', views.VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>', views.VoterDetailView.as_view(), name='voter'),
    path('graphs', views.VoterGraphsView.as_view(), name='graphs'),
]
