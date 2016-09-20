"""
Django settings for GenAut project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from oscar import get_core_apps, OSCAR_MAIN_TEMPLATE_DIR
from oscar.defaults import *

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_PATH = BASE_DIR
location = lambda x: os.path.join(BASE_DIR, '..', x)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7*w#5(yh__(b)0m&e1u8l1#ldlemmbn!^x)57q^$0map+3fwxz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'oscar.apps.search.context_processors.search_form',
    'oscar.apps.promotions.context_processors.promotions',
    'oscar.apps.checkout.context_processors.checkout',
    'oscar.apps.customer.notifications.context_processors.notifications',
    'oscar.core.context_processors.metadata',
    'apps.customer.context_processors.forms_processor'
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder'
)

# Application definition
INSTALLED_APPS = [
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'compressor',
    'paypal',
    'nested_inline',
    'apps.dashboard.pricelist',
    'apps.online_shops.amazon',
    'apps.dashboard.online_shops',
    'apps.dashboard.menus',
    'widget_tweaks',
] + get_core_apps(
    [
        'apps.address',
        'apps.catalogue',
        'apps.checkout',
        'apps.promotions',
        'apps.partner',
        'apps.customer',
        'apps.dashboard.catalogue',
        'apps.dashboard.promotions',
        'apps.search',
    ]
)

SITE_ID = 1

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',

    'apps.address.middleware.LoginRequiredMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oscar.apps.basket.middleware.BasketMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'GenAut.urls'

WSGI_APPLICATION = 'GenAut.wsgi.application'

LOGIN_URL = '/login'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = location('GenAut/st')
MEDIA_ROOT = location('GenAut/media')
MEDIA_URL = '/media/'

TEMPLATE_DIRS = (
    location('GenAut/templates'),
    OSCAR_MAIN_TEMPLATE_DIR,
)
STATICFILES_DIRS = (
    location('GenAut/static'),
)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}


OSCAR_DASHBOARD_NAVIGATION[5] = {
    'label': 'Content',
    'icon': 'icon-folder-close',
    'children': [
        {
            'label': 'Content blocks',
            'url_name': 'dashboard:promotion-list',
        },
        {
            'label': 'Content blocks by page',
            'url_name': 'dashboard:promotion-list-by-page',
        },
        {
            'label': 'Pages',
            'url_name': 'dashboard:page-list',
        },
        {
            'label': 'Email templates',
            'url_name': 'dashboard:comms-list',
        },
        {
            'label': 'Reviews',
            'url_name': 'dashboard:reviews-list',
        },
        {
            'label': 'Menus',
            'url_name': 'menus:menu-list',
        }
    ]
}

OSCAR_DASHBOARD_NAVIGATION += [
    {
        'label': 'Import',
        'icon': 'icon-list',
        'children': [
            {
                'label': 'KBS vehicle fitment data',
                'url_name': 'apps.dashboard.pricelist.views.import_pricelist'
            },
            {
                'label': 'Import Products',
                'url_name': 'apps.dashboard.pricelist.views.import_products'
            },
        ]
    },
    {
        'label': 'Online shops sync',
        'icon': 'icon-list',
        'children': [
            {
                'label': 'Amazon',
                'url_name': 'apps.dashboard.online_shops.views.amazon_sync_view'
            },
        ]
    },
    {
        'label': 'PayPal',
        'icon': 'icon-globe',
        'children': [
            {
                'label': 'Express transactions',
                'url_name': 'paypal-express-list',
            },
        ]
    },
]

THUMBNAIL_DEBUG = True

OSCAR_ALLOW_ANON_CHECKOUT = True
OSCAR_PRODUCTS_PER_PAGE = 16


PAYPAL_API_USERNAME = 'artyom.smushkov-facilitator_api1.gmail.com'
PAYPAL_API_PASSWORD = 'SZZS555X98MA4RJG'
PAYPAL_API_SIGNATURE = 'AiPC9BjkCyDFQXbSkoZcgqH3hpacAj-oSqZkyzZ7.VsMKxl.ci9NEWjZ'
PAYPAL_CALLBACK_TIMEOUT = 30

try:
    from .local_settings import *
except ImportError:
    pass
