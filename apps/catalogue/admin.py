import oscar.apps.catalogue.admin
from django.contrib import admin
from nested_inline.admin import NestedTabularInline, NestedModelAdmin
from .models import Vehicle, VehicleBrand, VehicleModel, VehicleType, ProductVehicleCompatibility, OriginalProductImage


class TypesInline(NestedTabularInline):
    model = VehicleType
    extra = 0
    ordering = ('vehicle_type',)


class ModelsInline(NestedTabularInline):
    model = VehicleModel
    inlines = [TypesInline]
    extra = 0
    ordering = ('vehicle_model',)


class ProductBrandAdmin(NestedModelAdmin):
    inlines = [ModelsInline]
    ordering = ('vehicle_brand',)


class ProductModelAdmin(NestedModelAdmin):
    inlines = [TypesInline]
    ordering = ('vehicle_model',)


admin.site.register(Vehicle)
admin.site.register(VehicleBrand, ProductBrandAdmin)
admin.site.register(VehicleModel, ProductModelAdmin)
admin.site.register(VehicleType)
admin.site.register(ProductVehicleCompatibility)
admin.site.register(OriginalProductImage)
