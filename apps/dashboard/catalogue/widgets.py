from django.core.urlresolvers import reverse_lazy
from oscar.forms.widgets import RemoteSelect


class VehicleSelect(RemoteSelect):
    lookup_url = reverse_lazy('dashboard:catalogue-vehicle-lookup')
