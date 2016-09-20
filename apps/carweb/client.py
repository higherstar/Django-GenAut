from bs4 import BeautifulSoup
import pycurl
import time
import urllib
import urlparse
import cStringIO
from django.http import Http404


from apps.catalogue.models import VehicleBrand, VehicleModel, VehicleType


class CarWebClient:
    def __init__(self):
        self.url = 'http://www.eurocarparts.com/car-parts/'
        self.vrm_url = '/catalog/manufacturers/getvehiclebyreg'
        self.vehicle_brand = ''
        self.vehicle_model = ''
        self.build_date = ''
        self.power = ''
        self.engine_volume = ''

    @staticmethod
    def __check_year(year):
        if len(year) == 2:
            if year[0] in ('0', '1'):
                year = '20' + year
            else:
                year = '19' + year
        return year

    @classmethod
    def __date_in_range(cls, date, range):
        if date == '':
            return True
        range_start, range_end = range.split('-')
        range_start_month, range_start_year = range_start.split('.')
        range_end_month, range_end_year = range_end.split('.')
        if '/' in date:
            man_month, man_year = date.split('/')
        else:
            man_month = '2'
            man_year = date
            range_start_month = '1'
            range_end_month = '12'
        man_year = cls.__check_year(man_year)
        range_start_year = cls.__check_year(range_start_year)
        range_end_year = cls.__check_year(range_end_year)
        if range_start_year == '':
            range_start_year = '0'
        if range_start_month == '':
            range_start_month = '0'
        if range_end_year == '':
            range_end_year = '9999'
        if range_end_month == '':
            range_end_month = '99'
        start_months = int(range_start_year) * 12 + int(range_start_month)
        end_months = int(range_end_year) * 12 + int(range_end_month)
        man_months = int(man_year) * 12 + int(man_month)
        return start_months <= man_months <= end_months

    def check_errors(self, vrm):
        raw_data = cStringIO.StringIO()
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, 'http://cameleo.ru/')
        curl.setopt(pycurl.USERAGENT, 'Mozilla/5.0 (X11; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0')
        curl.setopt(pycurl.HTTPHEADER, [
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding: identity',
            'Connection: keep-alive'
        ])
        curl.setopt(pycurl.FOLLOWLOCATION, True)
        curl.setopt(pycurl.COOKIEJAR, 'cookie.txt')
        curl.setopt(pycurl.USERAGENT, 'Mozilla/5.0 (X11; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0')
        curl.setopt(pycurl.HTTPHEADER, [
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding: identity',
            'Connection: keep-alive'
        ])
        curl.perform()

        curl.setopt(pycurl.POST, 1)
        curl.setopt(pycurl.POSTFIELDS, urllib.urlencode({'url': self.url}))
        curl.setopt(pycurl.USERAGENT, 'Mozilla/5.0 (X11; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0')
        curl.setopt(pycurl.HTTPHEADER, [
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding: identity',
            'Connection: keep-alive'
        ])
        curl.setopt(pycurl.REFERER, 'http://cameleo.ru/')
        curl.setopt(pycurl.URL, 'http://cameleo.ru/r')
        curl.setopt(pycurl.COOKIEFILE, 'cookie.txt')
        curl.setopt(pycurl.COOKIEJAR, 'coockie2.txt')
        curl.perform()

        curl.setopt(pycurl.REFERER, curl.getinfo(pycurl.EFFECTIVE_URL))
        curl.setopt(pycurl.COOKIEFILE, 'cookie2.txt')
        curl.setopt(pycurl.WRITEFUNCTION, raw_data.write)
        o = urlparse.urlparse(curl.getinfo(pycurl.EFFECTIVE_URL))
        curl.setopt(pycurl.URL, '%s://%s%s' % (o.scheme, o.netloc, self.vrm_url))
        curl.setopt(pycurl.POSTFIELDS, urllib.urlencode({'reg': vrm}))
        curl.perform()

        time.sleep(1)
        soup = BeautifulSoup(raw_data.getvalue())
        car_details_result_set = soup.select('.search-summery span[title]')
        if len(car_details_result_set) == 0:
            raise Http404
        else:
            return '%s %s %s %s %s' % tuple([e.text for e in car_details_result_set])

    def get_vehicle(self, car_details):
        # car_detail format : Brand model year volume fuel
        # example: Volkswagen Touran 2007 1.6 Petrol
        self.vehicle_brand, self.vehicle_model, self.build_date, self.engine_volume, _ = car_details.split(' ')
        self.vehicle_brand = self.vehicle_brand.upper()
        if self.vehicle_brand == 'VOLKSWAGEN':
            self.vehicle_brand = 'VW'
        brand_record = VehicleBrand.objects.filter(vehicle_brand=self.vehicle_brand).first()
        if not brand_record:
            return None

        models = list(VehicleModel.objects.filter(vehicle_brand=brand_record, vehicle_model__icontains=self.vehicle_model))
        types = VehicleType.objects.filter(vehicle_model__in=models)
        found_types = []
        for vehicle_type in types:
            name = vehicle_type.vehicle_type
            build_range = name.split(' built ')[1]
            if not name.startswith(self.engine_volume):
                continue
            if self.__date_in_range(self.build_date, build_range):
                found_types.append(vehicle_type)
        return found_types
