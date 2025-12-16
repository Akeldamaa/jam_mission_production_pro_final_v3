"""
Django settings for the JAM Mission project.

The settings here are configured for development by default.  For
production deployment you should set `DEBUG = False`, configure a
secure `SECRET_KEY` via environment variables, and set appropriate
`ALLOWED_HOSTS`.  Email settings are also configurable via
environment variables.
"""
from __future__ import annotations

import os
from pathlib import Path

# Base directory of the project (e.g. /path/to/jam_mission_production/backend)
BASE_DIR: Path = Path(__file__).resolve().parent.parent


# -----------------------------------------------------------------------------
# General configuration
# -----------------------------------------------------------------------------

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY: str = os.environ.get('DJANGO_SECRET_KEY', 'replace-me-with-a-secure-random-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG: bool = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

# Allow all hosts by default; override in production via environment variable
ALLOWED_HOSTS: list[str] = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')


# -----------------------------------------------------------------------------
# Application definition
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Local apps
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'jammission.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'core' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'jammission.wsgi.application'


# -----------------------------------------------------------------------------
# Database configuration
# -----------------------------------------------------------------------------
# We use SQLite for simplicity.  Override these settings for production (e.g.
# PostgreSQL) via environment variables.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# -----------------------------------------------------------------------------
# Password validation
# -----------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# -----------------------------------------------------------------------------
# Internationalization
# -----------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_TZ = True


# -----------------------------------------------------------------------------
# Static and media files
# -----------------------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'core' / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# -----------------------------------------------------------------------------
# Email configuration
# -----------------------------------------------------------------------------
# Default email settings use the console backend for development.  You can set
# DJANGO_EMAIL_BACKEND to override this (e.g. smtp.EmailBackend).
EMAIL_BACKEND = os.environ.get('DJANGO_EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.environ.get('DJANGO_EMAIL_HOST', '')
EMAIL_PORT = int(os.environ.get('DJANGO_EMAIL_PORT', 587))
EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_PASSWORD', '')
EMAIL_USE_TLS = os.environ.get('DJANGO_EMAIL_USE_TLS', 'True') == 'True'
EMAIL_USE_SSL = os.environ.get('DJANGO_EMAIL_USE_SSL', 'False') == 'True'
# Set a sensible default from email for sending notifications.  Owners can
# override this in production via the DJANGO_DEFAULT_FROM_EMAIL environment
# variable.  Use the official JAM Mission email for public contact.
DEFAULT_FROM_EMAIL = os.environ.get('DJANGO_DEFAULT_FROM_EMAIL', 'thejammission@gmail.com')

# Comma separated emails of owners who should receive notifications (e.g. for bookings and contact messages)
NOTIFICATION_EMAILS = [email.strip() for email in os.environ.get('DJANGO_NOTIFICATION_EMAILS', '').split(',') if email.strip()]


# -----------------------------------------------------------------------------
# Logging configuration (optional; prints to console)
# -----------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
