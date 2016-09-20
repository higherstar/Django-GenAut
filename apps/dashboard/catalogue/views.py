from django_tables2.config import RequestConfig
from oscar.apps.dashboard.catalogue.views import ProductCreateUpdateView as CoreProductCreateUpdateView
from oscar.apps.dashboard.catalogue.views import ProductListView as CoreProductListView
from oscar.views.generic import ObjectLookupView
from apps.dashboard.catalogue.forms import *
from apps.catalogue.models import ProductVehicleCompatibility, VehicleType, ProductDeliveryOptions


class ProductCreateUpdateView(CoreProductCreateUpdateView):

    compatibility_formset = ProductVehicleCompatibilityFormSet
    delivery_options_form = DeliveryOptionsForm()

    def __init__(self, *args, **kwargs):
        super(ProductCreateUpdateView, self).__init__(*args, **kwargs)
        self.formsets = {'category_formset': self.category_formset,
                         'image_formset': self.image_formset,
                         'recommended_formset': self.recommendations_formset,
                         'stockrecord_formset': self.stockrecord_formset,
                         'compatibility_formset': self.compatibility_formset}

    def get_context_data(self, *args, **kwargs):
        ctx = super(ProductCreateUpdateView, self).get_context_data(*args, **kwargs)
        print dir(self.delivery_options_form)
        self.delivery_options_form.fields['product'].initial = self.object
        if self.object is not None:
            options = ProductDeliveryOptions.objects.get_or_create(product = self.object)[0]
            self.delivery_options_form.fields['is_available'].initial = options.is_available
            self.delivery_options_form.fields['fast_dispatch'].initial = options.fast_dispatch
            self.delivery_options_form.fields['delivery_time'].initial = options.delivery_time
            self.delivery_options_form.fields['special_order'].initial = options.special_order
            ctx['delivery_options_form'] = self.delivery_options_form
        else:
            self.delivery_options_form.fields['is_available'].initial = ProductDeliveryOptions._meta.get_field_by_name('is_available')[0].default
            self.delivery_options_form.fields['fast_dispatch'].initial = ProductDeliveryOptions._meta.get_field_by_name('fast_dispatch')[0].default
            self.delivery_options_form.fields['delivery_time'].initial = ProductDeliveryOptions._meta.get_field_by_name('delivery_time')[0].default
            self.delivery_options_form.fields['special_order'].initial = ProductDeliveryOptions._meta.get_field_by_name('special_order')[0].default
        return ctx

    def post(self, *args, **kwargs):
        if self.get_object() is not None:
            options = ProductDeliveryOptions.objects.get_or_create(product = self.get_object())[0]
            delivery_options_form = DeliveryOptionsForm(self.request.POST, instance=options)
            delivery_options_form.save()
        return super(ProductCreateUpdateView, self).post(*args, **kwargs)


class ProductListView(CoreProductListView):
    def __init__(self, *args, **kwargs):
        super(ProductListView, self).__init__(*args, **kwargs)

    def get_table(self, **kwargs):
        """
        Return a table object to use. The table has automatic support for
        sorting and pagination.
        """
        options = {}
        table_class = self.get_table_class()
        kwargs['order_by'] = ('title',)
        table = table_class(self.get_table_data(), **kwargs)
        paginate = self.get_table_pagination()  # pylint: disable=E1102
        if paginate is not None:
            options['paginate'] = paginate
        RequestConfig(self.request, **options).configure(table)
        return table


class VehicleLookupView(ObjectLookupView):
    model = VehicleType

    def lookup_filter(self, qs, term):
        q = qs.extra(
            where=['`catalogue_vehicletype`.`vehicle_model_id`=`catalogue_vehiclemodel`.`id` AND `catalogue_vehiclemodel`.`vehicle_brand_id`=`catalogue_vehiclebrand`.`id` AND CONCAT(`catalogue_vehiclebrand`.`vehicle_brand`, " ", `catalogue_vehiclemodel`.`vehicle_model`, " ", `catalogue_vehicletype`.`vehicle_type`) LIKE %s'],
            params=['%%%s%%' % term],
            tables=['catalogue_vehiclemodel', 'catalogue_vehiclebrand']
        )
        #lookups = [Q(vehicle_type__contains=word) | Q(vehicle_model__vehicle_model__contains=word) | Q(vehicle_model__vehicle_brand__vehicle_brand__contains=word) for word in term.split(' ')]
        #q = qs.filter(*lookups)
        return q
        #return [vehicle for vehicle in qs if term in '%s %s %s' % (vehicle.vehicle_type, vehicle.vehicle_model.vehicle_model, vehicle.vehicle_model.vehicle_brand.vehicle_brand)]
