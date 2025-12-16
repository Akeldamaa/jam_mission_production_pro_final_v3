"""
URL patterns for the core app of JAM Mission.

These routes map to view functions that render pages, handle bookings,
blog posts, events, contact and application forms, and dashboards.  Use
named URLs throughout templates for reliable linking.
"""
from __future__ import annotations

from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services_page, name='services'),
    path('stays/', views.booking, name='stays'),  # Stays page uses booking form
    path('gardens/', views.services_page, name='gardens'),  # Placeholder (reuse services page)
    path('events/', views.events_page, name='events'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    # Owner management for events
    path('owner/events/new/', views.event_create, name='event_create'),
    path('owner/events/<slug:slug>/edit/', views.event_edit, name='event_edit'),
    path('products/', views.products_page, name='products'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/add/<slug:slug>/', views.cart_add, name='cart_add'),
    path('cart/', views.cart_view, name='cart'),
    # Owner management for products
    path('owner/products/new/', views.product_create, name='product_create'),
    path('owner/products/<slug:slug>/edit/', views.product_edit, name='product_edit'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:id>/', views.blog_detail, name='blog_detail'),
    path('blog/new/', views.blog_edit, name='blog_new'),
    path('blog/<int:id>/edit/', views.blog_edit, name='blog_edit'),
    path('booking/', views.booking, name='booking'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('tech/', views.tech_dashboard, name='tech_dashboard'),
    path('owner/', views.owner_dashboard, name='owner_dashboard'),
    # Owner management for services
    path('owner/services/new/', views.service_create, name='service_create'),
    path('owner/services/<slug:slug>/edit/', views.service_edit, name='service_edit'),
    path('contact/', views.contact, name='contact'),
    path('apply/', views.prequalification, name='prequalification'),
    path('faq/', views.faq, name='faq'),
    path('subscribe/', views.newsletter_subscribe, name='subscribe'),
]