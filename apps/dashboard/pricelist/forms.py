from django import forms
from apps.catalogue.models import Vehicle
from oscar.apps.partner.models import Partner


class PricelistUploadForm(forms.Form):
    csvfile = forms.FileField(label='File')
    vehicle = forms.ChoiceField(choices=[(v.id, v.vehicle) for v in Vehicle.objects.all()])
    # create_options = forms.BooleanField()


class ProductsUploadForm(forms.Form):
    csvfile = forms.FileField(label='File')
    partner = forms.ChoiceField(choices=[(p.id, p.name) for p in Partner.objects.all()])
    update_if_already_exists = forms.BooleanField(required=False)