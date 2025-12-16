"""
Custom template filters for checking user group membership.

These filters allow templates to check whether the current user belongs
to a given Django auth group without invoking method calls that are
disallowed in the template language.  Usage:

    {% load group_filters %}
    {% if user|has_group:'technical_admin' %}
        ...
    {% endif %}
"""
from __future__ import annotations

from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name: str) -> bool:
    """Return True if the user belongs to a group with the given name."""
    if not hasattr(user, 'groups'):
        return False
    return user.groups.filter(name=group_name).exists()