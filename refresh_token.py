import requests
import boto3
import base64
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


def refresh_access_token(
        refresh_token: str,
        basic_token: str
) -> dict:
    headers = {
        'Authorization': f'Basic {basic_token}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post('https://api.fitbit.com/oauth2/token', headers=headers, data=data)
    response_json = response.json()
    return response_json


def update_aws_secrets_manager(
        new_access_token: str,
        new_refresh_token: str,
        encoded_id: str,
        client_id: str,
        client_secret: str
) -> dict:
    secret_key_pair = f'{{' \
                      f'"access-token": "{new_access_token}", ' \
                      f'"refresh-token": "{new_refresh_token}", ' \
                      f'"encoded-id": "{encoded_id}", ' \
                      f'"client-id": "{client_id}", ' \
                      f'"client-secret": "{client_secret}"' \
                      f'}}'
    response = update_secret(
        region_name=REGION_NAME,
        secret_name=SECRET_NAME,
        secret_key_pair=secret_key_pair
    )
    return response


def main():

    # Get secret
    secret = get_secret(REGION_NAME, SECRET_NAME)
    access_token = secret['access-token']
    encoded_id = secret['encoded-id']
    refresh_token = secret['refresh-token']
    client_id = secret['client-id']
    client_secret = secret['client-secret']

    # Try using current access token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(f'https://api.fitbit.com/1/user/{encoded_id}/profile.json', headers=headers)
    print(f'Status code: {response.status_code}')
    pprint.pprint(response.json())

    # If access token is expired
    if response.status_code == 401 and response.json()['errors'][0]['errorType'] == 'expired_token':
        print('Access token expired')
        
        # Create basic token
        basic_token = base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()

        # Refresh token
        response_json = refresh_access_token(
            refresh_token=refresh_token,
            basic_token=basic_token
        )
        print(f'Refreshed access token')
        pprint.pprint(response_json)

        # Update AWS Secrets Manager
        new_access_token = response_json['access_token']
        new_refresh_token = response_json['refresh_token']
        response = update_aws_secrets_manager(
            new_access_token=new_access_token,
            new_refresh_token=new_refresh_token,
            encoded_id=encoded_id,
            client_id=client_id,
            client_secret=client_secret
        )
        print('Updated AWS Secrets Manager')
        pprint.pprint(response)


if __name__ == '__main__':
    main()

