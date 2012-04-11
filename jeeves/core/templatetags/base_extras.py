import re
from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def navactive(path, urls):
    if path == urls:
        return "active"
    return ""
    
@register.simple_tag
def navactive_startswith(path, urls):
    if urls == path[:len(urls)]:
        return "active"
    return ""