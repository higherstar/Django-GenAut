from django import forms
from django.forms.models import modelformset_factory
from django.utils.translation import ugettext_lazy as _
from django_markdown.widgets import MarkdownWidget
from oscar.core.loading import get_classes
from oscar.apps.promotions.models import MultiImage, Image
from oscar.forms.widgets import ImageInput
from .conf import PROMOTION_CLASSES

RawHTML = get_classes('promotions.models', ['RawHTML', ])[0]


ImageFormSet = modelformset_factory(
    Image,
    extra=3,
    fields=['name', 'link_url', 'image'],
    # widgets={'image': ImageInput()},
    can_delete=True,
)


class PromotionTypeSelectForm(forms.Form):
    choices = []
    for klass in PROMOTION_CLASSES:
        choices.append((klass.classname(), klass._meta.verbose_name))
    promotion_type = forms.ChoiceField(choices=tuple(choices),
                                       label=_("Promotion type"))
