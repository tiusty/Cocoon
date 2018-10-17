from __future__ import absolute_import, print_function
import docusign_esign as docusign

# Import constants
from cocoon.signature.constants import INTEGRATOR_KEY, BASE_URL, OAUTH_BASE_URL, REDIRECT_URI, PRIVATE_KEY_FILENAME, \
    USER_ID


class DocusignLogin(object):

    def __init__(self):
        self.integrator_key = INTEGRATOR_KEY
        self.base_url = BASE_URL
        self.oauth_base_url = OAUTH_BASE_URL
        self.redirect_uri = REDIRECT_URI
        self.private_key_filename = PRIVATE_KEY_FILENAME
        self.user_id = USER_ID

        self.api_client = None

    def set_up_docusign_api(self):
        api_client = docusign.ApiClient(self.base_url)
        oauth_login_url = api_client.get_jwt_uri(self.integrator_key, self.redirect_uri, self.oauth_base_url)

        # Print only needed for first time use
        # On first time put link into URL to allow permission
        # print(oauth_login_url)

        # configure the ApiClient to asynchronously get an access token and store it
        api_client.configure_jwt_authorization_flow(self.private_key_filename, self.oauth_base_url, self.integrator_key,
                                                    self.user_id, 3600)

        self.api_client = api_client
        docusign.configuration.api_client = api_client

