from django.conf.urls import patterns, url
from oscar.apps.catalogue import app
from apps.catalogue import views


class BaseCatalogueApplication(app.CatalogueApplication):
    image_view = views.ImageView

    def get_urls(self):
        urlpatterns = super(BaseCatalogueApplication, self).get_urls()
        urlpatterns += patterns(
            '',
            # url(r'^pick/(?P<product_slug>[\w-]*)_(?P<pk>\d+)/$', self.pick_view.as_view(), name='pick'),
            url(r'^image/$', self.image_view.as_view(), name="image-view"),
        )

        return self.post_process_urls(urlpatterns)


class CatalogueApplication(BaseCatalogueApplication):
    pass


application = CatalogueApplication()
