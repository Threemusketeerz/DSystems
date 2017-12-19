from django import template
from django.contrib.auth.models import User

register = template.Library()


@register.filter
def set_placeholder(field, placeholder=None):
    if not placeholder:
        return field
    
    field.field.widget.attrs.update({
        "class": "form-control",
        "placeholder": placeholder
        }
    )
    return field


