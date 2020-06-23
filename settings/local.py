from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'websitedb',
        'USER': 'websiteuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

# Google Analytics
GOOGLE_ANALYTICS_KEY = ''