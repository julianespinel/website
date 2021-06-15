from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'websitedb',
    }
}

# Google Analytics
GOOGLE_ANALYTICS_KEY = ''

# Default admin

DEFAULT_ADMIN_EMAIL = 'local@local.com'
DEFAULT_ADMIN_USERNAME = 'local'
DEFAULT_ADMIN_PASSWORD = 'local'
