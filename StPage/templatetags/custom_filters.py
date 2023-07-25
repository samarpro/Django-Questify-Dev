# myapp/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def get_dict_value_ques(dictionary,key):
    return dictionary[key]["Question"]

@register.simple_tag
def get_dict_value_option(dictionary,key,ind):
    print("one")
    if len(dictionary[key]['Option'])<1:
        return None
    else:
        return dictionary[key]['Option'][ind]


@register.simple_tag
def set_value(val=None):
    return val