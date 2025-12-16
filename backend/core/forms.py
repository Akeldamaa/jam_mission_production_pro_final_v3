"""
Forms for the JAM Mission project.

This module defines Django ModelForms for the various models defined in
`core.models`, providing a convenient way to validate and process user
input from HTML forms.  Widgets are customised to provide basic styling
consistent with the site's UI.
"""
from __future__ import annotations

from django import forms
from .models import (
    BlogPost,
    Booking,
    ContactMessage,
    PreQualificationApplication,
    Event,
    Service,
    Product,
    Order,
    NewsletterSubscriber,
)


class BlogForm(forms.ModelForm):
    """Form for creating or editing blog posts."""

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'cover']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input'}),
            'content': forms.Textarea(attrs={'class': 'input', 'rows': 10}),
            'cover': forms.ClearableFileInput(attrs={'class': 'input'}),
        }


class BookingForm(forms.ModelForm):
    """Form for requesting a stay booking or event tickets."""

    class Meta:
        model = Booking
        fields = ['name', 'email', 'date', 'tickets', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.EmailInput(attrs={'class': 'input'}),
            'date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'tickets': forms.NumberInput(attrs={'class': 'input', 'min': 1}),
            'notes': forms.Textarea(attrs={'class': 'input', 'rows': 4, 'placeholder': 'Any special requests?'}),
        }


class ContactForm(forms.ModelForm):
    """Form for sending a message via the contact page."""

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.EmailInput(attrs={'class': 'input'}),
            'subject': forms.TextInput(attrs={'class': 'input'}),
            'message': forms.Textarea(attrs={'class': 'input', 'rows': 6}),
        }


class PreQualificationForm(forms.ModelForm):
    """Form for completing the lease pre‑qualification application."""

    class Meta:
        model = PreQualificationApplication
        exclude = ['created_at', 'status']
        widgets = {
            'criminal_record': forms.Textarea(attrs={'class': 'input', 'rows': 3}),
            'probation_warrants': forms.Textarea(attrs={'class': 'input', 'rows': 3}),
            'smoking_drugs': forms.Textarea(attrs={'class': 'input', 'rows': 2}),
            'alcohol_use': forms.Textarea(attrs={'class': 'input', 'rows': 2}),
            'threats_history': forms.Textarea(attrs={'class': 'input', 'rows': 2}),
            'additional_structures': forms.Textarea(attrs={'class': 'input', 'rows': 2}),
            'vehicles_condition': forms.TextInput(attrs={'class': 'input'}),
            'children_ages': forms.TextInput(attrs={'class': 'input'}),
            'personal_garden': forms.TextInput(attrs={'class': 'input'}),
            'livestock': forms.Textarea(attrs={'class': 'input', 'rows': 2}),
            'pets': forms.Textarea(attrs={'class': 'input', 'rows': 2}),
            'fencing': forms.Textarea(attrs={'class': 'input', 'rows': 2}),
            'membership_plans': forms.TextInput(attrs={'class': 'input'}),
            'boondock_plan': forms.Textarea(attrs={'class': 'input', 'rows': 2}),
            'monthly_support': forms.TextInput(attrs={'class': 'input'}),
            'work_exchange_months': forms.TextInput(attrs={'class': 'input'}),
            'work_days_hours': forms.TextInput(attrs={'class': 'input'}),
            'work_start': forms.TextInput(attrs={'class': 'input'}),
            'deposit': forms.TextInput(attrs={'class': 'input'}),
            'contribution_area': forms.Textarea(attrs={'class': 'input', 'rows': 3}),
            'skills_talents': forms.Textarea(attrs={'class': 'input', 'rows': 3}),
        }


class EventForm(forms.ModelForm):
    """Form for creating or editing events by owners."""

    class Meta:
        model = Event
        # Exclude slug from the public form; it will be auto‑generated
        fields = [
            'title',
            'short_tagline',
            'start_date',
            'end_date',
            'price',
            'capacity',
            'description',
            'image',
            'is_active',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input'}),
            'short_tagline': forms.TextInput(attrs={'class': 'input'}),
            'start_date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'price': forms.NumberInput(attrs={'class': 'input', 'step': '0.01'}),
            'capacity': forms.NumberInput(attrs={'class': 'input', 'min': 0}),
            'description': forms.Textarea(attrs={'class': 'input', 'rows': 6}),
            'image': forms.ClearableFileInput(attrs={'class': 'input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'input'}),
        }


class ServiceForm(forms.ModelForm):
    """Form for creating or editing services by owners."""

    class Meta:
        model = Service
        # Exclude slug from public form; auto‑generated
        fields = ['name', 'description', 'price', 'image', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.Textarea(attrs={'class': 'input', 'rows': 6}),
            'price': forms.NumberInput(attrs={'class': 'input', 'step': '0.01'}),
            'image': forms.ClearableFileInput(attrs={'class': 'input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'input'}),
        }


class ProductForm(forms.ModelForm):
    """Form for creating or editing products by owners."""

    class Meta:
        model = Product
        # Exclude slug from public form; auto‑generated
        fields = ['name', 'description', 'price', 'image', 'in_stock']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.Textarea(attrs={'class': 'input', 'rows': 6}),
            'price': forms.NumberInput(attrs={'class': 'input', 'step': '0.01'}),
            'image': forms.ClearableFileInput(attrs={'class': 'input'}),
            'in_stock': forms.CheckboxInput(attrs={'class': 'input'}),
        }


class OrderForm(forms.ModelForm):
    """Form used by visitors to place an order for a product."""

    class Meta:
        model = Order
        fields = ['name', 'email', 'quantity', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.EmailInput(attrs={'class': 'input'}),
            'quantity': forms.NumberInput(attrs={'class': 'input', 'min': 1}),
            'notes': forms.Textarea(attrs={'class': 'input', 'rows': 4, 'placeholder': 'Any special requests?'}),
        }


class NewsletterForm(forms.ModelForm):
    """Simple form for newsletter signup."""

    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'Your email'}),
        }