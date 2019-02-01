from django.conf import settings

from config.settings.base import get_secret

# Docusign account variables
REDIRECT_URI = "https://bostoncocoon.com"

# Docusign variables dependent on settings file
if settings.DEBUG:
    OAUTH_BASE_URL = get_secret("OAUTH_BASE_URL_DEV")
    BASE_URL = get_secret('BASE_URL_DEV')
    USER_ID = get_secret('USER_ID_DEV')
    ACCOUNT_ID = get_secret('ACCOUNT_ID_DEV')
    INTEGRATOR_KEY = get_secret('INTEGRATOR_KEY_DEV')
    DOCUSIGN_KEY = "DOCUSIGN_PRIVATE_KEY_DEV"
    AUTHENTICATION_VALUE = get_secret('AUTHENTICATION_VALUE_DEV')

    # Templates in dev
    PRE_TOUR_TEMPLATE_ID = 'e998b44f-28cb-4d20-ad67-97a033cbbab1'
else:
    OAUTH_BASE_URL = get_secret("OAUTH_BASE_URL_PROD")
    BASE_URL = get_secret('BASE_URL_PROD')
    USER_ID = get_secret('USER_ID_PROD')
    ACCOUNT_ID = get_secret('ACCOUNT_ID_PROD')
    INTEGRATOR_KEY = get_secret('INTEGRATOR_KEY_PROD')
    DOCUSIGN_KEY = "DOCUSIGN_PRIVATE_KEY_PROD"

    # Authentication value is needed for production
    AUTHENTICATION_VALUE = get_secret('AUTHENTICATION_VALUE_PROD')

    # Templates in prod
    PRE_TOUR_TEMPLATE_ID = '161b9cfd-42e7-44ed-b1e4-f3e2b070c13e'


# Docusign api throttle
# They don't allow refreshs faster than 15 minutes.
# We set it to 16 to be safe
DOCUSIGN_REFRESH_RATE_MINUTES = 16
