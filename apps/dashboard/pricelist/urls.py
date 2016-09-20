from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.dashboard.pricelist.views',
    url(r'^import_search_fields', 'import_pricelist', name='file_import'),
    url(r'^import_products', 'import_products', name='file_import'),
    # url(r'^list/(?P<pk>\S+)/', CSVUpdate.as_view(), name='csvupdate'),
    # url(r'^500.shtml', CSVList.as_view(), name='err'),
)