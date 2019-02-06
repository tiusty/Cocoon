# Third party imports
from storages.backends.s3boto3 import S3Boto3Storage
from django.contrib.staticfiles.storage import ManifestFilesMixin

# Settings import
from config.settings.production import AWS_STATIC_LOCATION, AWS_PUBLIC_MEDIA_LOCATION


# Determines the storage location for static files
class StaticStorage(ManifestFilesMixin, S3Boto3Storage):
    location = AWS_STATIC_LOCATION


# Determines the storage location for public media files
class PublicMediaStorage(S3Boto3Storage):
    location = AWS_PUBLIC_MEDIA_LOCATION
    file_overwrite = False
