from django.apps import AppConfig


class AmazonConfig(AppConfig):
    name = 'apps.online_shops.amazon'
    #default_permissions = ['is_staff']
    verbose_name = 'Amazon sync application'

application = AmazonConfig
