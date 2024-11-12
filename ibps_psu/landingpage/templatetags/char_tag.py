from django import template

register = template.Library()

@register.filter
def contain_number(value):
    return any(char.isdigit() for char in value)
