from rets import Session
#
login_url = 'http://mlspin-dd.apps.retsiq.com/contact/rets/login'
username = 'AN5056'
password = 'izeh6e'
rets_client = Session(login_url, username, password=password, version="RETS/1.8", http_auth='basic')
rets_client.login()
search_results = rets_client.search(resource='RESI', resource_class='RN', dmql_query='(ListPrice=1200),(StandardStatus=ACT)')
system_data = rets_client.get_system_metadata()
print(system_data)


# from rets.client import RetsClient
#
# client = RetsClient(
#     login_url=login_url,
#     username=username,
#     password=password,
#     # Ensure that you are using the right auth_type for this particular MLS
#     # auth_type='basic',
#     # Alternatively authenticate using user agent password
#     user_agent=username,
#     user_agent_password=password,
# )

