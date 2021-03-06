"""
Django settings for suikerboontje_project project.

Generated by 'django-admin startproject' using Django 1.8.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
location = lambda x: os.path.join(os.path.dirname(os.path.realpath(__file__)), x)


from oscar.defaults import *

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'grrdb)ro5^_g2%cwh(o4v&r7&981=^n4u4yh*hf&lk)-rd7qh='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['suikerboon.sites.djangoeurope.com', ]


# Application definition
from oscar import get_core_apps

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

'''
STATIC_URL = '/static/'

SETTINGS_PATH = os.path.dirname(__file__)
PROJECT_PATH = os.path.join(SETTINGS_PATH, os.pardir)
PROJECT_PATH = os.path.abspath(PROJECT_PATH)
TEMPLATES_PATH = os.path.join(PROJECT_PATH, "templates")
STATIC_ROOT  = os.path.join(PROJECT_PATH, "static")
MEDIA_ROOT = os.path.join(PROJECT_PATH, "media")
MEDIA_URL = "/media/"

PROJECT_ROOT = os.path.join(SETTINGS_PATH, os.pardir)

STATICFILES_DIRS = [
    os.path.join(SETTINGS_PATH, "static"),
]'''

SETTINGS_PATH = os.path.dirname(__file__)

# Absolute path to the directory that holds media.
# Example: "/home/username/projectname/media/"
MEDIA_ROOT = os.path.join(SETTINGS_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# The absolute path to the directory where collectstatic will collect static files for deployment.
# Example: "/home/username/projectname/static/"
STATIC_ROOT = os.path.join(SETTINGS_PATH, 'static')

# URL to use when referring to static files located in STATIC_ROOT.
# Examples: "/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# For static assets that arent't tied to a particular app. 
# In addition to using a static/ directory inside your apps, you can define a list of directories 
STATICFILES_DIRS = (
    os.path.join(SETTINGS_PATH, 'common_static'),
)


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    
    'compressor',
    'widget_tweaks',

    # third party
    'Crypto',
    'braces',

    # custom apps
    'custom',


] + get_core_apps(['myapps.checkout', 'myapps.partner', 'myapps.basket'])
#] + get_core_apps(['myapps.checkout'])

SITE_ID = 1


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'oscar.apps.basket.middleware.BasketMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'suikerboontje_project.urls'

from oscar import OSCAR_MAIN_TEMPLATE_DIR

PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            location('templates'),
            #os.path.join(BASE_DIR, 'templates'),
            #os.path.join(OSCAR_MAIN_TEMPLATE_DIR, 'templates'),
            OSCAR_MAIN_TEMPLATE_DIR
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.core.context_processors.media",
                "django.core.context_processors.static",

                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.promotions.context_processors.promotions',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.apps.customer.notifications.context_processors.notifications',
                'oscar.core.context_processors.metadata',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

WSGI_APPLICATION = 'suikerboontje_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'nl-be'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Hidden Oscar features, e.g. wishlists or reviews
OSCAR_HIDDEN_FEATURES = ['reviews', 'wishlists',]

# Menu structure of the dashboard navigation
OSCAR_DASHBOARD_NAVIGATION = [
    {
        'label': _('Dashboard'),
        'icon': 'icon-th-list',
        'url_name': 'dashboard:index',
    },
    {
        'label': _('Catalogue'),
        'icon': 'icon-sitemap',
        'children': [
            {
                'label': _('Products'),
                'url_name': 'dashboard:catalogue-product-list',
            },
            {
                'label': _('Product Types'),
                'url_name': 'dashboard:catalogue-class-list',
            },
            {
                'label': _('Categories'),
                'url_name': 'dashboard:catalogue-category-list',
            },
#            {
#                'label': _('Ranges'),
#                'url_name': 'dashboard:range-list',
#            },
#            {
#                'label': _('Low stock alerts'),
#                'url_name': 'dashboard:stock-alert-list',
#            },
        ]
    },
#    {
#        'label': _('Fulfilment'),
#        'icon': 'icon-shopping-cart',
#        'children': [
#            {
#                'label': _('Orders'),
#                'url_name': 'dashboard:order-list',
#            },
#            {
#                'label': _('Statistics'),
#                'url_name': 'dashboard:order-stats',
#            },
#            {
#                'label': _('Partners'),
#                'url_name': 'dashboard:partner-list',
#            },
            # The shipping method dashboard is disabled by default as it might
            # be confusing. Weight-based shipping methods aren't hooked into
            # the shipping repository by default (as it would make
            # customising the repository slightly more difficult).
            # {
            #     'label': _('Shipping charges'),
            #     'url_name': 'dashboard:shipping-method-list',
            # },
#        ]
#    },
    {
        'label': _('Customers'),
        'icon': 'icon-group',
        'children': [
            {
                'label': _('Customers'),
                'url_name': 'dashboard:users-index',
            },
            {
                'label': _('Stock alert requests'),
                'url_name': 'dashboard:user-alert-list',
            },
        ]
    },
#    {
#        'label': _('Offers'),
#        'icon': 'icon-bullhorn',
#        'children': [
#            {
#                'label': _('Offers'),
#                'url_name': 'dashboard:offer-list',
#            },
#            {
#                'label': _('Vouchers'),
#                'url_name': 'dashboard:voucher-list',
#            },
#        ],
#    },
    {
        'label': _('Content'),
        'icon': 'icon-folder-close',
        'children': [
            {
                'label': _('Content blocks'),
                'url_name': 'dashboard:promotion-list',
            },
            {
                'label': _('Content blocks by page'),
                'url_name': 'dashboard:promotion-list-by-page',
            },
            {
                'label': _('Pages'),
                'url_name': 'dashboard:page-list',
            },
            {
                'label': _('Email templates'),
                'url_name': 'dashboard:comms-list',
            },
#            {
#                'label': _('Reviews'),
#                'url_name': 'dashboard:reviews-list',
#            },
        ]
    },
#    {
#        'label': _('Reports'),
#        'icon': 'icon-bar-chart',
#        'url_name': 'dashboard:reports-index',
#    },
]

OSCAR_DEFAULT_CURRENCY = 'EUR'

OSCAR_SHOP_NAME = "'t Suikerboontje"

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s',
        },
        'simple': {
            'format': '[%(asctime)s] %(message)s'
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
    'handlers': {
        'file':{
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'temm.log',
            'formatter': 'verbose',
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'oscar': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'oscar.catalogue.import': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'oscar.alerts': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },

        # Django loggers
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'level': 'WARNING',
            'propagate': True,
        },
    }
}

# OSCAR SETTINGS

OSCAR_PRODUCTS_PER_PAGE = 24
OSCAR_RECENTLY_VIEWED_PRODUCTS = 10