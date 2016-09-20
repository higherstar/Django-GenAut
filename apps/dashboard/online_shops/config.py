from django.apps import AppConfig


class OnlineShopsConfig(AppConfig):
    name = 'apps.dashboard.online_shops'
    default_permissions = ['is_staff']
    verbose_name = 'Online shops sync dashboard interface'
