"""
WSGI config for Unicorn project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from config.settings.base import get_secret
from config.keys.keys_filepaths import KEY_FILE_PATHS

# Tests loading all the keys to make sure they exists (does not verify that they are valid)
for key, path in KEY_FILE_PATHS.items():
    assert os.path.exists(path), "File: {0} does not exist at path {1}".format(key, path)

# Loads the settings file via the secrets file settings
os.environ["DJANGO_SETTINGS_MODULE"] = get_secret('DJANGO_SETTINGS_MODULE')

application = get_wsgi_application()
