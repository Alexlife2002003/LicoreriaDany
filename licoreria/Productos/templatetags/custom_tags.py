from django import template

register = template.Library()

@register.simple_tag
def update_variable(value):
    """Allows updating an existing variable in a template"""
    return value


@register.simple_tag
def sum_variable(a, b):
    """Adds two variables together and returns the result"""
    return a + b
