# Import Docusign Modules
import docusign_esign as docusign
from docusign_esign import AuthenticationApi, TemplatesApi, EnvelopesApi
from docusign_esign.rest import ApiException

# Import Cocoon modules
from cocoon.signature.docusign.docusign_base import DocusignLogin

# Import Cocoon constants
from cocoon.signature.constants import ACCOUNT_ID


class DocusignListDocuments(DocusignLogin):

    def __init__(self):
        super().__init__()
        self.set_up_docusign_api()
        self.account_id = ACCOUNT_ID
        self.envelope_id = "3b87405b-4988-4f42-a984-9c0bb6048c4b"

    def list_documents(self):

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
            assert (docs_list.envelope_id == self.envelope_id)

            print("EnvelopeDocumentsResult: ", end="")
            # pprint(docs_list)

            # The status of whether or not it is signed can be retrieved from here
            # print(envelopes_api.get_envelope(account_id, envelope_id))

            # Lists recipients of an envelope and you can check whether or not it has been signed
            print(envelopes_api.list_recipients(self.account_id, self.envelope_id))

        except ApiException as e:
            print("\nException when calling DocuSign API: %s" % e)
            assert e is None  # make the test case fail in case of an API exception




