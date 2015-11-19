from settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

FORCE_SCRIPT_NAME = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'claestim_suikerboontje',
        #'NAME': 'claestim_suikerboon_v01',
        'USER': 'claestim',
        'PASSWORD': 'LjC7XZgqGtx2',
        'HOST': '',
        'PORT': '',
    }
}
