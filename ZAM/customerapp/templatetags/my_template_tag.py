from django import template
from django.template import Template

register = template.Library()

@register.filter
def keyvalue(dict, key):
    return dict[key]
