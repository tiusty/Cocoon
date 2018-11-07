from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# Domains that are allowed
ALLOWED_HOSTS = ['bostoncocoon.com', 'cocoonbeta.com', '127.0.0.1']

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bostonCocoonDatabaseStaging',
        'USER': 'bostoncocoon',
        'PASSWORD': 'Pr0jectUn!corn2018',
        'HOST': 'cocoonstagingdatabase.cqoopoxrcwhz.us-east-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}

# AWS configuration settings
# AWS_STORAGE_BUCKET_NAME = 'bostoncocoonstaging'
# AWS_ACCESS_KEY_ID = 'AKIAIL5BFKNQ6GZPNDWQ'
# AWS_SECRET_ACCESS_KEY = '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'
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
#
# AWS_STATIC_LOCATION = 'static'
# STATICFILES_STORAGE = 'config.storage_backends.StaticStorage'
# STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)
#
# AWS_PUBLIC_MEDIA_LOCATION = 'media/public'
# DEFAULT_FILE_STORAGE = 'config.storage_backends.PublicMediaStorage'
