import requests
import boto3
import json
import pprint


SECRET_NAME = 'fitbit'
REGION_NAME = 'us-west-1'


def get_secret(region_name: str, secret_name: str) -> dict:
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    secret_value = client.get_secret_value(SecretId=secret_name)
    secret_string = secret_value['SecretString']
    secret = json.loads(secret_string)
    return secret


def update_secret(region_name: str, secret_name: str, secret_key_pair: str) -> dict:
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    response = client.update_secret(
        SecretId=secret_name,
        SecretString=secret_key_pair
    )
    return response


def main():

    # Get secret
    secret = get_secret(REGION_NAME, SECRET_NAME)
    access_token = secret['access-token']
    encoded_id = secret['encoded-id']
    refresh_token = secret['refresh-token']
    authorization_basic = secret['authorization-basic']

    # Try using current access token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(f'https://api.fitbit.com/1/user/{encoded_id}/profile.json', headers=headers)
    pprint.pprint(response.json())

    # Refresh token
    headers = {
        'Authorization': f'Basic {authorization_basic}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post('https://api.fitbit.com/oauth2/token', headers=headers, data=data)
    response_json = response.json()
    pprint.pprint(response_json)

    # Update AWS Secrets Manger
    new_access_token = response_json['access_token']
    new_refresh_token = response_json['refresh_token']
    secret_key_pair = f'{{' \
                      f'"access-token": "{new_access_token}", ' \
                      f'"refresh-token": "{new_refresh_token}", ' \
                      f'"encoded-id": "{encoded_id}", ' \
                      f'"authorization-basic": "{authorization_basic}"' \
                      f'}}'
    response = update_secret(
        region_name=REGION_NAME,
        secret_name=SECRET_NAME,
        secret_key_pair=secret_key_pair
    )
    pprint.pprint(response)


if __name__ == '__main__':
    main()

