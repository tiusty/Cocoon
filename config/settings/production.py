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

AWS_STORAGE_BUCKET_NAME = 'bostoncocoon-assets'
AWS_S3_REGION_NAME = 'us-east-2'
AWS_ACCESS_KEY_ID = 'AKIAIL5BFKNQ6GZPNDWQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_STATIC_LOCATION = 'static'
STATICFILES_STORAGE = 'config.settings.storage_backends.StaticStorage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)

AWS_PUBLIC_MEDIA_LOCATION = 'media/public'
DEFAULT_FILE_STORAGE = 'config.settings.storage_backends.PublicMediaStorage'
