from oscar.core.application import Application


class PricelistApplication(Application):
    name = 'apps.pricelist'
    default_permissions = ['is_staff']

application = PricelistApplication()