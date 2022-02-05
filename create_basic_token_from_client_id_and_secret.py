"""
- When registering an application in fitbit and choose OAuth 2.0 application type to be Server, 
  it requires to include the Basic token to the authorization header of HTTP requests.
- It assumes the server application can store client ID and client secret securely, so it can use them for the HTTP requests.
- If the application registration is Client or Personal type, it doesn't need the the basic token,
  because it assumes that the application cannot safely store the client ID and secret.
"""


import base64
import pprint


client_id = 'ABC123'
client_secret = 'DEF456'
base64_encoded = 'QUJDMTIzOkRFRjQ1Ng=='

# Authorization header to the request includes the Basic token
basic_token = base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()
print(f'Is encoding successful: {basic_token == base64_encoded}')

headers = {
    'Authorization': f'Basic {basic_token}',
    'Content-Type': 'application/x-www-form-urlencoded',
}
print('headers')
pprint.pprint(headers)