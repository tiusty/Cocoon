from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Domains that are allowed
ALLOWED_HOSTS = ['bostoncocoon.com', 'cocoonboston.com']

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}
