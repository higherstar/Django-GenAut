from django.core.urlresolvers import reverse
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect


from client import CarWebClient


class CarWebCheckView(View):
    def post(self, request, *args, **kwargs):
        car_web_client = CarWebClient()
        return HttpResponse(car_web_client.check_errors(request.POST['reg_number'].replace(' ', '')))


class VehicleSaveView(View):
    def post(self, request, *args, **kwargs):
        try:
            car_web_client = CarWebClient()
            vehicle_types = car_web_client.get_vehicle(request.POST['car_details'])
            request.session['vehicle_types'] = ','.join([str(t.pk) for t in vehicle_types])
            request.session['vehicle_info'] = request.POST['car_details']
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except Exception:
            return HttpResponseRedirect('/')


class VehicleFlushView(View):
    def post(self, request, *args, **kwargs):
        if 'vehicle_types' in request.session:
            del request.session['vehicle_types']
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
