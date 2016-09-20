from django import template
from apps.catalogue.utils import encrypt


register = template.Library()

@register.filter
def encrypt_url(url):
    return encrypt(url)