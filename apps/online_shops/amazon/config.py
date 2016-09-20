from oscar.core.application import Application


class PricelistApplication(Application):
    name = 'apps.online_shops.amazon'
    default_permissions = ['is_staff']
    verbose_name = 'Amazon sync application'

application = PricelistApplication()
