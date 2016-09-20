
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from paypal.express.dashboard.app import application as paypal_application
from oscar.app import application
from apps import customer
from apps.carweb.views import CarWebCheckView, VehicleSaveView, VehicleFlushView
from apps.dashboard.menus.app import application as menus_app
import django.views.defaults


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'GenAut.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^pricelist/', include('apps.dashboard.pricelist.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^check_vrm/', CarWebCheckView.as_view()),
    url(r'^vehicle_save/', VehicleSaveView.as_view()),
    url(r'^vehicle_flush/', VehicleFlushView.as_view()),
    url(r'^online_shops/', include('apps.dashboard.online_shops.urls')),
    url(r'^checkout/paypal/', include('paypal.express.urls')),
    url(r'^dashboard/paypal/express/', include(paypal_application.urls)),
    url(r'', include(application.urls)),
    url(r'^404/$', django.views.defaults.page_not_found),
    url(r'^login/$', customer.views.login_user),
    url(r'^dashboard/menus/', include(menus_app.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
