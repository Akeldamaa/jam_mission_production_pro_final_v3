"""
Admin configuration for the core app.

This module registers the core models with the Django admin site and
customises the list views for easier management.
"""
from __future__ import annotations

from django.contrib import admin
from .models import (
    BlogPost,
    Booking,
    Event,
    ContactMessage,
    PreQualificationApplication,
    Service,
    Product,
    Order,
    NewsletterSubscriber,
)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')
    list_filter = ('created',)
    search_fields = ('title', 'content')
    date_hierarchy = 'created'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'price', 'capacity', 'is_active')
    list_filter = ('is_active', 'start_date')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date', 'event', 'tickets', 'status', 'created')
    list_filter = ('status', 'date', 'event')
    search_fields = ('name', 'email', 'notes')
    readonly_fields = ('created',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'handled')
    list_filter = ('handled', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)


@admin.register(PreQualificationApplication)
class PreQualificationApplicationAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'status', 'adults', 'children')
    list_filter = ('status', 'created_at')
    readonly_fields = ('created_at',)
    search_fields = ('criminal_record', 'skills_talents')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active')
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'in_stock')
    list_filter = ('in_stock',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('created', 'product', 'name', 'email', 'quantity', 'status')
    list_filter = ('status', 'created', 'product')
    search_fields = ('name', 'email', 'product__name')
    readonly_fields = ('created',)


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)
    readonly_fields = ('created_at',)