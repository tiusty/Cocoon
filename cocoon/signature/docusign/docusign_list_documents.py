# Import Docusign Modules
import docusign_esign as docusign
from docusign_esign import AuthenticationApi, TemplatesApi, EnvelopesApi
from docusign_esign.rest import ApiException

# Import third party modules
from pprint import pprint

# Import Cocoon modules
from cocoon.signature.docusign.docusign_base import DocusignLogin

# Import Cocoon constants
from cocoon.signature.constants import ACCOUNT_ID

# Load the logger
import logging
logger = logging.getLogger(__name__)


class DocusignWrapper(DocusignLogin):

    def __init__(self):
        super().__init__()
        self.set_up_docusign_api()
        self.account_id = ACCOUNT_ID

    def list_documents(self, envelope_id):

        auth_api = AuthenticationApi()
        envelopes_api = EnvelopesApi()

        try:
            login_info = auth_api.login()
            assert login_info is not None
            assert len(login_info.login_accounts) > 0
            login_accounts = login_info.login_accounts
            assert login_accounts[0].account_id is not None

            base_url, _ = login_accounts[0].base_url.split('/v2')
            self.api_client.host = base_url
            docusign.configuration.api_client = self.api_client

            docs_list = envelopes_api.list_documents(login_accounts[0].account_id, self.envelope_id)
            assert docs_list is not None
            assert (docs_list.envelope_id == envelope_id)

            print("EnvelopeDocumentsResult: ", end="")
            # pprint(docs_list)

            # The status of whether or not it is signed can be retrieved from here
            # print(envelopes_api.get_envelope(account_id, envelope_id))

            # Lists recipients of an envelope and you can check whether or not it has been signed
            print(envelopes_api.list_recipients(self.account_id, envelope_id))

        except ApiException as e:
            print("\nException when calling DocuSign API: %s" % e)
            assert e is None  # make the test case fail in case of an API exception

    def send_document_for_signatures(self, template_id, email, user_full_name):

        # Create the role name
        template_role_name = 'Needs to sign'

        # create an envelope to be signed
        envelope_definition = docusign.EnvelopeDefinition()
        envelope_definition.email_subject = 'Please Sign the Cocoon Documents'
        envelope_definition.email_blurb = 'Hello, Please sign my Cocoon Documents.'

        # assign template information including ID and role(s)
        envelope_definition.template_id = template_id

        # create a template role with a valid template_id and role_name and assign signer info
        t_role = docusign.TemplateRole()
        t_role.role_name = template_role_name
        t_role.name = user_full_name
        t_role.email = email

        # create a list of template roles and add our newly created role
        # assign template role(s) to the envelope
        envelope_definition.template_roles = [t_role]

        # send the envelope by setting |status| to "sent". To save as a draft set to "created"
        envelope_definition.status = 'sent'

        auth_api = AuthenticationApi()
        envelopes_api = EnvelopesApi()

        try:
            login_info = auth_api.login(api_password='true', include_account_id_guid='true')
            assert login_info is not None
            assert len(login_info.login_accounts) > 0
            login_accounts = login_info.login_accounts
            assert login_accounts[0].account_id is not None

            base_url, _ = login_accounts[0].base_url.split('/v2')
            self.api_client.host = base_url
            docusign.configuration.api_client = self.api_client

            envelope_summary = envelopes_api.create_envelope(login_accounts[0].account_id, envelope_definition=envelope_definition)
            assert envelope_summary is not None
            assert envelope_summary.envelope_id is not None
            assert envelope_summary.status == 'sent'

            print("EnvelopeSummary: ", end="")
            pprint(envelope_summary)
            return envelope_summary.envelope_id

        except ApiException as e:
            print("\nException when calling DocuSign API: %s" % e)
            assert e is None # make the test case fail in case of an API exception
            return None

    def determine_is_signed(self, envelope_id):

        envelopes_api = EnvelopesApi()

        try:
            if envelopes_api.list_recipients(self.account_id, envelope_id).signers[0].status == 'completed':
                return True
            else:
                return False

        except ApiException as e:
            logger.warning("\nException when calling DocuSign API: %s" % e)
            return False





