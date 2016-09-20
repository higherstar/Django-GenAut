from django.http import HttpResponse
import json
import math

from oscar.apps.promotions.views import HomeView as CoreHomeView
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import Http404
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Count

from apps.catalogue.models import get_related_attr_values, Product, Category, ProductCategory
from oscar.apps.partner.strategy import Default


class HomeView(CoreHomeView):
    paginate_by = 20

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)
        ra = get_related_attr_values()
        ctx['vehicles'] = ra['vehicles']
        product_num = 20
        categories = list(Category.objects.filter(productcategory__isnull=False).annotate(p_count=Count('id')))
        if len(categories) == 0:
            return ctx
        products_per_category = product_num / len(categories)
        if products_per_category == 0:
            products_per_category = 1
        products = []
        if 'vehicle_types' in self.request.session:
            vehicle_types_pk = self.request.session['vehicle_types'].split(',')
            for category in categories[:-2]:
                for product_category in ProductCategory.objects.filter(
                        category=category,
                        product__compatibilities__vehicle_type__pk__in=vehicle_types_pk
                ).distinct().order_by('product__title')[:products_per_category]:
                    products.append(product_category.product)
            for product_category in ProductCategory.objects.filter(
                    category=categories[-1],
                    product__compatibilities__vehicle_type__pk__in=vehicle_types_pk
            ).distinct().order_by('product__title').all()[:product_num - len(products)]:
                products.append(product_category.product)
        else:
            for category in categories[:-2]:
                for product_category in ProductCategory.objects.filter(category=category).order_by('product__title')[:products_per_category]:
                    products.append(product_category.product)
            for product_category in ProductCategory.objects.filter(category=categories[-1]).order_by('product__title').all()[:product_num - len(products)]:
                products.append(product_category.product)
        ctx['products'] = products
        #page_no = self.request.GET.get('page', 1)
        #ctx['paginator'] = Paginator(Product.objects.order_by('title').all(), self.paginate_by)
        #try:
        #    ctx['page'] = ctx['paginator'].page(page_no)
        #except InvalidPage:
        #    raise Http404('No such page!')
        return ctx

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CoreHomeView, self).dispatch(*args, **kwargs)

    def post(self, request):
        if request.is_ajax():

            ra = get_related_attr_values(
                vehicle=request.POST.get('vehicle', ''),
                brand=request.POST.get('brand', ''),
                model=request.POST.get('model', '')
            )
            json_data = json.dumps(ra)

            return HttpResponse(json_data)
