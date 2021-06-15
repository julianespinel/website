from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'TEST': {
            'NAME': 'test_websitedb',
        },
    }
}

# Default admin

DEFAULT_ADMIN_EMAIL = 'test@test.com'
DEFAULT_ADMIN_USERNAME = 'test'
DEFAULT_ADMIN_PASSWORD = 'test'
