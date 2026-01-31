## File for URLs.

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path(r'', views.quote, name="quote"),
    path(r'about', views.about, name="about"),
    path(r'show_all', views.show_all, name="show_all"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)