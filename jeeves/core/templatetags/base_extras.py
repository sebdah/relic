from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def navactive(request, urls):
    for url in urls.split():
        if request.path.split('/')[1] == reverse(url).split('/')[1]:
            return "active"
    return ""