from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Domains that are allowed
ALLOWED_HOSTS = ['52.14.25.81', '127.0.0.1', 'bostoncocoon.com', 'kakun.us', 'cocoonboston.com', 'localhost']

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cocoon',
        'USER': 'cocoon_dev',
        'PASSWORD': 'cocoon_pass',
        'HOST': 'localhost',
        'PORT': '',
    }
}

