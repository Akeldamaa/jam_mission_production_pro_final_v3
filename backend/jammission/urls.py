"""
Root URL configuration for the JAM Mission project.

All URL patterns for the public site, booking, events, contact, and
application are delegated to the `core` application.  Static and media
files are served directly in development when `DEBUG` is enabled.
"""
from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Delegate remaining routes to the core app
]

if settings.DEBUG:
    # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
