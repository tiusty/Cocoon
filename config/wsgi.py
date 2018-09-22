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

# Opens the secrets file and loads the values
with open(os.path.expanduser("~") + '/work/Cocoon/config/settings/secrets.json') as f:
        secrets = json.loads(f.read())


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
