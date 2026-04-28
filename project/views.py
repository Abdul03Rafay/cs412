# File: project/views.py
# Author: Abdul Rafay (rafaya@bu.edu), 4/21/2026
# Description: Implements views for the Prayer Times application using generic
#              class-based views and function-based views where appropriate.

from django.views.generic import ListView, DetailView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from .models import City, PrayerTime, Profile, HijriCalendar, SavedCity
from .forms import ProfileForm
from .world_cities import WORLD_CITIES
import datetime
import urllib.request
import urllib.parse
import json

# Aladhan API parameter mappings
ALADHAN_METHOD = {'ISNA': 2, 'MWL': 3, 'Egyptian': 5, 'UmmAlQura': 4}
ALADHAN_SCHOOL = {'Standard': 0, 'Hanafi': 1}


def fetch_prayer_times_from_api(city, method_key, school_key):
    '''Fetch today's prayer times from the Aladhan API for a given city.
    Uses the city's latitude/longitude and the user's calculation method and madhab.
    Returns a dict of prayer name → time string, or None on failure.'''
    today = datetime.date.today()
    date_str = today.strftime('%d-%m-%Y')
    method = ALADHAN_METHOD.get(method_key, 2)
    school = ALADHAN_SCHOOL.get(school_key, 0)
    url = (
        f"https://api.aladhan.com/v1/timings/{date_str}"
        f"?latitude={city.latitude}&longitude={city.longitude}"
        f"&method={method}&school={school}"
    )
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
        timings = data['data']['timings']
        # Strip any timezone suffix (e.g. "05:43 (EST)" → "05:43")
        def clean(t): return t.split(' ')[0]
        return {
            'date': today,
            'fajr': clean(timings['Fajr']),
            'sunrise': clean(timings['Sunrise']),
            'zuhr': clean(timings['Dhuhr']),
            'asr': clean(timings['Asr']),
            'maghrib': clean(timings['Maghrib']),
            'isha': clean(timings['Isha']),
        }
    except Exception:
        return None


class MapView(LoginRequiredMixin, TemplateView):
    '''Main landing page after login. Displays a map with the user's saved cities
    and today's prayer times shown as hover cards on each pin.'''
    template_name = 'project/map.html'

    def get_context_data(self, **kwargs):
        '''Build JSON-serializable city data including today's prayer times for each saved city.'''
        context = super().get_context_data(**kwargs)
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        saved = SavedCity.objects.filter(profile=profile).select_related('city')

        today = datetime.date.today()
        cities_data = []
        for sc in saved:
            city = sc.city
            pt = PrayerTime.objects.filter(city=city, date=today).first()
            cities_data.append({
                'name': city.name,
                'lat': city.latitude,
                'lon': city.longitude,
                'pk': city.pk,
                'prayer_times': {
                    'fajr': pt.fajr.strftime('%H:%M'),
                    'zuhr': pt.zuhr.strftime('%H:%M'),
                    'asr': pt.asr.strftime('%H:%M'),
                    'maghrib': pt.maghrib.strftime('%H:%M'),
                    'isha': pt.isha.strftime('%H:%M'),
                } if pt else None,
            })

        context['cities_json'] = json.dumps(cities_data)
        context['today'] = today
        return context


class CityListView(LoginRequiredMixin, ListView):
    '''View to list all cities, supporting search functionality.'''
    template_name = 'project/city_list.html'
    model = City
    context_object_name = 'cities'

    def get_queryset(self):
        '''Filter cities based on search query if provided.'''
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query))
        return queryset

    def get_context_data(self, **kwargs):
        '''Pass the set of saved city PKs for the logged-in user.'''
        context = super().get_context_data(**kwargs)
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        context['saved_city_ids'] = set(
            SavedCity.objects.filter(profile=profile).values_list('city_id', flat=True)
        )
        return context


class CityDetailView(LoginRequiredMixin, DetailView):
    '''View to show details for a specific city, including prayer times.'''
    template_name = 'project/city_detail.html'
    model = City
    context_object_name = 'city'

    def get_context_data(self, **kwargs):
        '''Include filtered prayer times, today's date, and saved status in context.'''
        context = super().get_context_data(**kwargs)
        city = self.get_object()

        prayer_times = PrayerTime.objects.filter(city=city)

        date_query = self.request.GET.get('date')
        if date_query:
            try:
                filter_date = datetime.datetime.strptime(date_query, '%Y-%m-%d').date()
                prayer_times = prayer_times.filter(date=filter_date)
            except ValueError:
                pass
        context['prayer_times'] = prayer_times.order_by('date')

        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        context['is_saved'] = SavedCity.objects.filter(profile=profile, city=city).exists()
        return context


class ProfileDetailView(LoginRequiredMixin, DetailView):
    '''View to show the profile settings and saved cities for the logged-in user.'''
    template_name = 'project/profile_detail.html'
    model = Profile
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        '''Return the profile associated with the current user.'''
        return Profile.objects.get_or_create(user=self.request.user)[0]

    def get_context_data(self, **kwargs):
        '''Include saved cities in the profile context.'''
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['saved_cities'] = (
            SavedCity.objects.filter(profile=profile)
            .select_related('city')
            .order_by('-date_added')
        )
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    '''View to update the profile settings for the logged-in user.'''
    template_name = 'project/profile_form.html'
    model = Profile
    form_class = ProfileForm

    def get_object(self, queryset=None):
        '''Return the profile associated with the current user.'''
        return Profile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        '''Redirect to the profile detail page after a successful update.'''
        return reverse('profile_detail')


class HijriCalendarListView(LoginRequiredMixin, ListView):
    '''View to list Hijri calendar mappings and Islamic holidays.'''
    template_name = 'project/hijricalendar_list.html'
    model = HijriCalendar
    context_object_name = 'calendar_entries'
    ordering = ['date']


@login_required
def save_city(request, pk):
    '''Save a city to the user's saved list and fetch today's prayer times from the Aladhan API.
    Creates a SavedCity record and a PrayerTime record for today if one does not already exist.
    Redirects back to the city detail page.'''
    if request.method == 'POST':
        city = get_object_or_404(City, pk=pk)
        profile, _ = Profile.objects.get_or_create(user=request.user)
        SavedCity.objects.get_or_create(profile=profile, city=city)

        today = datetime.date.today()
        if not PrayerTime.objects.filter(city=city, date=today).exists():
            times = fetch_prayer_times_from_api(city, profile.calculation_method, profile.madhab)
            if times:
                PrayerTime.objects.create(
                    city=city,
                    date=times['date'],
                    fajr=times['fajr'],
                    sunrise=times['sunrise'],
                    zuhr=times['zuhr'],
                    asr=times['asr'],
                    maghrib=times['maghrib'],
                    isha=times['isha'],
                )
    return redirect('city_detail', pk=pk)


@login_required
def unsave_city(request, pk):
    '''Remove a city from the user's saved list.
    Deletes the SavedCity record for the current user and city.
    Supports an optional "next" POST parameter to redirect after deletion.'''
    if request.method == 'POST':
        city = get_object_or_404(City, pk=pk)
        profile, _ = Profile.objects.get_or_create(user=request.user)
        SavedCity.objects.filter(profile=profile, city=city).delete()
        next_url = request.POST.get('next', '')
        if next_url:
            return redirect(next_url)
    return redirect('city_detail', pk=pk)


@login_required
def add_city(request):
    '''Display a searchable list of world cities and add the selected one to the user's saved list.
    On POST, calls the Aladhan timingsByCity API with the city name and country to retrieve
    coordinates, timezone, and today's prayer times. Creates City, SavedCity, and PrayerTime
    records as needed, then redirects to the map.'''
    error = None

    if request.method == 'POST':
        city_query = request.POST.get('city_query', '').strip()
        # Split "City, Country" on the last comma — handles names like "St. Louis, United States"
        parts = city_query.rsplit(', ', 1)
        city_name = parts[0].strip()
        country = parts[1].strip() if len(parts) > 1 else ''

        if not city_name:
            error = 'Please select or enter a city.'
        else:
            profile, _ = Profile.objects.get_or_create(user=request.user)
            today = datetime.date.today()
            date_str = today.strftime('%d-%m-%Y')
            method = ALADHAN_METHOD.get(profile.calculation_method, 2)
            school = ALADHAN_SCHOOL.get(profile.madhab, 0)

            params = {'city': city_name, 'method': method, 'school': school}
            if country:
                params['country'] = country
            query_string = urllib.parse.urlencode(params)
            url = f"https://api.aladhan.com/v1/timingsByCity/{date_str}?{query_string}"

            try:
                with urllib.request.urlopen(url, timeout=10) as response:
                    data = json.loads(response.read().decode())

                if data.get('code') == 200:
                    timings = data['data']['timings']
                    meta = data['data']['meta']
                    def clean(t): return t.split(' ')[0]

                    # Use the display name from the input; look up by name to avoid duplicates
                    city_obj, _ = City.objects.get_or_create(
                        name=city_name,
                        defaults={
                            'latitude': meta['latitude'],
                            'longitude': meta['longitude'],
                            'timezone': meta['timezone'],
                        }
                    )

                    SavedCity.objects.get_or_create(profile=profile, city=city_obj)

                    if not PrayerTime.objects.filter(city=city_obj, date=today).exists():
                        PrayerTime.objects.create(
                            city=city_obj,
                            date=today,
                            fajr=clean(timings['Fajr']),
                            sunrise=clean(timings['Sunrise']),
                            zuhr=clean(timings['Dhuhr']),
                            asr=clean(timings['Asr']),
                            maghrib=clean(timings['Maghrib']),
                            isha=clean(timings['Isha']),
                        )

                    return redirect('map')
                else:
                    error = f"City '{city_query}' was not found. Try a different spelling or city name."

            except Exception:
                error = 'Could not connect to the prayer times service. Please try again.'

    return render(request, 'project/add_city.html', {
        'world_cities': WORLD_CITIES,
        'error': error,
    })


def register(request):
    '''Register a new user account, create their Profile, log them in, and redirect to the map.
    Uses Django's built-in UserCreationForm for validation.'''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('map')
    else:
        form = UserCreationForm()
    return render(request, 'project/register.html', {'form': form})
