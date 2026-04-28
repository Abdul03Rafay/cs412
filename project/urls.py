# File: project/urls.py
# Author: Abdul Rafay (rafaya@bu.edu), 4/21/2026
# Description: URL configuration for the Prayer Times (Muezzin) application.

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    MapView,
    CityListView,
    CityDetailView,
    ProfileDetailView,
    ProfileUpdateView,
    HijriCalendarListView,
    save_city,
    unsave_city,
    add_city,
    fetch_prayer_times_api,
    register,
)

urlpatterns = [
    path('', MapView.as_view(), name='map'),
    path('cities/', CityListView.as_view(), name='city_list'),
    path('cities/add/', add_city, name='add_city'),
    path('city/<int:pk>/', CityDetailView.as_view(), name='city_detail'),
    path('city/<int:pk>/save/', save_city, name='save_city'),
    path('city/<int:pk>/unsave/', unsave_city, name='unsave_city'),
    path('profile/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('calendar/', HijriCalendarListView.as_view(), name='calendar_list'),
    path('api/prayer-times/', fetch_prayer_times_api, name='fetch_prayer_times_api'),

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register, name='register'),
]
