from oscar.apps.catalogue.search_handlers import SimpleProductSearchHandler as CoreSimpleProductSearchHandler
from apps.catalogue.models import Product


class SimpleProductSearchHandler(CoreSimpleProductSearchHandler):
    def __init__(self, request_data, full_path, categories=None):
        if 'sort_by' in request_data.keys():
            self.sort_by = request_data['sort_by']
        else:
            self.sort_by = 'title'
        if self.sort_by == 'price':
            self.sort_by = 'stockrecords__price_excl_tax'
        if 'per_page' in request_data.keys():
            try:
                self.paginate_by = int(request_data['per_page'])
            except:
                pass
        self.request_data = request_data
        super(SimpleProductSearchHandler, self).__init__(request_data, full_path, categories)

    def get_queryset(self):
        qs = Product.browsable.base_queryset().order_by(self.sort_by)
        if self.categories:
            qs = qs.filter(categories__in=self.categories).distinct()
        if 'vehicle_types' in self.request_data:
            vehicle_types_pk = self.request_data['vehicle_types'].split(',')
            qs = qs.filter(compatibilities__vehicle_type__pk__in=vehicle_types_pk).distinct()
        return qs
