"""
Views for the JAM Mission web application.

These view functions render the various pages of the site, handle form
submissions, and manage user authentication.  Decorators and custom
logic ensure that owner and technical admin dashboards are separated
according to user group membership.
"""
from __future__ import annotations

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail

from .forms import (
    BlogForm,
    BookingForm,
    ContactForm,
    PreQualificationForm,
    EventForm,
    ServiceForm,
    ProductForm,
    OrderForm,
    NewsletterForm,
)
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


def home(request: HttpRequest) -> HttpResponse:
    """Render the landing page with mission statement and featured content."""
    # Fetch some upcoming events and active services/products to feature on home page
    events = Event.objects.filter(is_active=True).order_by('start_date')[:3]
    services = Service.objects.filter(is_active=True)[:3]
    products = Product.objects.filter(in_stock=True)[:3]
    posts = BlogPost.objects.order_by('-created')[:3]
    return render(request, 'home.html', {
        'events': events,
        'services': services,
        'products': products,
        'posts': posts,
    })


def services_page(request: HttpRequest) -> HttpResponse:
    """List all active services."""
    services = Service.objects.filter(is_active=True)
    return render(request, 'services.html', {'services': services})


def products_page(request: HttpRequest) -> HttpResponse:
    """List all products available for sale."""
    products = Product.objects.filter(in_stock=True)
    return render(request, 'products.html', {'products': products})


def events_page(request: HttpRequest) -> HttpResponse:
    """Display a list of active events."""
    events = Event.objects.filter(is_active=True)
    return render(request, 'events.html', {'events': events})


def event_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """Show details for a single event and allow booking tickets."""
    event = get_object_or_404(Event, slug=slug, is_active=True)
    form = BookingForm(request.POST or None)
    success = False
    if request.method == 'POST' and form.is_valid():
        booking = form.save(commit=False)
        # attach this event to the booking
        booking.event = event
        # limit tickets to available
        tickets_requested = booking.tickets
        if tickets_requested > event.available_tickets:
            form.add_error('tickets', f'Only {event.available_tickets} tickets are available.')
        else:
            booking.save()
            # send notification email
            recipients = settings.NOTIFICATION_EMAILS
            subject = f'New event booking: {event.title}'
            body = (
                f"Name: {booking.name}\n"
                f"Email: {booking.email}\n"
                f"Tickets: {booking.tickets}\n"
                f"Date: {booking.date}\n"
                f"Notes: {booking.notes}\n"
                f"Event: {event.title}"
            )
            if recipients:
                send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipients, fail_silently=True)
            success = True
            form = BookingForm()
    return render(request, 'event_detail.html', {'event': event, 'form': form, 'success': success})


def booking(request: HttpRequest) -> HttpResponse:
    """Handle bookings for stays or general services (without events)."""
    form = BookingForm(request.POST or None)
    success = False
    if request.method == 'POST' and form.is_valid():
        booking = form.save(commit=False)
        # event_slug may be passed from event_detail forms
        event_slug = request.POST.get('event_slug')
        if event_slug:
            event = Event.objects.filter(slug=event_slug).first()
            booking.event = event
        booking.save()
        # send booking notification
        recipients = settings.NOTIFICATION_EMAILS
        subject = 'New booking request'
        body = (
            f"Name: {booking.name}\n"
            f"Email: {booking.email}\n"
            f"Date: {booking.date}\n"
            f"Tickets: {booking.tickets}\n"
            f"Notes: {booking.notes}\n"
        )
        if booking.event:
            body += f"Event: {booking.event.title}\n"
        if recipients:
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipients, fail_silently=True)
        success = True
        form = BookingForm()
    return render(request, 'booking.html', {'form': form, 'success': success})


def blog_list(request: HttpRequest) -> HttpResponse:
    """Display all blog posts in reverse chronological order."""
    posts = BlogPost.objects.order_by('-created')
    return render(request, 'blog_list.html', {'posts': posts})


def blog_detail(request: HttpRequest, id: int) -> HttpResponse:
    """
    Display a single blog post with full content.  If the post
    does not exist a 404 will be raised.  Unlike the list view
    this page shows the cover image, publication date and full
    body of the post.  Owners can edit the post from here if
    logged in and authorised.
    """
    post = get_object_or_404(BlogPost, id=id)
    return render(request, 'blog_detail.html', {'post': post})


@login_required
def blog_edit(request: HttpRequest, id: int | None = None) -> HttpResponse:
    """Create or edit a blog post.  Only logged in users can access."""
    post = None
    if id is not None:
        post = get_object_or_404(BlogPost, id=id)
    form = BlogForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Post saved successfully.')
        return redirect('blog_list')
    return render(request, 'blog_edit.html', {'form': form, 'post': post})


def login_view(request: HttpRequest) -> HttpResponse:
    """Custom login view that redirects based on user group."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # Redirect based on group membership
            if user.is_superuser or user.groups.filter(name='technical_admin').exists():
                return redirect('tech_dashboard')
            elif user.groups.filter(name='owner').exists():
                return redirect('owner_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')


def logout_view(request: HttpRequest) -> HttpResponse:
    """Log the user out and redirect to the home page."""
    logout(request)
    return redirect('home')


@login_required
def tech_dashboard(request: HttpRequest) -> HttpResponse:
    """Dashboard for technical administrators.  Includes link to Django admin and site overview."""
    if not (request.user.is_superuser or request.user.groups.filter(name='technical_admin').exists()):
        return redirect('home')
    return render(request, 'tech_dashboard.html')


@login_required
def owner_dashboard(request: HttpRequest) -> HttpResponse:
    """Dashboard for owners to manage bookings, event tickets and blog posts."""
    if not request.user.groups.filter(name='owner').exists() and not request.user.is_superuser:
        return redirect('home')
    # Fetch bookings (non-event) and event bookings
    stay_bookings = Booking.objects.filter(event__isnull=True).order_by('-created')
    event_bookings = Booking.objects.filter(event__isnull=False).order_by('-created')
    posts = BlogPost.objects.order_by('-created')
    events = Event.objects.order_by('start_date')
    services = Service.objects.order_by('name')
    products = Product.objects.order_by('name')
    orders = Order.objects.order_by('-created')
    subscribers = NewsletterSubscriber.objects.order_by('-created_at')
    messages_count = ContactMessage.objects.count()
    applications_count = PreQualificationApplication.objects.count()

    # Analytics summary counts
    analytics = {
        'events': events.count(),
        'services': services.count(),
        'products': products.count(),
        'posts': posts.count(),
        'stay_bookings': stay_bookings.count(),
        'event_bookings': event_bookings.count(),
        'orders': orders.count(),
        'subscribers': subscribers.count(),
        'messages': messages_count,
        'applications': applications_count,
    }
    return render(request, 'owner_dashboard.html', {
        'stay_bookings': stay_bookings,
        'event_bookings': event_bookings,
        'posts': posts,
        'events': events,
        'services': services,
        'products': products,
        'orders': orders,
        'subscribers': subscribers,
        'analytics': analytics,
    })


def contact(request: HttpRequest) -> HttpResponse:
    """Handle contact form submissions."""
    form = ContactForm(request.POST or None)
    sent = False
    if request.method == 'POST' and form.is_valid():
        message: ContactMessage = form.save()
        subject = message.subject or 'New message from JAM Mission website'
        body = (
            f"Name: {message.name}\n"
            f"Email: {message.email}\n\n"
            f"Message:\n{message.message}"
        )
        recipients = settings.NOTIFICATION_EMAILS
        if recipients:
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipients, fail_silently=True)
        sent = True
        form = ContactForm()
    return render(request, 'contact.html', {'form': form, 'sent': sent})


def prequalification(request: HttpRequest) -> HttpResponse:
    """Handle the JAM Mission lease pre‑qualification application form."""
    form = PreQualificationForm(request.POST or None, request.FILES or None)
    sent = False
    if request.method == 'POST' and form.is_valid():
        app: PreQualificationApplication = form.save()
        # notify owners
        subject = 'New lease pre‑qualification application'
        body = (
            f"Application submitted on {app.created_at:%Y-%m-%d %H:%M}.\n"
            f"Adults: {app.adults}, Children: {app.children}\n"
            f"Lease term: {app.lease_term}\n"
            f"Housing size: {app.housing_size}\n"
            f"Monthly support: {app.monthly_support}"
        )
        recipients = settings.NOTIFICATION_EMAILS
        if recipients:
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipients, fail_silently=True)
        sent = True
        form = PreQualificationForm()
    return render(request, 'prequalification.html', {'form': form, 'sent': sent})


def faq(request: HttpRequest) -> HttpResponse:
    """Render the Frequently Asked Questions page."""
    return render(request, 'faq.html')


def newsletter_subscribe(request: HttpRequest) -> HttpResponse:
    """
    Handle newsletter subscription.  Visitors can submit their email to be
    added to the NewsletterSubscriber list.  Duplicate emails are ignored.
    """
    form = NewsletterForm(request.POST or None)
    success = False
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        # Only create new subscriber if it doesn't already exist
        subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
        success = True
        form = NewsletterForm()
    return render(request, 'newsletter_signup.html', {'form': form, 'success': success})


def cart_add(request: HttpRequest, slug: str) -> HttpResponse:
    """
    Add a product to the session cart.  The cart is stored in the
    user's session as a mapping of product slug to quantity.  Quantity
    defaults to 1 if not supplied.  After adding the item, redirect to
    the cart page.
    """
    product = get_object_or_404(Product, slug=slug)
    qty = 1
    try:
        qty = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        qty = 1
    cart = request.session.get('cart', {})
    cart[slug] = cart.get(slug, 0) + qty
    request.session['cart'] = cart
    return redirect('cart')


def cart_view(request: HttpRequest) -> HttpResponse:
    """
    Display the contents of the shopping cart and allow the visitor
    to place an order for all items at once.  On POST, the order
    details are captured via OrderForm and individual Order objects are
    created for each cart item.  After saving orders, the cart is
    cleared and a success message is shown.
    """
    cart = request.session.get('cart', {}) or {}
    items = []
    total = 0
    for slug, qty in cart.items():
        product = Product.objects.filter(slug=slug, in_stock=True).first()
        if product:
            subtotal = product.price * qty
            items.append({'product': product, 'quantity': qty, 'subtotal': subtotal})
            total += subtotal
    form = OrderForm(request.POST or None)
    success = False
    if request.method == 'POST' and items and form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        notes = form.cleaned_data['notes']
        # Create individual orders for each product
        for item in items:
            Order.objects.create(
                product=item['product'],
                name=name,
                email=email,
                quantity=item['quantity'],
                notes=notes,
            )
        # send notification email summarising the cart
        recipients = settings.NOTIFICATION_EMAILS
        if recipients:
            summary_lines = []
            for item in items:
                summary_lines.append(f"{item['product'].name} × {item['quantity']} = ${item['subtotal']}")
            body = (
                f"New combined order from {name}\n"
                f"Email: {email}\n"
                + "\n".join(summary_lines) + "\n"
                f"Total: ${total}\n"
                f"Notes: {notes}"
            )
            send_mail('New combined product order', body, settings.DEFAULT_FROM_EMAIL, recipients, fail_silently=True)
        # Clear the cart and reset form
        request.session['cart'] = {}
        success = True
        form = OrderForm()
        items = []
        total = 0
    return render(request, 'cart.html', {'items': items, 'total': total, 'form': form, 'success': success})


def product_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """
    Display a single product and allow visitors to place an order.  On
    successful submission, an email notification is sent to owners and
    payment instructions are displayed.
    """
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    form = OrderForm(request.POST or None)
    success = False
    if request.method == 'POST' and form.is_valid():
        order = form.save(commit=False)
        order.product = product
        order.save()
        # notify owners of new order
        recipients = settings.NOTIFICATION_EMAILS
        if recipients:
            subject = f'New product order: {product.name}'
            body = (
                f"Product: {product.name}\n"
                f"Quantity: {order.quantity}\n"
                f"Name: {order.name}\n"
                f"Email: {order.email}\n"
                f"Notes: {order.notes}"
            )
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipients, fail_silently=True)
        success = True
        form = OrderForm()
    return render(request, 'product_detail.html', {'product': product, 'form': form, 'success': success})


@login_required
def event_create(request: HttpRequest) -> HttpResponse:
    """Allow owners to create a new event."""
    if not (request.user.is_superuser or request.user.groups.filter(name='owner').exists()):
        return redirect('home')
    form = EventForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        event = form.save()
        messages.success(request, 'Event created successfully.')
        return redirect('owner_dashboard')
    return render(request, 'event_form.html', {'form': form, 'editing': False})


@login_required
def event_edit(request: HttpRequest, slug: str) -> HttpResponse:
    """Allow owners to edit an existing event."""
    if not (request.user.is_superuser or request.user.groups.filter(name='owner').exists()):
        return redirect('home')
    event = get_object_or_404(Event, slug=slug)
    form = EventForm(request.POST or None, request.FILES or None, instance=event)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Event updated successfully.')
        return redirect('owner_dashboard')
    return render(request, 'event_form.html', {'form': form, 'editing': True, 'event': event})


@login_required
def product_create(request: HttpRequest) -> HttpResponse:
    """Allow owners to create a new product."""
    if not (request.user.is_superuser or request.user.groups.filter(name='owner').exists()):
        return redirect('home')
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Product created successfully.')
        return redirect('owner_dashboard')
    return render(request, 'product_form.html', {'form': form, 'editing': False})


@login_required
def product_edit(request: HttpRequest, slug: str) -> HttpResponse:
    """Allow owners to edit an existing product."""
    if not (request.user.is_superuser or request.user.groups.filter(name='owner').exists()):
        return redirect('home')
    product = get_object_or_404(Product, slug=slug)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Product updated successfully.')
        return redirect('owner_dashboard')
    return render(request, 'product_form.html', {'form': form, 'editing': True, 'product': product})


@login_required
def service_create(request: HttpRequest) -> HttpResponse:
    """Allow owners to create a new service."""
    if not (request.user.is_superuser or request.user.groups.filter(name='owner').exists()):
        return redirect('home')
    form = ServiceForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Service created successfully.')
        return redirect('owner_dashboard')
    return render(request, 'service_form.html', {'form': form, 'editing': False})


@login_required
def service_edit(request: HttpRequest, slug: str) -> HttpResponse:
    """Allow owners to edit an existing service."""
    if not (request.user.is_superuser or request.user.groups.filter(name='owner').exists()):
        return redirect('home')
    service = get_object_or_404(Service, slug=slug)
    form = ServiceForm(request.POST or None, request.FILES or None, instance=service)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Service updated successfully.')
        return redirect('owner_dashboard')
    return render(request, 'service_form.html', {'form': form, 'editing': True, 'service': service})
