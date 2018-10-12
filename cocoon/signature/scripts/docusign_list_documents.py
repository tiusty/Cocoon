from cocoon.signature.docusign.docusign_list_documents import DocusignWrapper

print('hi')
list = DocusignWrapper('ebd91598-100d-4455-8b18-a2b83ae3a960')
if list.determine_is_signed():
    print('signed')
else:
    print('not signed')

# from __future__ import absolute_import, print_function
# from pprint import pprint
# import unittest
# import webbrowser
#
# import docusign_esign as docusign
# from docusign_esign import AuthenticationApi, TemplatesApi, EnvelopesApi
# from docusign_esign.rest import ApiException

# user_name = "awagud12@gmail.com"
# integrator_key = "37951692-e5fe-4e15-af79-9183ac019a57"
# base_url = "https://demo.docusign.net/restapi"
# oauth_base_url = "account-d.docusign.com" # use account.docusign.com for Live/Production
# redirect_uri = "https://bostoncocoon.com"
# private_key_filename = "docusign_private_key.txt"
# user_id = "4d882612-2587-4842-b32b-8d7e24458aba"
# template_id = "e998b44f-28cb-4d20-ad67-97a033cbbab1"
# envelope_id = "3b87405b-4988-4f42-a984-9c0bb6048c4b"
# account_id = "6769317"
#
# api_client = docusign.ApiClient(base_url)
#
# # IMPORTANT NOTE:
# # the first time you ask for a JWT access token, you should grant access by making the following call
# # get DocuSign OAuth authorization url:
# oauth_login_url = api_client.get_jwt_uri(integrator_key, redirect_uri, oauth_base_url)
# # open DocuSign OAuth authorization url in the browser, login and grant access
# # webbrowser.open_new_tab(oauth_login_url)
# print(oauth_login_url)
#
# # END OF NOTE
#
# # configure the ApiClient to asynchronously get an access token and store it
# api_client.configure_jwt_authorization_flow(private_key_filename, oauth_base_url, integrator_key, user_id, 3600)
#
# docusign.configuration.api_client = api_client
#
# auth_api = AuthenticationApi()
# envelopes_api = EnvelopesApi()
#
# try:
#     login_info = auth_api.login()
#     assert login_info is not None
#     assert len(login_info.login_accounts) > 0
#     login_accounts = login_info.login_accounts
#     assert login_accounts[0].account_id is not None
#
#     base_url, _ = login_accounts[0].base_url.split('/v2')
#     api_client.host = base_url
#     docusign.configuration.api_client = api_client
#
#     docs_list = envelopes_api.list_documents(login_accounts[0].account_id, envelope_id)
#     assert docs_list is not None
#     assert (docs_list.envelope_id == envelope_id)
#
#     print("EnvelopeDocumentsResult: ", end="")
#     # pprint(docs_list)
#
#     # The status of whether or not it is signed can be retrieved from here
#     # print(envelopes_api.get_envelope(account_id, envelope_id))
#
#     # Lists recipients of an envelope and you can check whether or not it has been signed
#     print(envelopes_api.list_recipients(account_id, envelope_id))
#
# except ApiException as e:
#     print("\nException when calling DocuSign API: %s" % e)
#     assert e is None  # make the test case fail in case of an API exception
#
#
# #