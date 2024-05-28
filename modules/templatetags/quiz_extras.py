from django import template

register = template.Library()


@register.filter
def get_value(dictionary, key):
    if dictionary is None or key is None:
        return None
    return dictionary.get(key)


@register.filter
def join_string(string1, string2):
    return string1 + ", " + string2
