from django.core.paginator import Paginator, InvalidPage
from django.http.response import Http404
from django.shortcuts import render_to_response
from oscar.apps.search.views import FacetedSearchView as CoreFacetedSearchView
from haystack.models import SearchResult
from apps.carweb.client import CarWebClient
from apps.catalogue.models import Product, VehicleType


class FacetedSearchView(CoreFacetedSearchView):
    def create_response(self):
        if 'car_details' in self.request.GET or 'type' in self.request.GET:
            context = {}
            try:
                page_no = int(self.request.GET.get('page', 1))
            except (TypeError, ValueError):
                page_no = 1

            vehicle_types = []
            searched_car = ''
            if 'car_details' in self.request.GET:
                car_web_client = CarWebClient()
                vehicle_types = car_web_client.get_vehicle(self.request.GET['car_details'])
                try:
                    searched_car = '%s %s %s %skW built %s' % (
                        car_web_client.vehicle_brand,
                        car_web_client.vehicle_model,
                        car_web_client.engine_volume,
                        car_web_client.power,
                        car_web_client.build_date
                    )
                except:
                    pass

            elif 'type' in self.request.GET:
                type_value = self.request.GET.get('type', '')
                vehicle_types = VehicleType.objects.filter(id=int(type_value))
                searched_car = str(vehicle_types.first())
                if vehicle_types is None:
                    raise Http404("No such page!")

            products = Product.objects.filter(compatibilities__vehicle_type__in=vehicle_types)
            paginator = Paginator(products, 25)
            try:
                page = paginator.page(page_no)
            except InvalidPage:
                raise Http404("No such page!")
            object_list = []

            for obj in page.object_list:
                object_list.append(SearchResult('catalogue', 'product', obj.pk, 0))
            page.object_list = object_list

            if len(vehicle_types) != 0:
                context['paginator'] = paginator
                context['page'] = page
            context['query'] = searched_car
            context['suggetion'] = None
            context['form'] = self.form
            context.update(self.extra_context())
            return render_to_response(self.template, context, context_instance=self.context_class(self.request))
        else:
            context = {}

            # get number of items per page
            try:
                per_page = int(self.request.GET.get('per_page', 16))
            except (TypeError, ValueError):
                per_page = 16


            # get number of items per page
            try:
                page_no = int(self.request.GET.get('page', 1))
            except (TypeError, ValueError):
                page_no = 1

            # prepare paginator
            paginator = Paginator(self.results, per_page)

            page = paginator.page(page_no)

            context = {
                'query': self.query,
                'form': self.form,
                'page': page,
                'per_page': per_page,
                'page_obj': page,
                'paginator': paginator,
                'suggestion': None,
            }

            # get range around current page
            num_pages = paginator.num_pages
            if page_no<=2:
                page_range = range(1, 6)
            elif page_no>=num_pages-2:
                page_range = range(num_pages-4, num_pages+1)
            else:
                page_range = range(page_no-2, page_no+3)
            context['page_range'] = page_range

            context['is_paginated'] = True

            if self.results and hasattr(self.results, 'query') and self.results.query.backend.include_spelling:
                context['suggestion'] = self.form.get_suggestion()

            context.update(self.extra_context())
            return render_to_response(self.template, context, context_instance=self.context_class(self.request))


