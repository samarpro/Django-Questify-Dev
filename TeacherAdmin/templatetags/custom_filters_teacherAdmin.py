from django import template
from sys import getsizeof
register = template.Library()

@register.filter
def split(text,split_from):
    print(getsizeof(text))
    return str(text).split(split_from)[-1]