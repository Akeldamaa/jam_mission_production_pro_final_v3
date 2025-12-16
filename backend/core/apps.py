"""
App configuration for the core app of JAM Mission.

This app contains the models, views, templates, and other resources
for the public website, booking system, blog CMS, and contact/application
forms.
"""
from __future__ import annotations

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'