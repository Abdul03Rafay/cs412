# File: project/models.py
# Author: Abdul Rafay (rafaya@bu.edu), 4/20/2026
# Description: Defines the data models for the Prayer Times (Muezzin) application.

from django.db import models
from django.contrib.auth.models import User

class City(models.Model):
    '''Represents a geographic location for which prayer times are calculated.'''
    name = models.TextField(blank=False)
    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)
    timezone = models.TextField(blank=False)

    def __str__(self):
        '''Return a string representation of this City.'''
        return f"{self.name}"

class PrayerTime(models.Model):
    '''Stores the daily prayer times for a specific City and date.'''
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    date = models.DateField(blank=False)
    
    # Prayer times
    fajr = models.TimeField(blank=False)
    sunrise = models.TimeField(blank=False)
    zuhr = models.TimeField(blank=False)
    asr = models.TimeField(blank=False)
    maghrib = models.TimeField(blank=False)
    isha = models.TimeField(blank=False)

    def __str__(self):
        '''Return a string representation of these Prayer Times.'''
        return f"Prayer Times for {self.city.name} on {self.date}"

class Profile(models.Model):
    '''Extends the User model with additional settings for prayer calculations.'''
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='project_profile')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    
    # Madhab choices (Standard vs Shafi etc.)
    MADHAB_CHOICES = [
        ('Standard', 'Standard (Imam Shafi, Hanbali, Maliki)'),
        ('Hanafi', 'Hanafi'),
    ]
    madhab = models.TextField(choices=MADHAB_CHOICES, default='Standard')
    
    # Calculation Method choices
    METHOD_CHOICES = [
        ('ISNA', 'Islamic Society of North America (ISNA)'),
        ('MWL', 'Muslim World League (MWL)'),
        ('Egyptian', 'Egyptian General Authority of Survey'),
        ('UmmAlQura', 'Umm al-Qura University, Makkah'),
    ]
    calculation_method = models.TextField(choices=METHOD_CHOICES, default='ISNA')
    
    notification_preference = models.BooleanField(default=True)
    display_language = models.TextField(default='English')

    def __str__(self):
        '''Return a string representation of this Profile.'''
        return f"Profile for {self.user.username}"

class HijriCalendar(models.Model):
    '''Maps Gregorian dates to Hijri dates and Islamic holidays.'''
    date = models.DateField(unique=True)
    hijri_day = models.IntegerField()
    hijri_month = models.TextField()
    hijri_year = models.IntegerField()
    holiday_name = models.TextField(blank=True)

    def __str__(self):
        '''Return a string representation of this Hijri date.'''
        return f"{self.hijri_day} {self.hijri_month} {self.hijri_year} ({self.date})"

class SavedCity(models.Model):
    '''Tracks which cities a user has saved, with prayer times fetched via the Aladhan API.'''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='saved_cities')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='saved_by')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['profile', 'city']

    def __str__(self):
        '''Return a string representation of this SavedCity.'''
        return f"{self.profile.user.username} → {self.city.name}"
