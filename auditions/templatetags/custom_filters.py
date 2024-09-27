# auditions/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """
    Add a CSS class to a form field widget.
    """
    if hasattr(field, 'as_widget'):
        return field.as_widget(attrs={'class': css_class})
    return field  # Return the field unchanged if it doesn't have 'as_widget'
