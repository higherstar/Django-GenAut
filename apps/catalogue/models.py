from django.db import models
from django.db.models.aggregates import Count
from django.core.exceptions import ObjectDoesNotExist
from oscar.apps.catalogue.abstract_models import AbstractProduct, AbstractProductImage, _


class Product(AbstractProduct):
    def primary_image(self):
        """
        Returns the primary image for a product. Usually used when one can
        only display one product image, e.g. in a list of products.
        """
        images = self.original_images.all()
        ordering = self.images.model.Meta.ordering
        if not ordering or ordering[0] != 'display_order':
            # Only apply order_by() if a custom model doesn't use default
            # ordering. Applying order_by() busts the prefetch cache of
            # the ProductManager
            images = images.order_by('display_order')
        try:
            return images[0]
        except IndexError:
            # We return a dict with fields that mirror the key properties of
            # the ProductImage class so this missing image can be used
            # interchangeably in templates.  Strategy pattern ftw!
            return {
                'original': self.get_missing_image(),
                'caption': '',
                'is_missing': True}


class OriginalProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='original_images')
    display_order = models.PositiveIntegerField(default=0)
    url = models.URLField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'catalogue'
        ordering = ["display_order"]
        unique_together = ("product", "display_order")
        verbose_name = _('Product original image')
        verbose_name_plural = _('Product original images')


class ProductDeliveryOptions(models.Model):
    product = models.OneToOneField(Product, related_name='delivery_options')
    is_available = models.BooleanField(default=True)
    fast_dispatch = models.BooleanField(default=False)
    delivery_time = models.BooleanField(default=False)
    special_order = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Product Delivery Options'
        verbose_name_plural = 'Products Delivery Options'

    def __unicode__(self):
        str_options = (
            u'Fast dispatch' if self.fast_dispatch else '',
            u'Delivered in 2 to 8 weeks' if self.delivery_time else '',
            u'Special order' if self.special_order else ''
        )
        return '%s.' % ', '.join(str_options)


class Vehicle(models.Model):

    vehicle = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"

    def __unicode__(self):
        return self.vehicle


class VehicleBrand(models.Model):

    vehicle_brand = models.CharField(max_length=255, default='')

    class Meta:
        verbose_name = "Vehicle Brand"
        verbose_name_plural = "Vehicle Brands"

    def __unicode__(self):
        return self.vehicle_brand


class VehicleModel(models.Model):

    vehicle_model = models.CharField(max_length=255)
    vehicle_brand = models.ForeignKey(VehicleBrand, related_name='models')
    vehicle = models.ForeignKey(Vehicle)

    class Meta:
        verbose_name = "Vehicle Model"
        verbose_name_plural = "Vehicle Models"

    def __unicode__(self):
        return u'%s %s' % (unicode(self.vehicle_brand), self.vehicle_model)


class VehicleType(models.Model):

    vehicle_type = models.CharField(max_length=255)
    vehicle_model = models.ForeignKey(VehicleModel, related_name='types')

    class Meta:
        verbose_name = "Vehicle Type"
        verbose_name_plural = "Vehicle Types"
        ordering = ('vehicle_model__vehicle_brand__vehicle_brand', 'vehicle_model__vehicle_model', 'vehicle_type', )

    def __unicode__(self):
        return u'%s %s' % (unicode(self.vehicle_model), self.vehicle_type)


class ProductVehicleCompatibility(models.Model):
    vehicle_type = models.ForeignKey(VehicleType)
    product = models.ForeignKey(Product, related_name='compatibilities')

    class Meta:
        verbose_name = "Product Vehicle Compatibility"
        verbose_name_plural = "Product Vehicle Compatibilities"

    def __unicode__(self):
        return u'%s compatible with %s' % (self.product.title, unicode(self.vehicle_type))


def get_related_attr_values(vehicle=None, brand=None, model=None):

    vehicles = [item.vehicle for item in Vehicle.objects.all()]
    brands = []
    models = []
    type_data = []

    if vehicle:
        try:
            v = Vehicle.objects.get(vehicle=vehicle)
        except ObjectDoesNotExist:
            pass
        else:
            brands = [item.vehicle_brand for item in VehicleBrand.objects.filter(models__vehicle=v.id).annotate(count=Count('vehicle_brand')).all()]

            if brand:
                try:
                    brand = VehicleBrand.objects.get(vehicle_brand=brand)
                except ObjectDoesNotExist:
                    pass
                else:
                    models = [item.vehicle_model for item in brand.models.filter(vehicle=v).all()]

                    if model:
                        try:
                            model = VehicleModel.objects.get(vehicle_model=model)
                        except ObjectDoesNotExist:
                            pass
                        else:
                            type_data = [(item.id, item.vehicle_type) for item in model.types.all()]

    return {
        'vehicles': vehicles,
        'brands': brands,
        'models': models,
        'type_data': type_data
    }


from oscar.apps.catalogue.models import *