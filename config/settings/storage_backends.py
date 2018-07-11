# Third party imports
from storages.backends.s3boto3 import S3Boto3Storage

# Settings import
from config.settings.production import AWS_STATIC_LOCATION, AWS_PUBLIC_MEDIA_LOCATION

class StaticStorage(S3Boto3Storage):
    location = AWS_STATIC_LOCATION

class PublicMediaStorage(S3Boto3Storage):
    location = AWS_PUBLIC_MEDIA_LOCATION
    file_overwrite = False
