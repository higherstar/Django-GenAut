# -*- coding: utf-8 -*-
import tempfile
import gc
import csv

import xlrd
from oscar.apps.catalogue.categories import create_from_breadcrumbs
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from oscar.apps.partner.models import Partner, StockRecord

from apps.catalogue.models import ProductAttribute, ProductAttributeValue, Vehicle, VehicleBrand, \
                                  VehicleModel, VehicleType, Product, ProductClass, Category, \
                                  ProductCategory, OriginalProductImage, ProductVehicleCompatibility
from apps.online_shops.amazon import utils as amazon


class PriceListField:
    def __init__(self, label='', value=''):
        self.label = label
        self.value = value


class PriceListReader:
    def __init__(self, price_list_file):
        if price_list_file.name.endswith('.xlsx') or price_list_file.name.endswith('.xls'):
            self.file_type = 'xlsx'
            self.price_list_file = price_list_file
        elif price_list_file.name.endswith('.csv'):
            self.file_type = 'csv'
            #this code is required to open uploaded file in 'rU' mode
            self.temp_file = tempfile.NamedTemporaryFile('w')
            for chunk in price_list_file:
                self.temp_file.write(chunk)
            self.temp_file.flush()
            self.price_list_file = open(self.temp_file.name, 'rU')
        else:
            raise ValidationError('Invalid file type')

    def read(self, start_row):
        self.price_list_file.seek(0)
        if self.file_type == 'xlsx':
            book = xlrd.open_workbook(file_contents=self.price_list_file.read())
            for sheet in book.sheets():
                for row_id in range(start_row, sheet.nrows):
                    yield [value for value in sheet.row_values(row_id)]
        elif self.file_type == 'csv':
            csv_reader = csv.reader(self.price_list_file, dialect=csv.excel)
            current_row = 0
            for row in csv_reader:
                if current_row < start_row:
                    current_row += 1
                    continue
                yield [value.decode('iso-8859-1') for value in row]

    def get_attrs_names(self, labels=True):
        self.price_list_file.seek(0)
        if self.file_type == 'xlsx':
            book = xlrd.open_workbook(file_contents=self.price_list_file.read())
            sheet = book.sheet_by_index(0)
            if labels:
                return [str(value) for value in sheet.row_values(1)]
            else:
                return [str(value) for value in sheet.row_values(2)]
        elif self.file_type == 'csv':
            csv_reader = csv.reader(self.price_list_file, dialect=csv.excel)
            current_row = 0
            for row in csv_reader:
                print row
                if labels and current_row == 1:
                    return row
                if not labels and current_row == 2:
                    return row
                current_row += 1


class ImportReport:
    def __init__(self):
        self._skipped = []
        self._imported_total = 0
        self._products = []
        self._types = []

    def skip(self, column, reason, data, upc):
        self._skipped.append((column, reason, data, upc))

    def success(self):
        self._imported_total += 1

    @property
    def skipped(self):
        for column, reason, data, upc in self._skipped:
            yield column, reason, str(data), upc

    @property
    def skipped_total(self):
        return len(self._skipped)

    @property
    def imported_total(self):
        return self._imported_total

    @property
    def products(self):
        return sorted(self._products, key=lambda product: product.title)

    @property
    def types(self):
        return sorted([str(type) for type in self._types])

    def add_product(self, product):
        self._products.append(product)

    def add_type(self, type):
        self._types.append(type)


class OptionError(Exception):
    pass


class ExcelImporter(object):

    def __init__(self, type=None, partner=None, update=False):
        if type:
            self.vehicle = Vehicle.objects.get(id=type)
        if partner:
            self.partner = Partner.objects.get(id=partner)
        self.update = update


    def import_file(self, excel_file):
        report = ImportReport()
        vehicles_list = []
        brands = {}
        models = {}
        types = {}
        price_list_reader = PriceListReader(excel_file)
        for csv_row in price_list_reader.read(1):
            row = {
                'manufacturer': csv_row[0],
                'model': csv_row[1],
                'type': csv_row[2],
            }
            vehicle_model = '%s %s' % (row['manufacturer'], row['model'])
            vehicle_name = '%s %s %s' % (row['manufacturer'], row['model'], row['type'])
            if vehicle_name not in vehicles_list:
                if row['manufacturer'] in brands.keys():
                    brand = brands[row['manufacturer']]
                else:
                    brand = VehicleBrand.objects.get_or_create(vehicle_brand=row['manufacturer'])[0]
                    brands[row['manufacturer']] = brand
                if vehicle_model in models.keys():
                    model = models[vehicle_model]
                else:
                    model = VehicleModel.objects.get_or_create(vehicle_brand=brand, vehicle_model=row['model'], vehicle=self.vehicle)[0]
                    models[vehicle_model] = model
                if vehicle_name not in types.keys():
                    types[vehicle_name] = VehicleType.objects.get_or_create(vehicle_model=model, vehicle_type=row['type'])[0]
                    report.success()
                    report.add_type(types[vehicle_name])
                vehicles_list.append(vehicle_name)
        return report

    @transaction.atomic
    def import_products(self, excel_file, update):
        report = ImportReport()
        #vehicles_slug = [(v, slugify(unicode(v).split(' built')[0])) for v in VehicleType.objects.all()]
        vehicles_slug = []
        stock_records = []
        images = []
        saved_images = {}
        attribute_values = []
        compatibilities = []
        product_categories = []
        price_list_reader = PriceListReader(excel_file)
        attr_names = price_list_reader.get_attrs_names(labels=False)
        labels = price_list_reader.get_attrs_names(labels=True)
        cur_row = 3
        for csv_row in price_list_reader.read(3):
            print cur_row
            cur_row += 1
            row = {}
            for i in range(len(csv_row)):
                attr = attr_names[i]
                attr_value = csv_row[i]
                if isinstance(attr_value, str):
                    attr_value = attr_value.decode('iso-8859-1')
                elif isinstance(attr_value, int) or isinstance(attr_value, float):
                    attr_value = unicode(attr_value)
                if len(attr_value) != 0:
                    row[attr] = PriceListField(label=labels[i], value=attr_value)
            if row['feed_product_type'].value == '':
                break
            product_type_row = ProductClass.objects.get_or_create(name=row['feed_product_type'].value, track_stock=0)
            product_type = product_type_row[0]
            if product_type_row[1]:
                product_type.track_stock = 0
                product_type.save()
            if Category.objects.filter(name=row['feed_product_type'].value).count() == 0:
                create_from_breadcrumbs(row['feed_product_type'].value)
            category = Category.objects.get(name=row['feed_product_type'].value)
            pr_count = Product.objects.filter(upc=row['external_product_id'].value).count()
            if (pr_count == 0 and not update) or update:
                print 'creating'
                if pr_count == 0:
                    product = Product(upc=row['external_product_id'].value)
                else:
                    product = Product.objects.get(upc=row['external_product_id'].value)
                    ProductAttributeValue.objects.filter(product=product).delete()
                    ProductCategory.objects.filter(product=product).delete()
                    StockRecord.objects.filter(product=product).delete()
                    OriginalProductImage.objects.filter(product=product).delete()
                    ProductVehicleCompatibility.objects.filter(product=product).delete()
                product.title = row['item_name'].value
                product.description = row['product_description'].value
                product.product_class = product_type
                product.parent = None
                product.save()
                #products.append(product)


                stock_record = StockRecord()
                stock_record.product = product
                stock_record.partner = self.partner
                stock_record.partner_sku = row['item_sku'].value
                stock_record.price_currency = row['currency'].value
                stock_record.price_excl_tax = float(row['standard_price'].value.replace(',', '.'))
                stock_record.price_retail = float(row['standard_price'].value.replace(',', '.'))
                stock_record.cost_price = float(row['standard_price'].value.replace(',', '.'))
                stock_record.num_in_stock = int(float(row['quantity'].value))
                stock_record.num_allocated = int(float(row['quantity'].value))
                if StockRecord.objects.filter(partner=self.partner, partner_sku=row['item_sku'].value).count() != 0:
                    product.delete()
                    report.skip('0', 'This SKU already exists', row['item_sku'].value, row['external_product_id'].value)
                    continue
                append = True
                for record in stock_records:
                    if stock_record.partner_sku == record.partner_sku:
                        append = False
                        break
                if append:
                    stock_records.append(stock_record)
                append = True
                product_category = ProductCategory(product=product, category=category)
                for pr_category in product_categories:
                    if product_category.product == pr_category.product and product_category.category == pr_category.category:
                        append = False
                        break
                if append:
                    product_categories.append(product_category)
                for attr in row.keys():
                    if 'image_url' in attr:
                        image_link = row[attr].value
                        if len(image_link) != 0:
                            image = OriginalProductImage()
                            image.product = product
                            if 'main' in attr:
                                display_order = 0
                            else:
                                display_order = int(attr[-1])
                            image.display_order = display_order
                            image.url = image_link
                            image.save()
                    elif attr not in (
                        'item_sku',
                        'item_name',
                        'external_product_id',
                        'external_product_id_type',
                        'feed_product_type',
                        'product_description',
                        'currency',
                        'standard_price',
                        'quantity',
                        'item_package_quantity',
                        'number_of_items',
                        'is_discontinued',
                        'categories'
                    ):
                        attribute = ProductAttribute.objects.get_or_create(name=row[attr].label, product_class=product_type, code=slugify(attr.decode('utf8')))[0]
                        attribute_value = ProductAttributeValue(product=product, attribute=attribute)
                        if len(row[attr].value) < 255:
                            if attr in ('quantity', 'item_package_quantity', 'number_of_items'):
                                attribute_value.value_integer = int(row[attr].value)
                            elif 'price' in attr:
                                attribute_value.value_float = float(row[attr].value.replace(',', '.'))
                            else:
                                attribute_value.value_text = row[attr].value
                        else:
                            attribute_value.value_richtext = row[attr].value
                        #attribute_value.save()
                        append = True
                        for value in attribute_values:
                            if attribute_value.product == value.product and attribute_value.value == value.value:
                                append = False
                                break
                        if append:
                            attribute_values.append(attribute_value)
                vehicles_slug_comp = [v for v in vehicles_slug if product.slug.startswith(v[1])]
                if len(vehicles_slug_comp) != 0:
                    current_vehicle = ((None, ''))
                    for v in vehicles_slug_comp:
                        if len(v[1]) > len(current_vehicle[1]):
                            current_vehicle = v
                    compatible_with = ProductVehicleCompatibility(product=product, vehicle_type=current_vehicle[0])
                    #compatible_with.save()
                    compatibilities.append(compatible_with)
                report.add_product(product)
                report.success()

                clear = False
                if len(attribute_values) > 1000:
                    ProductAttributeValue.objects.bulk_create(attribute_values)
                    attribute_values = []
                    clear = True
                if len(product_categories) > 1000:
                    ProductCategory.objects.bulk_create(product_categories)
                    product_categories = []
                    clear = True
                if len(stock_records) > 1000:
                    StockRecord.objects.bulk_create(stock_records)
                    stock_records = []
                    clear = True
                if len(compatibilities) > 1000:
                    ProductVehicleCompatibility.objects.bulk_create(compatibilities)
                    compatibilities = []
                    clear = True
                if len(images) > 1000:
                    OriginalProductImage.objects.bulk_create(images)
                    images = []
                    clear = True
                if clear:
                    gc.collect()
            else:
                report.skip(3, 'Product already exists', row['title'].encode('iso-8859-1'), row['external_product_id'])

        #feeds = mws.Feeds(amazon.ACCESS_ID, amazon.SECRET_KEY, amazon.SELLER_ID, region='UK')
        #amazon_product_upload_result = feeds.submit_feed(amazon_xml.get_product_xml(), amazon.PRODUCT_FEED_TYPE, [amazon.MARKETPLACE_ID])
        #amazon_image_upload_result = feeds.submit_feed(amazon_xml.get_image_xml(), amazon.IMAGE_FEED_TYPE, [amazon.MARKETPLACE_ID])
        #amazon_pricing_upload_result = feeds.submit_feed(amazon_xml.get_pricing_xml(), amazon.PRICING_FEED_TYPE, [amazon.MARKETPLACE_ID])
        #amazon_availability_upload_result = feeds.submit_feed(amazon_xml.get_availability_xml(), amazon.AVAILABILITY_FEED_TYPE, [amazon.MARKETPLACE_ID])
        #feeds.get_feed_submission_result(amazon_upload_result.parsed['FeedSubmissionInfo']['FeedSubmissionId']['value'])
        #submit_results = feeds.get_feed_submission_list()
        #xml_file = open('/home/templarrr/amazon.xml', 'w')
        #xml_file.write(amazon_xml.get_product_xml())
        #xml_file.close()
        #img_file = open('/home/templarrr/amazon_img.xml', 'w')
        #img_file.write(amazon_xml.get_image_xml())
        #img_file.close()
        for i in range(0, len(product_categories), 1000):
            ProductCategory.objects.bulk_create(product_categories[i: i + 1000])
        for i in range(0, len(stock_records), 1000):
            StockRecord.objects.bulk_create(stock_records[i: i + 1000])
        for i in range(0, len(images), 1000):
            OriginalProductImage.objects.bulk_create(images[i: i + 1000])
        for i in range(0, len(attribute_values), 1000):
            ProductAttributeValue.objects.bulk_create(attribute_values[i: i + 1000])
        for i in range(0, len(compatibilities), 1000):
            ProductVehicleCompatibility.objects.bulk_create(compatibilities[i: i + 1000])
        return report

