import mws
import time
import urllib
import csv
from lxml import etree
from cStringIO import StringIO
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
from oscar.apps.partner.models import StockRecord, Partner
from apps.online_shops.amazon import utils as amazon
from apps.online_shops.amazon.models import AmazonSync
from apps.catalogue.models import Product, ProductClass, ProductAttribute, ProductAttributeValue, ProductDeliveryOptions


class Command(BaseCommand):
    def handle(self, *args, **options):
        sync_record = AmazonSync.objects.get(status='_STARTING_')
        sync_record.status = 'Collecting data...'
        sync_record.save()
        reports = mws.Reports(amazon.ACCESS_ID, amazon.SECRET_KEY, amazon.SELLER_ID, region='UK')
        request_report = reports.request_report(amazon.PRODUCT_LIST_REPORT, marketplaceids=[amazon.MARKETPLACE_ID])
        report_done = False
        report_request_id = request_report.parsed['ReportRequestInfo']['ReportRequestId']['value']
        while not report_done:
            time.sleep(45)
            request_report_list = reports.get_report_request_list(requestids=[report_request_id])
            if request_report_list.parsed['ReportRequestInfo']['ReportProcessingStatus']['value'] == '_DONE_':
                if 'GeneratedReportId' in request_report_list.parsed['ReportRequestInfo'].keys():
                    report_id = request_report_list.parsed['ReportRequestInfo']['GeneratedReportId']['value']
                else:
                    time.sleep(60)
                    report_list = reports.get_report_list(requestids=[report_request_id])
                    report_id = report_list.parsed['ReportInfo']
                report_done = True
        sync_record.status = 'Amazon report loaded.'
        report = reports.get_report(report_id)
        report_buffer = StringIO(report.original)
        report_reader = csv.DictReader(report_buffer, delimiter='\t')
        rows = list(report_reader)
        product_class = ProductClass.objects.get_or_create(name='AutoPart', track_stock=0)[0]
        partner = Partner.objects.first()
        csv_to_site_attrs = {
            'item-condition': 'condition_type',
            'open-date': 'product_site_launch_date',
            'item-note': 'condition_note',
        }
        condition_types = {
            '1': 'Used Like New',
            '2': 'Used Very Good',
            '3': 'Used Good',
            '4': 'Used Acceptable',
            '5': 'Collectible Like New',
            '6': 'Collectible Very Good',
            '7': 'Collectible Good',
            '8': 'Collectible Acceptable',
            '9': 'Used; Refurbished',
            '10': 'Refurbished',
            '11': 'New',
        }

        asins_used = []
        attribute_records = {}
        stock_records = []
        attribute_value_records = []

        unique_asins = []
        products_total = 0
        for row in rows:
            if not row['asin1'] in unique_asins:
                unique_asins.append(row['asin1'])
                products_total += 1
        sync_record.products_total = products_total
        sync_record.status = 'Saving products data...'
        sync_record.save()
        k = 1
        unique_asins = []
        product_ids_from_amazon = []
        for i in range(0, len(rows), 100):
            with transaction.atomic():
                for row in rows[i: i + 100]:
                    print k
                    k += 1
                    if row['item-name'].endswith('...'):
                        row['item-name'] = row['item-name'][: -4]
                    row['item-name'].strip()
                    if row['item-name'] == '':
                        continue
                    row['item-name'] = row['item-name'].decode('iso-8859-1')
                    if Product.objects.filter(upc=row['asin1']).exists():
                        product = Product.objects.get(upc=row['asin1'])
                    else:
                        if Product.objects.filter(title=row['item-name']).exists():
                            product = Product.objects.get(title=row['item-name'])
                            product.upc = row['asin1']
                        else:
                            if Product.objects.filter(title__startswith=row['item-name']).exists():
                                product = Product.objects.get(title__startswith=row['item-name'])
                                product.upc = row['asin1']
                            else:
                                product = Product(upc=row['asin1'])
                                product.title = row['item-name']

                    product.description = row['item-description'].replace('&lt;', '<').replace('&gt;', '>')
                    product.product_class = product_class
                    product.parent = None
                    product.save()
                    if not hasattr(product, 'delivery_options'):
                        product_delivery_options = ProductDeliveryOptions(product=product)
                        product_delivery_options.save()

                    product_ids_from_amazon.append(product.id)

                    product.stockrecords.all().delete()
                    stock_record = StockRecord()
                    stock_record.product = product
                    stock_record.partner = partner
                    stock_record.partner_sku = row['seller-sku']
                    stock_record.price_currency = 'GBP'
                    stock_record.price_excl_tax = float(row['price'])
                    stock_record.price_retail = float(row['price'])
                    stock_record.cost_price = float(row['price'])
                    stock_record.num_in_stock = int(row['quantity'])
                    stock_record.num_allocated = int(row['quantity'])

                    stock_record.save()
                    #stock_records.append(stock_record)

                    for key in csv_to_site_attrs.keys():
                        if row[key] == '':
                            continue
                        if key in row.keys():
                            if not slugify(csv_to_site_attrs[key].decode('iso-8859-1')) in attribute_records.keys():
                                if ProductAttribute.objects.filter(code=csv_to_site_attrs[key].decode('iso-8859-1'), product_class=product_class).exists():
                                    attribute = ProductAttribute.objects.get(code=csv_to_site_attrs[key].decode('iso-8859-1'), product_class=product_class)
                                else:
                                    attribute = ProductAttribute(name=csv_to_site_attrs[key].decode('iso-8859-1'), code=key, product_class=product_class)
                                    attribute.save()
                                attribute_records[slugify(csv_to_site_attrs[key].decode('iso-8859-1'))] = attribute
                            else:
                                attribute = attribute_records[slugify(csv_to_site_attrs[key].decode('iso-8859-1'))]

                            ProductAttributeValue.objects.filter(product=product, attribute=attribute).delete()
                            print 'Deleting values of attribute ', attribute
                            if key == 'item-condition':
                                value_text = condition_types[row[key]]
                            else:
                                value_text=row[key]
                            attribute_value = ProductAttributeValue(product=product, attribute=attribute, value_text=value_text)
                            attribute_value.save()
                            #attribute_value_records.append(attribute_value)
                    if not row['asin1'] in unique_asins:
                        unique_asins.append(row['asin1'])
                        sync_record.products_synced += 1
                        sync_record.save()

        sync_record.status = 'Deleting non-Amazon products...'
        sync_record.save()

        Product.objects.exclude(id__in=product_ids_from_amazon).delete()

        sync_record.status = 'Done.'
        sync_record.save()
