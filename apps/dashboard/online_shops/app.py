from oscar.core.application import Application


class PricelistApplication(Application):
    name = 'apps.dashboard.online_shops'
    default_permissions = ['is_staff']
    verbose_name = 'Online shops sync dashboard interface'

application = PricelistApplication()