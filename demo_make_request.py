"""
I can't paste my access token here, so instead I saved
my access token in AWS Secret Manager and retrieve it
by boto3. When you get your access token, ignore this
boto3 Secret Manger part, and paste your access token
to {access_token} in headers.
"""


import requests
import boto3
import json
import pprint


SECRET_NAME = 'fitbit'
REGION_NAME = 'us-west-1'


def get_secret(region_name: str, secret_name: str) -> dict:
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    secret_string = get_secret_value_response['SecretString']
    secret = json.loads(secret_string)
    return secret


def main():

    # Get access token saved in AWS Secret Manager
    secret = get_secret(region_name=REGION_NAME, secret_name=SECRET_NAME)
    access_token = secret['access-token']

    # Make HTTP requests to fitbit API
    url = 'https://api.fitbit.com/1/user/-/profile.json'
    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.request('GET', url, headers=headers, data=payload)
    pprint.pprint(response.json())


if __name__ == '__main__':
    main()
