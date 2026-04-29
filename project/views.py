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
from django.http import JsonResponse
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

        context['cities_json']    = json.dumps(cities_data)
        context['home_city_pk']   = profile.city.pk if profile.city else None
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
        '''Include saved cities and today's home-city prayer times in the profile context.'''
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['saved_cities'] = (
            SavedCity.objects.filter(profile=profile)
            .select_related('city')
            .order_by('-date_added')
        )
        if profile.city:
            context['home_prayer_times'] = PrayerTime.objects.filter(
                city=profile.city, date=datetime.date.today()
            ).first()
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


class HijriCalendarListView(LoginRequiredMixin, TemplateView):
    '''Interactive Hijri calendar: horizontally-scrollable date strip with a prayer time
    card that updates when the user changes the date or selected city.'''
    template_name = 'project/hijricalendar_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, _ = Profile.objects.get_or_create(user=self.request.user)

        today = datetime.date.today()
        start = today - datetime.timedelta(days=45)
        end   = today + datetime.timedelta(days=45)

        # Build Hijri lookup from DB cache
        hijri_map = {
            hc.date.isoformat(): {
                'hijri_day':    hc.hijri_day,
                'hijri_month':  hc.hijri_month,
                'hijri_year':   hc.hijri_year,
                'holiday_name': hc.holiday_name,
            }
            for hc in HijriCalendar.objects.filter(date__gte=start, date__lte=end)
        }

        # 91-day date list for the strip
        dates = []
        d = start
        while d <= end:
            iso = d.isoformat()
            h = hijri_map.get(iso, {})
            dates.append({
                'gregorian':    iso,
                'hijri_day':    h.get('hijri_day', ''),
                'hijri_month':  h.get('hijri_month', ''),
                'hijri_year':   h.get('hijri_year', ''),
                'holiday_name': h.get('holiday_name', ''),
                'is_today':     d == today,
            })
            d += datetime.timedelta(days=1)

        # Saved cities for city filter
        saved = list(SavedCity.objects.filter(profile=profile).select_related('city'))
        cities = [{'pk': sc.city.pk, 'name': sc.city.name} for sc in saved]
        city_pks = [sc.city.pk for sc in saved]

        # Prayer times for all saved cities in the date window
        prayer_times = {}
        for pt in PrayerTime.objects.filter(city__in=city_pks, date__gte=start, date__lte=end):
            key = f"{pt.city_id}_{pt.date.isoformat()}"
            prayer_times[key] = {
                'fajr':    pt.fajr.strftime('%H:%M'),
                'sunrise': pt.sunrise.strftime('%H:%M'),
                'zuhr':    pt.zuhr.strftime('%H:%M'),
                'asr':     pt.asr.strftime('%H:%M'),
                'maghrib': pt.maghrib.strftime('%H:%M'),
                'isha':    pt.isha.strftime('%H:%M'),
            }

        context['today']             = today.isoformat()
        context['dates_json']        = json.dumps(dates)
        context['cities_json']       = json.dumps(cities)
        context['prayer_times_json'] = json.dumps(prayer_times)
        return context


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
    '''Merged Cities page: shows the user's saved cities and lets them add a new one.
    On POST, geocodes the city via the Nominatim (OpenStreetMap) API for accurate
    coordinates, then calls the Aladhan timings API using those coordinates to retrieve
    timezone and today's prayer times. Creates City, SavedCity, and PrayerTime records
    as needed, then redirects to the map. Uses update_or_create so any city previously
    stored with inaccurate coordinates is corrected on re-add.'''
    error = None
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        city_query = request.POST.get('city_query', '').strip()
        # Split "City, Country" on the last comma — handles names like "St. Louis, United States"
        parts = city_query.rsplit(', ', 1)
        city_name = parts[0].strip()
        country = parts[1].strip() if len(parts) > 1 else ''

        if not city_name:
            error = 'Please select or enter a city.'
        else:
            today = datetime.date.today()
            date_str = today.strftime('%d-%m-%Y')
            method = ALADHAN_METHOD.get(profile.calculation_method, 2)
            school = ALADHAN_SCHOOL.get(profile.madhab, 0)

            try:
                # Step 1: Geocode with Nominatim for accurate coordinates
                geo_query = f"{city_name}, {country}" if country else city_name
                geo_params = urllib.parse.urlencode({'q': geo_query, 'format': 'json', 'limit': 1})
                geo_req = urllib.request.Request(
                    f"https://nominatim.openstreetmap.org/search?{geo_params}",
                    headers={'User-Agent': 'Muezzin-CS412/1.0 rafaya@bu.edu'},
                )
                with urllib.request.urlopen(geo_req, timeout=10) as response:
                    geo_data = json.loads(response.read().decode())

                if not geo_data:
                    error = f"City '{city_query}' was not found. Try a different spelling or city name."
                else:
                    lat = float(geo_data[0]['lat'])
                    lon = float(geo_data[0]['lon'])

                    # Step 2: Fetch prayer times from Aladhan using the accurate coordinates
                    aladhan_url = (
                        f"https://api.aladhan.com/v1/timings/{date_str}"
                        f"?latitude={lat}&longitude={lon}"
                        f"&method={method}&school={school}"
                    )
                    with urllib.request.urlopen(aladhan_url, timeout=10) as response:
                        data = json.loads(response.read().decode())

                    if data.get('code') == 200:
                        timings = data['data']['timings']
                        meta    = data['data']['meta']
                        def clean(t): return t.split(' ')[0]

                        city_obj, _ = City.objects.update_or_create(
                            name=city_name,
                            defaults={
                                'latitude':  lat,
                                'longitude': lon,
                                'timezone':  meta['timezone'],
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
                        error = 'Could not fetch prayer times. Please try again.'

            except Exception:
                error = 'Could not connect to location services. Please try again.'

    saved_cities = SavedCity.objects.filter(profile=profile).select_related('city').order_by('-date_added')
    return render(request, 'project/add_city.html', {
        'world_cities': WORLD_CITIES,
        'error': error,
        'saved_cities': saved_cities,
    })


@login_required
def fetch_prayer_times_api(request):
    '''AJAX endpoint: return prayer times for a city + date, fetching from Aladhan if not cached.
    GET params: city (pk), date (YYYY-MM-DD).
    Returns JSON {ok, fajr, zuhr, asr, maghrib, isha} or {ok: false, error}.'''
    city_pk  = request.GET.get('city', '').strip()
    date_str = request.GET.get('date', '').strip()

    try:
        target_date = datetime.date.fromisoformat(date_str)
        city_pk_int = int(city_pk)
    except (ValueError, TypeError):
        return JsonResponse({'ok': False, 'error': 'Invalid parameters.'})

    city = City.objects.filter(pk=city_pk_int).first()
    if not city:
        return JsonResponse({'ok': False, 'error': 'City not found.'})

    # Get times — from cache or fresh from Aladhan
    pt = PrayerTime.objects.filter(city=city, date=target_date).first()
    if pt:
        times = {
            'fajr':    pt.fajr.strftime('%H:%M'),
            'sunrise': pt.sunrise.strftime('%H:%M'),
            'zuhr':    pt.zuhr.strftime('%H:%M'),
            'asr':     pt.asr.strftime('%H:%M'),
            'maghrib': pt.maghrib.strftime('%H:%M'),
            'isha':    pt.isha.strftime('%H:%M'),
        }
    else:
        profile, _ = Profile.objects.get_or_create(user=request.user)
        method = ALADHAN_METHOD.get(profile.calculation_method, 2)
        school = ALADHAN_SCHOOL.get(profile.madhab, 0)
        api_date = target_date.strftime('%d-%m-%Y')
        url = (
            f"https://api.aladhan.com/v1/timings/{api_date}"
            f"?latitude={city.latitude}&longitude={city.longitude}"
            f"&method={method}&school={school}"
        )
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())
            timings = data['data']['timings']
            def clean(t): return t.split(' ')[0]

            times = {
                'fajr':    clean(timings['Fajr']),
                'sunrise': clean(timings['Sunrise']),
                'zuhr':    clean(timings['Dhuhr']),
                'asr':     clean(timings['Asr']),
                'maghrib': clean(timings['Maghrib']),
                'isha':    clean(timings['Isha']),
            }

            try:
                h = data['data']['date']['hijri']
                HijriCalendar.objects.get_or_create(
                    date=target_date,
                    defaults={
                        'hijri_day':   int(h['day']),
                        'hijri_month': h['month']['en'],
                        'hijri_year':  int(h['year']),
                        'holiday_name': '',
                    }
                )
            except Exception:
                pass

            PrayerTime.objects.create(city=city, date=target_date, **times)
        except Exception:
            return JsonResponse({'ok': False, 'error': 'Could not reach the prayer times service.'})

    # Always include Hijri date if cached (covers both paths)
    hijri = {}
    hc = HijriCalendar.objects.filter(date=target_date).first()
    if hc:
        hijri = {
            'hijri_day':    hc.hijri_day,
            'hijri_month':  hc.hijri_month,
            'hijri_year':   hc.hijri_year,
            'holiday_name': hc.holiday_name,
        }

    return JsonResponse({'ok': True, **times, **hijri})


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
