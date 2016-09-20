from django.contrib import messages
from django.views.generic.base import View
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404, HttpResponse
from django.utils.translation import ugettext_lazy as _
from oscar.apps.catalogue.models import ProductCategory, Category
from oscar.apps.catalogue.views import ProductCategoryView as CoreProductCategoryView,\
                                       CatalogueView as CoreCatalogueView,\
                                       ProductDetailView as CoreProductDetailView
from oscar.apps.catalogue.reviews.forms import ProductReviewForm
from oscar.apps.catalogue.search_handlers import get_product_search_handler_class
from apps.catalogue.models import get_related_attr_values, VehicleBrand

from .models import Product, VehicleType
from .utils import decrypt
from apps.carweb.client import CarWebClient


class ProductDetailView(CoreProductDetailView):
    def get_context_data(self, **kwargs):
        ctx = super(ProductDetailView, self).get_context_data(**kwargs)
        ra = get_related_attr_values()
        ctx['vehicles'] = ra['vehicles']
        ctx['product_review_form'] = ProductReviewForm(
            product=self.object,
            user=self.request.user
        )
        return ctx


class ProductCategoryView(CoreProductCategoryView):
    def get(self, request, *args, **kwargs):
        # Fetch the category; return 404 or redirect as needed
        self.category = self.get_category()
        potential_redirect = self.redirect_if_necessary(
            request.path, self.category)
        if potential_redirect is not None:
            return potential_redirect

        try:
            request_data = request.GET.dict()
            if 'vehicle_types' in request.session:
                request_data['vehicle_types'] = request.session['vehicle_types']
            self.search_handler = self.get_search_handler(
                request_data, request.get_full_path(), self.get_categories())
        except InvalidPage:
            messages.error(request, _('The given page number was invalid.'))
            return redirect(self.category.get_absolute_url())

        return super(ProductCategoryView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(ProductCategoryView, self).get_context_data(**kwargs)
        ra = get_related_attr_values()
        ctx['vehicles'] = ra['vehicles']

        # get number of current page
        try:
            page_no = int(self.request.GET.get('page', 1))
        except (TypeError, ValueError):
            page_no = 1

        # get number of items per page
        try:
            per_page = int(self.request.GET.get('per_page', 16))
        except (TypeError, ValueError):
            per_page = 16
        ctx['per_page'] = per_page

        # get sorting by part type
        try:
            sort_by_part_type = int(self.request.GET.get('sort_by_part_type', ''))
        except (TypeError, ValueError):
            sort_by_part_type = ''

        # get sorting by brand
        try:
            sort_by_brand = int(self.request.GET.get('sort_by_brand', ''))
        except (TypeError, ValueError):
            sort_by_brand = ''

        # get object list
        object_list = ctx['paginator'].object_list

        # filter object list
        if sort_by_brand != '':
            object_list = object_list.filter(brand=sort_by_brand)
        elif sort_by_part_type != '':
            part_type_obj = get_object_or_404(Category, id=sort_by_part_type)
            object_list = part_type_obj.product_set.all()
            ctx['sort_by_part_type'] = part_type_obj

        # prepare pagination
        new_pagination = Paginator(object_list, per_page)
        ctx['paginator'] = new_pagination

        # get current page
        try:
            page = new_pagination.page(page_no)
        except InvalidPage:
            raise Http404("No such page!")
        ctx['page'] = page

        # get range around current page
        num_pages = new_pagination.num_pages
        if page_no <= 2:
            page_range = range(1, 6)
        elif page_no >= num_pages-2:
            page_range = range(num_pages-4, num_pages+1)
        else:
            page_range = range(page_no-2, page_no+3)
        ctx['page_range'] = page_range

        # get content od filtering dropdowns
        ctx['brands'] = VehicleBrand.objects.all()
        ctx['part_types'] = Category.objects.all()

        return ctx


class CatalogueView(CoreCatalogueView):
    # renders browse.html
    def get(self, request, *args, **kwargs):
        try:
            request_data = request.GET.dict()
            if 'vehicle_types' in request.session:
                request_data['vehicle_types'] = request.session['vehicle_types']
            self.search_handler = self.get_search_handler(
                request_data, request.get_full_path(), [])
        except InvalidPage:
            # Redirect to page one.
            messages.error(request, _('The given page number was invalid.'))
            return redirect('catalogue:index')
        return super(CoreCatalogueView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(CatalogueView, self).get_context_data(**kwargs)
        ra = get_related_attr_values()
        ctx['vehicles'] = ra['vehicles']
        return ctx


class ImageView(View):
    def get(self, request):
        if 'd' in request.GET.keys():
            url = decrypt(request.GET['d'].encode('utf-8'))
            if url.startswith('/media/'):
                response = HttpResponse(content_type='image/jpg')
                print settings.PROJECT_PATH + url, 'r'
                with open(settings.PROJECT_PATH + url, 'r') as img:
                    response.write(img.read())
                return response
            else:
                return render_to_response('image.html', {'url': url})
