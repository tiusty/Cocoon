"""
WSGI config for Unicorn project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import json

from django.core.wsgi import get_wsgi_application
from django.core.exceptions import ImproperlyConfigured
from config.settings.base import BASE_DIR

from config.keys.keys_filepaths import KEY_FILE_PATHS

# Opens the secrets file and loads the values
with open(os.path.join(BASE_DIR, 'settings/secrets.json')) as f:
        secrets = json.loads(f.read())

# Tests loading all the keys to make sure they exists (does not verify that they are valid)
for key, path in KEY_FILE_PATHS.items():
    assert os.path.exists(path), "File: {0} does not exist at path {1}".format(key, path)


# Function loads a value from the secrets file
def get_secret(setting, secrets=secrets):
        try:
                return secrets[setting]
        except KeyError:
                        error_msg = 'Set the {0} environment variable'.format(setting)
                        raise ImproperlyConfigured(error_msg)


# Loads the settings file via the secrets file settings
os.environ["DJANGO_SETTINGS_MODULE"] = get_secret('DJANGO_SETTINGS_MODULE')

application = get_wsgi_application()
