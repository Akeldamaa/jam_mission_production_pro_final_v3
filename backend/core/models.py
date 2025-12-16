"""
Database models for the JAM Mission project.

The models defined here represent blog posts, bookings, events, messages
submitted via the contact form, applications for lease pre‑qualification,
services and products offered by JAM Mission.  They provide simple
fields appropriate for this project and can be extended as needed.
"""
from __future__ import annotations

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver

def _unique_slugify(instance, value, slug_field_name='slug'):
    """
    Generate a unique slug for a given model instance.

    This helper will create a slug from ``value`` and ensure that the slug
    is unique within the model's table.  If a conflict exists, a suffix
    ``-1``, ``-2``, etc. will be appended until the slug is unique.

    The generated slug is assigned to ``instance.slug`` but not saved
    automatically.  The slug field name can be customised with
    ``slug_field_name`` if a different attribute name is used.
    """
    slug_base = slugify(value)
    slug = slug_base
    Model = instance.__class__
    counter = 1
    # When updating an existing object, exclude its own PK from the lookup
    pk = instance.pk
    # Keep looping until a unique slug is found
    while Model.objects.filter(**{slug_field_name: slug}).exclude(pk=pk).exists():
        slug = f"{slug_base}-{counter}"
        counter += 1
    setattr(instance, slug_field_name, slug)


class BlogPost(models.Model):
    """A blog or announcement post with optional cover image."""

    title = models.CharField(max_length=200)
    content = models.TextField()
    cover = models.ImageField(upload_to='blog/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Event(models.Model):
    """Represents an event that visitors can book tickets for."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_tagline = models.CharField(max_length=255, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.PositiveIntegerField(default=0)
    description = models.TextField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['start_date', 'title']

    def __str__(self) -> str:
        return self.title

    @property
    def tickets_sold(self) -> int:
        """Return the number of confirmed or paid bookings for this event."""
        return sum(b.tickets for b in self.eventbookings.filter(status__in=['confirmed', 'paid']))

    @property
    def available_tickets(self) -> int:
        """Return the number of tickets remaining."""
        return max(self.capacity - self.tickets_sold, 0)


class Booking(models.Model):
    """A booking request for a stay or event tickets."""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    date = models.DateField(help_text='Date for your stay or booking')
    tickets = models.PositiveIntegerField(default=1, help_text='Number of tickets (for events)')
    event = models.ForeignKey(Event, related_name='eventbookings', blank=True, null=True, on_delete=models.SET_NULL)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self) -> str:
        if self.event:
            return f"{self.name} – {self.event.title} ({self.tickets} tickets)"
        return f"{self.name} – Stay on {self.date}"


class ContactMessage(models.Model):
    """Messages submitted via the contact form."""

    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    handled = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.name} – {self.subject or 'Contact message'}"


class PreQualificationApplication(models.Model):
    """Application form for JAM Mission lease pre‑qualification."""

    # 1. Identification: front and back of ID for all adults
    id_front = models.ImageField(upload_to='applications/ids/', blank=True, null=True)
    id_back = models.ImageField(upload_to='applications/ids/', blank=True, null=True)

    # 2. Personal History
    criminal_record = models.TextField(blank=True, help_text='Criminal record details')
    probation_warrants = models.TextField(blank=True, help_text='Probation status or outstanding warrants')
    smoking_drugs = models.TextField(blank=True, help_text='Smoking or recreational drug use')
    alcohol_use = models.TextField(blank=True, help_text='Alcohol use behaviour')
    threats_history = models.TextField(blank=True, help_text='Former partners with threats/violence')

    # 3. Lease term
    lease_term = models.CharField(max_length=100, blank=True)

    # 4. Housing structure
    housing_size = models.CharField(max_length=255, blank=True)
    housing_foundation = models.CharField(max_length=255, blank=True)

    # 5. Additional structures
    additional_structures = models.TextField(blank=True)

    # 6. Vehicles
    num_vehicles = models.PositiveIntegerField(default=0)
    vehicles_condition = models.CharField(max_length=255, blank=True)

    # 7. Household members
    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)
    children_ages = models.CharField(max_length=255, blank=True)

    # 8. Gardening
    personal_garden = models.CharField(max_length=255, blank=True)

    # 9. Livestock
    livestock = models.TextField(blank=True)

    # 10. Pets
    pets = models.TextField(blank=True)

    # 11. Fencing
    fencing = models.TextField(blank=True)

    # 12. Membership
    membership_plans = models.CharField(max_length=255, blank=True)

    # 13. Utilities
    require_water = models.BooleanField(default=False)
    require_power = models.BooleanField(default=False)
    require_septic = models.BooleanField(default=False)
    boondock_plan = models.TextField(blank=True)

    # 14. Monthly contribution
    monthly_support = models.CharField(max_length=255, blank=True)

    # 15. Work exchange
    work_exchange_months = models.CharField(max_length=255, blank=True)
    work_days_hours = models.CharField(max_length=255, blank=True)
    work_start = models.CharField(max_length=255, blank=True)

    # 16. Deposit or collateral
    deposit = models.CharField(max_length=255, blank=True)

    # 17. Contribution area
    contribution_area = models.TextField(blank=True)

    # 18. Skills & talents
    skills_talents = models.TextField(blank=True)

    # Internal fields
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('reviewed', 'Reviewed'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Application from {self.created_at:%Y-%m-%d} (adults: {self.adults}, children: {self.children})"


class Service(models.Model):
    """Services offered by JAM Mission (e.g. petting zoo, tours)."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    """Products available for sale (e.g. eggs, chicks, plants)."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    in_stock = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    """
    An order for a product. Visitors can purchase products like eggs or chicks by
    submitting their contact details and desired quantity. Payment is handled
    separately via Zelle or Venmo, so this record tracks the order status and
    metadata but does not process payments.
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('cancelled', 'Cancelled'),
    ]

    product = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self) -> str:
        return f"{self.name} – {self.product.name} × {self.quantity}"


class NewsletterSubscriber(models.Model):
    """
    Store email addresses for visitors who sign up to receive JAM Mission news
    and marketing emails. Signing up via the home page or dedicated newsletter
    form creates an entry here.
    """

    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.email


# ---------------------------------------------------------------
# Slug auto-generation signals
#
# The following signal handlers automatically generate a unique slug
# for Event, Service and Product instances if one has not been
# supplied.  Slugs are derived from the title or name fields and
# ensure clean, URL‑friendly identifiers without requiring owners
# to enter them manually.  This improves usability on the owner
# dashboard and prevents invalid slug input.

@receiver(pre_save, sender=Event)
def set_event_slug(sender, instance: Event, **kwargs):
    """Automatically set a slug for new events if missing."""
    if not instance.slug:
        _unique_slugify(instance, instance.title)


@receiver(pre_save, sender=Service)
def set_service_slug(sender, instance: Service, **kwargs):
    """Automatically set a slug for new services if missing."""
    if not instance.slug:
        _unique_slugify(instance, instance.name)


@receiver(pre_save, sender=Product)
def set_product_slug(sender, instance: Product, **kwargs):
    """Automatically set a slug for new products if missing."""
    if not instance.slug:
        _unique_slugify(instance, instance.name)