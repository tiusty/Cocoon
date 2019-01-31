from django.conf import settings

# Docusign account variables
REDIRECT_URI = "https://bostoncocoon.com"

# Docusign variables dependent on settings file
if settings.DEBUG:
    OAUTH_BASE_URL = "account-d.docusign.com" # use account.docusign.com for Live/Production
    BASE_URL = "https://demo.docusign.net/restapi"
    USER_ID = "4d882612-2587-4842-b32b-8d7e24458aba"
    ACCOUNT_ID = "6769317"
    INTEGRATOR_KEY = "37951692-e5fe-4e15-af79-9183ac019a57"


# Template IDs
PRE_TOUR_TEMPLATE_ID = 'e998b44f-28cb-4d20-ad67-97a033cbbab1'
