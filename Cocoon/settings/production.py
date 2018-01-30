from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
#TODO: Turn to False when the website goes public
DEBUG = True

# Domains that are allowed
ALLOWED_HOSTS = ['bostoncocoon.com', 'cocoonboston.com']

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bostonCocoonDatabase',
	'USER': 'bostoncocoon',
	'PASSWORD': 'Pr0jectUn!corn2018',
	'HOST': 'coocondatabase.cqoopoxrcwhz.us-east-2.rds.amazonaws.com',
	'PORT': '5432',
    }
}
