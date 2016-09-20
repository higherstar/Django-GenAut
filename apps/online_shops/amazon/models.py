from django.db import models


class AmazonSync(models.Model):
    DIRECTION_CHOICES = (
        ('u', 'From GenAut to Amazon'),
        ('d', 'From Amazon to GenAut')
    )
    direction = models.CharField(max_length=1, choices=DIRECTION_CHOICES)
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    products_total = models.PositiveIntegerField()
    products_synced = models.PositiveIntegerField()
