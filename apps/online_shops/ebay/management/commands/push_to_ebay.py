import ebaysdk
from ebaysdk.utils import getNodeText
from ebaysdk.exception import ConnectionError
from ebaysdk.trading import Connection as Trading
from django.core.management.base import BaseCommand
from apps.catalogue.models import Product
from apps.online_shops.ebay.utils import EbaySync


class Command(BaseCommand):
    def handle(self, *args, **options):
        ebay_sync = EbaySync()
        products = Product.objects.all()
        for product in products:
            print product
            ebay_sync.upload_product(product)
