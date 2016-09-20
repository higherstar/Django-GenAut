from collections import OrderedDict
from lxml import etree


ACCESS_ID = 'AKIAIG4MLGAKOOXV4DGQ'
SECRET_KEY = '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'
ACCOUNT_ID = '8287-0683-1288'
SELLER_ID = 'AJ5L86B5BIVRJ'
MARKETPLACE_ID = 'A1F83G8C2ARO7P'
MWS_AUTORIZATION_TOKEN = 'amzn.mws.b6a694bb-c7b3-69fd-b5d3-ebdf30bf4a98'

PRODUCT_FEED_TYPE = '_POST_PRODUCT_DATA_'
IMAGE_FEED_TYPE = '_POST_PRODUCT_IMAGE_DATA_'
PRICING_FEED_TYPE = '_POST_PRODUCT_PRICING_DATA_'
AVAILABILITY_FEED_TYPE = '_POST_INVENTORY_AVAILABILITY_DATA_'

PRODUCT_LIST_REPORT = '_GET_MERCHANT_LISTINGS_DATA_'


class AmazonXML:
    def __init__(self):
        self.__product_amazon_envelope = etree.Element('AmazonEnvelope', nsmap={'xsi': 'http://www.w3.org/2001/XMLSchema-instance'})
        self.__product_amazon_envelope.set('{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation', 'amzn-envelope.xsd')

        header = etree.Element('Header')
        document_version = etree.Element('DocumentVersion')
        document_version.text = '1.01'
        merchant_identifier = etree.Element('MerchantIdentifier')
        merchant_identifier.text = SELLER_ID
        header.append(document_version)
        header.append(merchant_identifier)
        self.__product_amazon_envelope.append(header)
        message_type = etree.Element('MessageType')
        message_type.text = 'Product'
        self.__product_amazon_envelope.append(message_type)
        purge_and_replace = etree.Element('PurgeAndReplace')
        purge_and_replace.text = 'false'
        self.__product_amazon_envelope.append(purge_and_replace)


        self.__image_amazon_envelope = etree.Element('AmazonEnvelope', nsmap={'xsi': 'http://www.w3.org/2001/XMLSchema-instance'})
        self.__image_amazon_envelope.set('{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation', 'amzn-envelope.xsd')

        header = etree.Element('Header')
        document_version = etree.Element('DocumentVersion')
        document_version.text = '1.01'
        merchant_identifier = etree.Element('MerchantIdentifier')
        merchant_identifier.text = SELLER_ID
        header.append(document_version)
        header.append(merchant_identifier)
        self.__image_amazon_envelope.append(header)
        message_type = etree.Element('MessageType')
        message_type.text = 'ProductImage'
        self.__image_amazon_envelope.append(message_type)

        self.__pricing_amazon_envelope =  etree.Element('AmazonEnvelope', nsmap={'xsi': 'http://www.w3.org/2001/XMLSchema-instance'})
        self.__pricing_amazon_envelope.set('{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation', 'amzn-envelope.xsd')

        header = etree.Element('Header')
        document_version = etree.Element('DocumentVersion')
        document_version.text = '1.01'
        merchant_identifier = etree.Element('MerchantIdentifier')
        merchant_identifier.text = SELLER_ID
        header.append(document_version)
        header.append(merchant_identifier)
        self.__pricing_amazon_envelope.append(header)
        message_type = etree.Element('MessageType')
        message_type.text = 'Price'
        self.__pricing_amazon_envelope.append(message_type)

        self.__availability_amazon_envelope =  etree.Element('AmazonEnvelope', nsmap={'xsi': 'http://www.w3.org/2001/XMLSchema-instance'})
        self.__availability_amazon_envelope.set('{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation', 'amzn-envelope.xsd')

        header = etree.Element('Header')
        document_version = etree.Element('DocumentVersion')
        document_version.text = '1.01'
        merchant_identifier = etree.Element('MerchantIdentifier')
        merchant_identifier.text = SELLER_ID
        header.append(document_version)
        header.append(merchant_identifier)
        self.__availability_amazon_envelope.append(header)
        message_type = etree.Element('MessageType')
        message_type.text = 'Inventory'
        self.__availability_amazon_envelope.append(message_type)

        self.__product_message_id = 1
        self.__image_message_id = 1
        self.__pricing_message_id = 1
        self.__availability_message_id = 1

        self.__csv_to_xml_desc_attrs = OrderedDict([
            ('item_name', 'Title'),
            ('brand_name', 'Brand'),
            ('product_description', 'Description'),
            ('bullet_pointN', 'BulletPoint'),
            ('package_weight', 'PackageWeight'),
            ('website_shipping_weight', 'ShippingWeight'),
            ('catalog_number', 'MerchantCatalogNumber'),
            ('standard_price', 'MSRP'),
            ('legal_disclaimer_description', 'LegalDisclaimer'),
            ('manufacturer', 'Manufacturer'),
            ('part_number', 'MfrPartNumber'),
            ('generic_keywordsN', 'SearchTerms'),
            ('platinum_keywordsN', 'PlatinumKeywords'),
            ('is_memorabilia', 'Memorabilia'),
            ('is_autographed', 'Autographed'),
            ('product_type', 'ItemType'),
            ('can_be_gift_wrapped', 'IsGiftWrapAvailable'),
            ('can_be_gift_messaged', 'IsGiftMessageAvailable'),
            ('is_discontinued', 'IsDiscontinuedByManufacturer'),
            ('max_aggregate_ship_quantity', 'MaxAggregateShipQuantity'),
            ('recommended_browse_nodesN', 'RecommendedBrowseNode'),
            ('eu_toys_safety_directive_age_warning', 'TSDAgeWarning'),
            ('eu_toys_safety_directive_warning', 'TSDWarning'),
            ('eu_toys_safety_directive_language', 'TSDLanguage'),
        ])

        self.__csv_to_xml_data_attrs = OrderedDict([
            ('size_name', 'Size'),
            ('color_name', 'ColorSpecification/Color'),
            ('color_map', 'ColorSpecification/ColorMap'),
            ('material_type', 'Material'),
            ('item_shape', 'ItemShape'),
            ('viscosity', 'Viscosity'),
            ('hole_count', 'NumberOfHoles'),
            ('number_of_grooves', 'NumberOfGrooves'),
            ('oe_manufacturer', 'PartInterchangeData/OEManufacturer'),
            ('part_interchange_info', 'PartInterchangeData/PartInterchangeInfo'),
            ('voltage', 'Voltage'),
            ('wattage', 'Wattage'),
            ('warranty_description', 'ManufacturerWarrantyDescription'),
            #('mfg_warranty_description_type', 'MfgWarrantyDescriptionType'),
            ('part_type_id', 'part_type_id'),
            ('amperage', 'Amperage'),
        ])

    def get_product_xml(self, pretty_print=False):
        return etree.tostring(self.__product_amazon_envelope, xml_declaration=True, pretty_print=pretty_print, encoding='iso-8859-1')

    def get_image_xml(self, pretty_print=False):
        return etree.tostring(self.__image_amazon_envelope, xml_declaration=True, pretty_print=pretty_print, encoding='iso-8859-1')

    def get_pricing_xml(self, pretty_print=False):
        return etree.tostring(self.__pricing_amazon_envelope, xml_declaration=True, pretty_print=pretty_print, encoding='iso-8859-1')

    def get_availability_xml(self, pretty_print=False):
        return etree.tostring(self.__availability_amazon_envelope, xml_declaration=True, pretty_print=pretty_print, encoding='iso-8859-1')

    def add_product(self, row):
        message = etree.Element('Message')
        message_id = etree.Element('MessageID')
        message_id.text = str(self.__product_message_id)
        message.append(message_id)
        operation_type = etree.Element('OperationType')
        operation_type.text = 'Update'
        message.append(operation_type)

        product = etree.Element('Product')
        sku = etree.Element('SKU')
        sku.text = row['item_sku'].value
        product.append(sku)

        if 'external_product_id' in row.keys() and 'external_product_id_type' in row.keys():
            product_id = etree.Element('StandardProductID')
            product_id_type = etree.Element('Type')
            product_id_type.text = row['external_product_id_type'].value
            product_id.append(product_id_type)
            product_id_value = etree.Element('Value')
            product_id_value.text = row['external_product_id'].value
            product_id.append(product_id_value)
            product.append(product_id)

        if 'product_site_launch_date' in row.keys():
            launch_date = etree.Element('LaunchDate')
            launch_date.text = row['product_site_launch_date'].value.replace('.', '-') + 'T00:00:00'
            product.append(launch_date)

        if 'merchant_release_date' in row.keys():
            release_date = etree.Element('ReleaseDate')
            release_date.text = row['merchant_release_date'].value.replace('.', '-') + 'T00:00:00'
            product.append(release_date)

        if 'condition_type' in row.keys(): #TODO: fixed set of values
            condition = etree.Element('Condition')
            condition_type = etree.Element('ConditionType')
            condition_type.text = row['condition_type'].value
            condition.append(condition_type)
            if 'condition_note' in row.keys():
                condition_note = etree.Element('ConditionNote')
                condition_note.text = row['condition_note'].value
                condition.append(condition_note)
            product.append(condition)

        items_per_pack = etree.Element('ItemPackageQuantity')
        items_per_pack.text = row['item_package_quantity'].value
        product.append(items_per_pack)

        quantity = etree.Element('NumberOfItems')
        quantity.text = row['number_of_items'].value #TODO right field for quantity
        product.append(quantity)

        description_data = etree.Element('DescriptionData')
        for csv_attr in self.__csv_to_xml_desc_attrs.keys():
            if csv_attr.endswith('N'):
                for row_attr in row.keys():
                    if row_attr.startswith(csv_attr[: -1]):
                        xml_element = etree.Element(self.__csv_to_xml_desc_attrs[csv_attr])
                        xml_element.text = row[row_attr].value
                        if csv_attr.startswith('platinum'):
                            xml_element.text = xml_element.text[:49]
                        description_data.append(xml_element)
            elif csv_attr.startswith('is') or csv_attr.startswith('can'):
                if csv_attr in row.keys():
                    xml_element = etree.Element(self.__csv_to_xml_desc_attrs[csv_attr])
                    if row[csv_attr].value.lower() not in ('false', 'no', '0'):
                        xml_element.text = 'true'
                    else:
                        xml_element.text = 'false'
                    description_data.append(xml_element)
            elif csv_attr in row.keys():
                xml_element = etree.Element(self.__csv_to_xml_desc_attrs[csv_attr])
                if 'price' in csv_attr:
                    xml_element.set('currency', row['currency'].value)
                    xml_element.text = row[csv_attr].value.replace(',', '.')
                elif csv_attr.endswith('weight'):
                    if not csv_attr + '_unit_of_measure' in row.keys():
                        continue
                    xml_element.set('unitOfMeasure', row[csv_attr + '_unit_of_measure'].value)
                else:
                    xml_element.text = row[csv_attr].value
                description_data.append(xml_element)
        product.append(description_data)

        product_data = etree.Element('ProductData')
        auto_accessory = etree.Element('AutoAccessory')
        product_type = etree.Element('ProductType')
        product_type_entry = etree.Element(row['feed_product_type'].value)
        complex_elements = []
        for csv_attr in self.__csv_to_xml_data_attrs:
            if csv_attr in row.keys():
                if '/' in self.__csv_to_xml_data_attrs[csv_attr]:
                    root_name, child_name = self.__csv_to_xml_data_attrs[csv_attr].split('/')
                    root_found = False
                    for child in complex_elements:
                        if child.tag == root_name:
                            root_element = child
                            root_found = True
                            break
                    if not root_found:
                        root_element = etree.Element(root_name)
                        complex_elements.append(root_element)
                    child_element = etree.Element(child_name)
                    child_element.text = row[csv_attr].value
                    root_element.append(child_element)
                else:
                    xml_element = etree.Element(self.__csv_to_xml_data_attrs[csv_attr])
                    xml_element.text = row[csv_attr].value
                    if csv_attr == 'amperage':
                        if not 'amperage_unit_of_measure' in row.keys():
                            continue
                        xml_element.set('unitOfMeasure', row['amperage_unit_of_measure'].value)
                    product_type_entry.append(xml_element)
        for element in complex_elements:
            if len(element) == 2:
                product_type_entry.append(element)
        product_type.append(product_type_entry)
        auto_accessory.append(product_type)
        product_data.append(auto_accessory)
        product.append(product_data)

        message.append(product)
        self.__product_amazon_envelope.append(message)
        self.__product_message_id += 1

        self.__add_pricing(row)
        self.__add_availability(row)

    def add_image(self, sku, image_link, image_number):
        message = etree.Element('Message')
        message_id = etree.Element('MessageID')
        message_id.text = str(self.__image_message_id)
        message.append(message_id)
        operation_type = etree.Element('OperationType')
        operation_type.text = 'Update'
        message.append(operation_type)

        product_image = etree.Element('ProductImage')
        sku_element = etree.Element('SKU')
        sku_element.text = sku
        product_image.append(sku_element)
        image_type = etree.Element('ImageType')
        image_type.text = 'Main' if image_number == 0 else 'PT%d' % image_number
        product_image.append(image_type)
        image_location = etree.Element('ImageLocation')
        image_location.text = image_link
        product_image.append(image_location)

        message.append(product_image)
        self.__image_amazon_envelope.append(message)
        self.__image_message_id += 1

    def __add_pricing(self, row):
        message = etree.Element('Message')
        message_id = etree.Element('MessageID')
        message_id.text = str(self.__pricing_message_id)
        message.append(message_id)
        operation_type = etree.Element('OperationType')
        operation_type.text = 'Update'
        message.append(operation_type)

        price = etree.Element('Price')
        sku = etree.Element('SKU')
        sku.text = row['item_sku'].value
        price.append(sku)
        standard_price = etree.Element('StandardPrice')
        standard_price.set('currency', row['currency'].value)
        standard_price.text = row['standard_price'].value.replace(',', '.')
        price.append(standard_price)

        if 'sale_price' in row.keys() and 'sale_from_date' in row.keys() and 'sale_end_date' in row.keys():
            sale = etree.Element('Sale')
            start_date = etree.Element('StartDate')
            start_date.text = row['sale_from_date'].value.replace('.', '-') + 'T00:00:00'
            end_date = etree.Element('EndDate')
            end_date.text = row['sale_end_date'].value.replace('.', '-') + 'T00:00:00'
            sale.append(end_date)
            sale_price = etree.Element('SalePrice')
            sale_price.set('currency', row['currency'])
            sale_price.text = row['sale_price'].value.replace(',', '.')
            sale.append(sale_price)
            price.append(sale)

        message.append(price)
        self.__pricing_amazon_envelope.append(message)
        self.__pricing_message_id += 1

    def __add_availability(self, row):
        message = etree.Element('Message')
        message_id = etree.Element('MessageID')
        message_id.text = str(self.__pricing_message_id)
        message.append(message_id)
        operation_type = etree.Element('OperationType')
        operation_type.text = 'Update'
        message.append(operation_type)

        inventory = etree.Element('Inventory')
        sku = etree.Element('SKU')
        sku.text = row['item_sku'].value
        inventory.append(sku)

        if 'fulfillment_center_id' in row.keys():
            fulfillment_center_id = etree.Element('FulfillmentCenterID')
            fulfillment_center_id.text = row['fulfillment_center_id'].value
            inventory.append(fulfillment_center_id)

        quantity = etree.Element('Quantity')
        quantity.text = row['quantity'].value
        inventory.append(quantity)

        if 'restock_date' in row.keys():
            restock_date = etree.Element('RestockDate')
            restock_date.text = row['restock_date'].replace('.', '-') + 'T00:00:00'.value
            inventory.append(restock_date)

        if 'fulfillment_latency' in row.keys():
            fulfillment_latency = etree.Element('FulfillmentLatency')
            fulfillment_latency.text = row['fulfillment_latency'].value
            inventory.append(fulfillment_latency)

        message.append(inventory)
        self.__availability_amazon_envelope.append(message)
        self.__availability_message_id += 1