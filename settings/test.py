from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test_websitedb',
        'USER': 'postgres',
        'PASSWORD': 'example',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}