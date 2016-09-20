from django import template
from django.template.loader import select_template

__author__ = 'Jakub'

register = template.Library()

@register.simple_tag(takes_context=True)
def render_searched_product(context, product):
    """
    Render a product snippet as you would see in a browsing display.

    This templatetag looks for different templates depending on the UPC and
    product class of the passed product.  This allows alternative templates to
    be used for different product classes.
    """
    if not product:
        # Search index is returning products that don't exist in the
        # database...
        return ''

    names = ['catalogue/partials/product.html']
    template_ = select_template(names)
    # Ensure the passed product is in the context as 'product'
    context['product'] = product.object
    return template_.render(context)
