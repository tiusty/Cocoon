# Import Docusign Modules
import docusign_esign as docusign
from docusign_esign import AuthenticationApi, EnvelopesApi
from docusign_esign.rest import ApiException

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

        envelopes_api = EnvelopesApi()

        try:
            # Lists recipients of an envelope and you can check whether or not it has been signed
            print(envelopes_api.list_recipients(self.account_id, envelope_id))

        except ApiException as e:
            logger.error("\nException in {0} when calling DocuSign API: {1}"
                         .format(DocusignWrapper.list_documents.__name__,
                                 e))
            assert e is None  # make the test case fail in case of an API exception

    @staticmethod
    def send_document_for_signatures(template_id, email, user_full_name):
        """
        Creates a document for the user to sign

        :param template_id: (string) -> The docusign template to use for the documents
        :param email: (string) -> The user email to send the documents to
        :param user_full_name: (string) -> The full name of the user
        :return: (string|None) -> Returns either the envelope_id of the created documents or None if there was a failure
        """

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
            assert login_info is not None, "Login_info is None"
            assert len(login_info.login_accounts) > 0, "There are 0 accounts"
            login_accounts = login_info.login_accounts
            assert login_accounts[0].account_id is not None, "Account id is None"

            envelope_summary = envelopes_api.create_envelope(login_accounts[0].account_id,
                                                             envelope_definition=envelope_definition)
            assert envelope_summary is not None, "Envelope_summary is None"
            assert envelope_summary.envelope_id is not None, "Envelope id is None"
            assert envelope_summary.status == 'sent', "Envelop status != sent"

            logger.debug(envelope_summary)
            return envelope_summary.envelope_id

        except ApiException as e:
            logger.error("\nException when calling DocuSign API: %s" % e)
            return None

        except AssertionError as e:
            logger.error("\nAssertionError in {0}: {1}".format(DocusignWrapper.send_document_for_signatures.__name__,
                                                               e))
            return None

    def determine_is_signed(self, envelope_id):
        """
        Queries docusign for a particular envelope to see if the user signed it or not
        :param envelope_id: (String) -> The envelope_id of the document that is being checked
        :return: (boolean) -> True: The document is signed
                              False: The document is not signed or error
        """

        envelopes_api = EnvelopesApi()

        try:
            if envelopes_api.list_recipients(self.account_id, envelope_id).signers[0].status == 'completed':
                return True
            else:
                return False

        except ApiException as e:
            logger.error("\nException in {0} when calling DocuSign API: {1}"
                         .format(DocusignWrapper.determine_is_signed.__name__,
                                 e))
            return False

    def resend_envelope(self, envelope_id):
        """
        Resends the envelope to the user if they need it again (i.e they deleted it or something)

        :param envelope_id: (string) -> The envelope_id stored on docusign
        :return: (boolean) -> True: The document was successfully resent
                              False; The document was not able to be resent
        """
        envelopes_api = EnvelopesApi()

        try:
            # Add the signer (it is 1 since there should only be one signer per document)
            signer = docusign.Signer()
            # signer.email = "agudelo.a@gatech.edu"
            # signer.name = 'Alex Agudelo 2asdfsdf'
            signer.recipient_id = 1

            recipients = docusign.Recipients()
            recipients.signers = [signer]

            recipients_update_summary = envelopes_api.update_recipients(self.account_id, envelope_id,
                                                                        recipients=recipients,
                                                                        resend_envelope='true')
            assert recipients_update_summary is not None, "Recipients update summary is None"
            assert len(recipients_update_summary.recipient_update_results) > 0, "Length of recipient_update_results is " \
                                                                                "not >0"
            assert ("SUCCESS" == recipients_update_summary.recipient_update_results[0].error_details.error_code), \
                "The error code" \
                "was not success"
            print("RecipientsUpdateSummary: ", end="")
            return True

        except ApiException as e:
            logger.error("\nException in {0} when calling DocuSign API: {1}"
                         .format(DocusignWrapper.resend_envelope.__name__,
                                 e))
            return False
