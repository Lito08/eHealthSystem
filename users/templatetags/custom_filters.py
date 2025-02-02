from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def add_days(value, days):
    """Adds the specified number of days to a date."""
    if value:
        return value + timedelta(days=int(days))
    return value
