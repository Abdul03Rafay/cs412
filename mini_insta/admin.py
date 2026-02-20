# File: mini_insta/admin.py
# Author: Abdul Rafay (rafaya@bu.edu), 2/13/2026 - 2/20/2026.
# Description: Python file to register relvant models with the admin.

from django.contrib import admin

# Register your models here.
from .models import Profile, Post, Photo
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)