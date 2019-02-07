# Import Django modules
from django.contrib.staticfiles.storage import ManifestFilesMixin

# Third party imports
import os
from storages.backends.s3boto3 import S3Boto3Storage, SpooledTemporaryFile

# Settings import
from config.settings.production import AWS_STATIC_LOCATION, AWS_PUBLIC_MEDIA_LOCATION


# Determines the storage location for static files
class StaticStorage(ManifestFilesMixin, S3Boto3Storage):
    location = AWS_STATIC_LOCATION

    # This override is necessary due to a bug in S3-bucket django backend library
    #   From online
    def _save_content(self, obj, content, parameters):
        """
        We create a clone of the content file as when this is passed to boto3 it wrongly closes
        the file upon upload where as the storage backend expects it to still be open
        """
        # Seek our content back to the start
        content.seek(0, os.SEEK_SET)

        # Create a temporary file that will write to disk after a specified size
        content_autoclose = SpooledTemporaryFile()

        # Write our original content into our copy that will be closed by boto3
        content_autoclose.write(content.read())

        # Upload the object which will auto close the content_autoclose instance
        super(StaticStorage, self)._save_content(obj, content_autoclose, parameters)

        # Cleanup if this is fixed upstream our duplicate should always close
        if not content_autoclose.closed:
            content_autoclose.close()


# Determines the storage location for public media files
class PublicMediaStorage(S3Boto3Storage):
    location = AWS_PUBLIC_MEDIA_LOCATION
    file_overwrite = False
