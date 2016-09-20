from django.db import models
from django.utils.translation import ugettext_lazy as _
from oscar.apps.promotions.models import AbstractPromotion


class MultiHTML(AbstractPromotion):
    _type = 'Multi-HTML'
    name = models.CharField(_("Name"), max_length=128)
    raw_htmls = models.ManyToManyField(
        'promotions.RawHTML', blank=True,
        help_text=_(
            "Choose the RawHTML content blocks that this block will use. "
            "(You may need to create some first)."))
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'promotions'
        verbose_name = _("Multi HTML")
        verbose_name_plural = _("Multi HTML")


from oscar.apps.promotions.models import *  # noqa
