from django.db import models


class EbayProductSync(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    products_total = models.PositiveIntegerField()
    products_synced = models.PositiveIntegerField()


class ProductEbayId(models.Model):
    product = models.OneToOneField('catalogue.Product', related_name='ebay_id')
    ebay_id = models.CharField(max_length=63)
