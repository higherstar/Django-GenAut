import time
from django.views.generic import TemplateView
from subprocess import Popen
from oscar.views.decorators import staff_member_required

from ...online_shops.amazon.models import AmazonSync #from apps.online_shops.amazon.models failed with "No module named dashboard.online_shops.views"


class PullFromAmazonView(TemplateView):

    template_name = 'dashboard/online_shops/amazon_sync.html'

    def get_context_data(self, **kwargs):
        ctx = super(TemplateView, self).get_context_data(**kwargs)
        ctx['amazon_pulls'] = AmazonSync.objects.filter(direction='d')
        return ctx

    def post(self, *args, **kwargs):
        amazon_sync = AmazonSync()
        amazon_sync.status = '_STARTING_'
        amazon_sync.direction = 'd'
        amazon_sync.products_synced = 0
        amazon_sync.products_total = 0
        amazon_sync.save()
        Popen(['/home/geniuspart/public_html/venv2/bin/python', '/home/geniuspart/public_html/GenAut/manage.py', 'pull_from_amazon'])
        time.sleep(2)
        return self.get(*args, **kwargs)

amazon_sync_view = PullFromAmazonView.as_view()