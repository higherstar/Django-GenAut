from ebaysdk.trading import Connection as Trading
from ebaysdk.shopping import Connection as Shopping
from ebaysdk.exception import ConnectionError
from oscar.apps.partner.models import StockRecord
from apps.online_shops.ebay.models import ProductEbayId


name = 'Key Set 1'
dev_id = '076c1c91-4517-481a-a710-0b11fd433496'
app_id = 'ArtyomSm-a740-45ee-92b4-a5f2ff8677de'
cert_id = '56d14b70-36b7-4751-abb6-81529e973701'
user_token = 'AgAAAA**AQAAAA**aAAAAA**U/dyVQ**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFk4GhDZeEqA2dj6x9nY+seQ**w3gDAA**AAMAAA**Joy103MCO/WQBDVJvdep1PfXX0y0B762KDNKHdMonouN/A+70cEIQaTdgQDbq3TrWp0ypdwFzwsUn2yehZisOeBmJNpONxGVaUt5lbHj1xrKyJI3P4fwHhhJHlUN3FkP7ryU8cNxYOM1BNphwX02eEiCt0o2OS2XK6G04SeL2Kwgg22m1PzBSme4ID3x54gA0eKpkvj/WcG8YQY6Uqs53n36D4mARYe3/A/M0nx1sOsG1dCd0EY8I8u/VA0Ie2R0mvWHPO9+uxKpJtBeaLhR7ibUKUBUwTuX4XQKqRkdWcFfbyIg3sNVOivD2vU1G+TLT1MfQ5g5Lyd9ETvunZGSFEJE+1Od1mgULSwQJ2h6TEJIwJDQeXhefE9w5seL1PP6QUVGbnjIir8USVs3OKd0UFbkheNKg+6HVlOK2ARwvvgIYYr4QGhwmQXZ3EcKOFPfQySURYRrrfwbWA8Et+d9kqZ7y3w/3iY79guP8Olu7krkoQFEL9cfn4ssjr0qfavarpNRhL2Jl9c/APD/YUsw3L4kB0gC1YNMyeIpXpQfxOC+0wFBD90f9BSEWkCxQWSV58gWMK3N2ftIuQQHszJc2oGNBIOXZVKg0aea2W0OykTaiW0/jH7LSbcFmgGIgHEC+Tg1MayFrrJrX3V/CLpoT2UV8f8hRE/LkjZedGlNZlGkgFj/r9e94UicOvHdQv8iwRqcwKeTeXJ0aL5dCK27TzY8V335wSHiCN3japkdKLpeW7uVcYBWbntFiiBEIwc1'


class EbaySync:
    def __init__(self):
        self.trading_api = Trading(domain='api.sandbox.ebay.com', debug=True, config_file=None, appid=app_id,
                          certid=cert_id, devid=dev_id, token=user_token, site_id=3, warnings=False)
        self.trading_api.config.values['siteid'] = 3
        self.shopping_api = Shopping(domain='open.api.sandbox.ebay.com', debug=False, config_file=None, appid=app_id, site_id=3, warnings=False)
        self.shopping_api.config.values['siteid'] = 3

    def upload_product(self, product):
        my_item = self.product_to_dict(product)
        try:
            if hasattr(product, 'ebay_id'):
                my_item['Item']['ItemID'] = product.ebay_id.ebay_id
                item_status_response = self.shopping_api.execute('GetItemStatus', {'ItemID': my_item['Item']['ItemID']})
                if item_status_response.reply.Item.ListingStatus == 'Active':
                    self.trading_api.execute('ReviseItem', my_item)
                else:
                    self.trading_api.execute('RelistItem', my_item)
            else:
                add_item_response = self.trading_api.execute('AddItem', my_item)
                product_ebay_id = ProductEbayId(product=product, ebay_id=add_item_response.reply.ItemID)
                product_ebay_id.save()
        except ConnectionError as e:
            print(e)
            print(e.response.dict())
            raise Exception

    @staticmethod
    def product_to_dict(product):
        stock_record = StockRecord.objects.filter(product=product).first()
        condition_ids = {
            'New': '1000',
            'New other': '1500',
            'New with defects': '1750',
            'Manufacturer refurbished': '2000',
            'Seller refurbished': '2500',
            'Used': '3000',
            'Very Good': '4000',
            'Good': '5000',
            'Acceptable': '6000',
            'For parts of not working': '7000'
        }
        category_ids = {
            'Car bulbs': '174060',
        }
        database_to_ebay_attrs = {
            'voltage': 'Voltage',
            'wattage': 'Wattage',
            'brand_name': 'Brand',
            'part_number': 'Manufacturer Part Number',
        }

        key_features = [attr_value.value_text for attr_value in product.attribute_values.filter(attribute__code__startswith='bullet_point').order_by('attribute__code')]
        features_text = '<h3>Features</h3><ul><li>' + '</li><li>'.join([feature for feature in key_features if feature != '']) + '</li></ul>'

        item_specifics = []
        for attr_value in product.attribute_values.all():
            attr_code = attr_value.attribute.code
            for database_attr_code in database_to_ebay_attrs.keys():
                if database_attr_code == attr_code:
                    item_specifics.append({
                        'NameValueList': {
                            'Name': database_to_ebay_attrs[database_attr_code],
                            'Value': attr_value.value_text,
                        }
                    })

        res = {
            'Item': {
                   'Title': product.title if len(product.title) < 80 else product.title[:76] + ' ...',
                   'Description': '<![CDATA[' + product.description + features_text + ']]>',
                   'ConditionID': condition_ids['New'],
                   'Site': 'UK',
                   'Country': 'GB',
                   'PrimaryCategory': {
                       'CategoryID': category_ids['Car bulbs'],   #TODO choose the category
                   },
                   'PictureDetails': {
                       'PictureURL': [image.url.replace('https', 'http') for image in product.original_images.order_by('display_order')]
                   },
                   'StartPrice': str(stock_record.price_excl_tax),
                   'Currency': 'GBP',                 #TODO
                   #'Location': 'Blabla, UK',
                   'PaymentMethods': 'PayPal',
                   'PayPalEmailAddress': 'dave@theimip.com',
                   'Quantity': stock_record.num_in_stock,
                   'ListingType': 'FixedPriceItem',
                   'ListingDuration': 'GTC',
                   'PostalCode': 'BN68AR',
                   'ReturnPolicy': {
                       'ReturnsAcceptedOption': 'ReturnsAccepted',
                       'RefundOption': 'MoneyBack',
                       'ReturnsWithinOption': 'Days_14',
                       'Description': 'Returns accepted if goods can be retuned within 14 days from receipt. goods must be unused with original packaging in sellable condition',
                       'ShippingCostPaidByOption': 'Buyer',
                   },
                   'ShippingDetails': {
                       'ShippingType': 'Flat',
                       'ShippingServiceOptions': {
                           'ShippingServicePriority': '1', #TODO check if it's applicable when Dave replies about shipping type
                           'ShippingService': 'UK_RoyalMailSecondClassStandard',
                           'ShippingServiceCost': '6.99',
                       }
                   }
            }
        }
        if len(item_specifics) != 0:
            res['Item']['ItemSpecifics'] = item_specifics

        '''if product.compatibilities.count() != 0:
            res['Item']['ItemCompatibilityList'] = {'Type': 'NameValue'}
            res['Item']['ItemCompatibilityList']['Compatibility'] = []
            for comp in product.compatibilities.all():
                res['Item']['ItemCompatibilityList']['Compatibility'].append({
                    'NameValueList': [
                        {
                            'Name': 'Car Make',
                            'Value': comp.vehicle_type.vehicle_model.vehicle_brand.vehicle_brand
                        },
                        {
                            'Name': 'Model',
                            'Value': comp.vehicle_type.vehicle_model.vehicle_model
                        },
                        {
                            'Name': 'Variant',
                            'Value': comp.vehicle_type.vehicle_type
                        }
                    ]
                })'''

        return res