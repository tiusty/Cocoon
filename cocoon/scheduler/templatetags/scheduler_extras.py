from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter(name="try_string")
@stringfilter
def try_string(string, alt_text):
    if string is "":
        return alt_text
    return string


@register.simple_tag(name="condition")
def condition(value, truthy, falsey):
    if value:
        return truthy
    return falsey