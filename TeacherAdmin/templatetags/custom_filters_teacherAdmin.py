from django import template
from sys import getsizeof
register = template.Library()

@register.filter
def split(text,split_from):
    return str(text).split(split_from)[-1]


@register.filter
def subtract(val1,val2):
    return val1-val2