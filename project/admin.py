# File: project/admin.py
# Author: Abdul Rafay (rafaya@bu.edu), 4/20/2026
# Description: Register models for the Prayer Times application with the Django Admin site.

from django.contrib import admin
from .models import City, PrayerTime, Profile, HijriCalendar, SavedCity

admin.site.register(City)
admin.site.register(PrayerTime)
admin.site.register(Profile)
admin.site.register(HijriCalendar)
admin.site.register(SavedCity)
