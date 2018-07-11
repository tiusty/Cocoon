from .local import *


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cocoon',
        'USER': 'cocoon_dev',
        'PASSWORD': 'cocoon_pass',
        'HOST': 'localhost',
        'PORT': '',
    }
}
