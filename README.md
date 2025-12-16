# JAM Mission – Full Production Version

This repository contains a complete Django web application for the JAM Mission project.  It is designed to be ready for deployment on common cloud platforms (Render, DigitalOcean App Platform, Vercel, Heroku, etc.) or on your own server.  The app provides a polished public website with a booking system, dynamic events, blog CMS, contact form, and lease pre‑qualification application.  It also separates technical and owner administration via Django's built–in authentication and custom dashboards.

## Features

- **Landing page** with mission statement, links to services, stays, gardens, products, events, blog, booking and contact.
- **Admin portal** for full site management.
- **Owner dashboard** to manage blog posts, bookings and event tickets without full admin access.
- **Events**: create events with date, price, capacity, description and images; visitors can view and request tickets.
- **Blog CMS**: owners can post announcements with images; public can browse posts.
- **Booking engine** for camp/RV stays and event tickets; owners can confirm/reject/mark paid.
- **Contact page** with form that stores messages and optionally emails owners.
- **Lease Pre‑Qualification form** to collect prospective tenant information.
- **Responsive design** built with Tailwind CSS, Google Fonts, a custom colour palette and simple cards.

## Running Locally

1.  Ensure you have Python 3.11 or later installed.  Create and activate a virtualenv:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3.  Apply migrations and create a superuser:

    ```bash
    cd backend
    python manage.py migrate
    python manage.py createsuperuser
    ```

4.  Run the development server:

    ```bash
    python manage.py runserver
    ```

5.  Visit `http://127.0.0.1:8000/` in your browser.  Log in at `/login/` to access owner/technical dashboards or `/admin/` for full admin access.

## Deployment Notes

- Before deploying, set `DEBUG = False` and configure `ALLOWED_HOSTS` in `backend/jammission/settings.py`.
- Set a secure `SECRET_KEY` as an environment variable (`DJANGO_SECRET_KEY`).
- Configure email by setting `DJANGO_EMAIL_HOST`, `DJANGO_EMAIL_PORT`, `DJANGO_EMAIL_USER`, `DJANGO_EMAIL_PASSWORD`, `DJANGO_EMAIL_USE_TLS`/`DJANGO_EMAIL_USE_SSL`, `DJANGO_DEFAULT_FROM_EMAIL`, and `DJANGO_NOTIFICATION_EMAILS` environment variables.
- Run `python manage.py collectstatic` to collect static assets for production.
