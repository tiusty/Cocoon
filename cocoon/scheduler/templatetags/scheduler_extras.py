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


@register.simple_tag(name="replace")
def replace(value, find, replace):
    return str(value).replace(find, replace)


@register.filter(name="gmaps_from_address")
def gmap_from_address(value):
    return "https://maps.google.com/?daddr=" + value

@register.filter(name="agent_to_link")
@stringfilter
def agent_to_link(value, provider):
    if provider == "MLSPIN":
        return "https://h3b.mlspin.com/tools/roster/agent.asp?aid={0}&nomenu=true".format(value)

@register.filter
def index(List, i):
    return List[int(i)]

@register.filter(name="listing_to_ygl")
@stringfilter
def listing_to_ygl(value):
    return "https://app.yougotlistings.com/rentals/{0}".format(value)