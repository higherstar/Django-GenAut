from oscar.apps.dashboard.catalogue.app import CatalogueApplication as CoreCatalogueApplication
from django.conf.urls import url
from views import VehicleLookupView


class CatalogueApplication(CoreCatalogueApplication):
    def get_urls(self):
        urls = super(CatalogueApplication, self).get_urls()
        urls.append(url(
            r'^vehicle_lookup', VehicleLookupView.as_view(), name='catalogue-vehicle-lookup'
        ))
        return self.post_process_urls(urls)


application = CatalogueApplication()