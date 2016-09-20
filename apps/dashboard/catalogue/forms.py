from django.forms import ModelForm, Form
from django.db.models import Count
from django.forms.models import inlineformset_factory
from django.forms.fields import ChoiceField
from django.forms.widgets import HiddenInput
from django.core.exceptions import ValidationError
from apps.catalogue.models import ProductVehicleCompatibility, VehicleType, Product, VehicleBrand, VehicleModel, Vehicle, ProductDeliveryOptions

from widgets import VehicleSelect


class AlwaysValidChoiceField(ChoiceField):
    def valid_value(self, value):
        return True


class ProductVehicleCompatibilityForm(ModelForm):
    class Meta:
        model = ProductVehicleCompatibility
        fields = ('vehicle_type',)
        widgets = {
            'vehicle_type': VehicleSelect,
        }


BaseProductVehicleCompatibilityFormSet = inlineformset_factory(
    Product, ProductVehicleCompatibility, form=ProductVehicleCompatibilityForm, extra=100)


class ProductVehicleCompatibilityFormSet(BaseProductVehicleCompatibilityFormSet):
    def __init__(self, product_class, user, *args, **kwargs):
        # This function just exists to drop the extra arguments
        super(ProductVehicleCompatibilityFormSet, self).__init__(*args, **kwargs)


class DeliveryOptionsForm(ModelForm):
    class Meta:
        model = ProductDeliveryOptions
        fields = (
            'product',
            'is_available',
            'fast_dispatch',
            'delivery_time',
            'special_order'
        )
        widgets = {
            'product': HiddenInput
        }
        labels = {
            'delivery_time': 'Delivered in 2 to 8 weeks',
        }
