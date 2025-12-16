"""
WSGI config for the JAM Mission project.

This module exposes the WSGI callable as a module-level variable named
``application``.  It is used by Django's development server and by
WSGI servers in production deployments.
"""

from __future__ import annotations

import os

from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'django' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jammission.settings')

# Create the WSGI application.
application = get_wsgi_application()
