import urllib
from django.utils.http import urlquote

__author__ = 'Jakub'

from django import template


register = template.Library()

@register.simple_tag
def url_replace(request, field, value):

    dict_ = request.GET.copy()
    dict_[field] = value

    return '?' + urllib.urlencode(dict_)
