from django.conf.urls import patterns, url
from .views import PullFromAmazonView

urlpatterns = patterns(
    'apps.dashboard.online_shops.views',
    url(r'^amazon_sync_view', 'amazon_sync_view', name='amazon_sync_view'),
)