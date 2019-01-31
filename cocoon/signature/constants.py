from django.conf import settings

# Docusign account variables
REDIRECT_URI = "https://bostoncocoon.com"

# Docusign variables dependent on settings file
if not settings.DEBUG:
    OAUTH_BASE_URL = "account-d.docusign.com" # use account.docusign.com for Live/Production
    BASE_URL = "https://demo.docusign.net/restapi"
    USER_ID = "4d882612-2587-4842-b32b-8d7e24458aba"
    ACCOUNT_ID = "6769317"
    INTEGRATOR_KEY = "37951692-e5fe-4e15-af79-9183ac019a57"
    DOCUSIGN_KEY = "DOCUSIGN_PRIVATE_KEY_DEV"
    AUTHENTICATION_VALUE=""

    # Templates in dev
    PRE_TOUR_TEMPLATE_ID = 'e998b44f-28cb-4d20-ad67-97a033cbbab1'
else:
    OAUTH_BASE_URL = "account.docusign.com"
    INTEGRATOR_KEY = "37951692-e5fe-4e15-af79-9183ac019a57"
    ACCOUNT_ID = "42932310"
    USER_ID = "60c09393-42c2-4319-a6fe-92d345e4540c"
    BASE_URL = "https://na3.docusign.net/restapi"
    DOCUSIGN_KEY = "DOCUSIGN_PRIVATE_KEY_PROD"
    AUTHENTICATION_VALUE = "Mzc5NTE2OTItZTVmZS00ZTE1LWFmNzktOTE4M2FjMDE5YTU3OmFiZDViYjI0LWRmMjctNDEwYS1hYTk3LWQzOTUwZGJhNDk0NQ=="

    # Templates in prod
    PRE_TOUR_TEMPLATE_ID = '161b9cfd-42e7-44ed-b1e4-f3e2b070c13e'


# Docusign api throttle
# They don't allow refreshs faster than 15 minutes.
# We set it to 16 to be safe
DOCUSIGN_REFRESH_RATE_MINUTES = 16
