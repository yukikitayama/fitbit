import boto3
import requests
import json
import pprint


SECRET_NAME = 'fitbit'
REGION_NAME = 'us-west-1'
DATE = '2021-11-28'
RESPONSE_JSON = f'data/sleep_log_{DATE}.json'


def get_secret(region_name: str, secret_name: str) -> dict:
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    secret_string = get_secret_value_response['SecretString']
    secret = json.loads(secret_string)
    return secret


def main():

    # Get secrets
    secret = get_secret(region_name=REGION_NAME, secret_name=SECRET_NAME)
    access_token = secret['access-token']
    encoded_id = secret['encoded-id']

    # Get sleep log data by date
    url = f'https://api.fitbit.com/1.2/user/{encoded_id}/sleep/date/{DATE}.json'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.request('GET', url, headers=headers)
    print('Response headers')
    pprint.pprint(response.headers)
    print()
    print(f'Response contents')
    pprint.pprint(response.json())
    print()

    # Save data
    with open(RESPONSE_JSON, 'w') as outfile:
        json.dump(response.json(), outfile, indent=2)
    print(f'Saved the data from fitbit API to {RESPONSE_JSON}')


if __name__ == '__main__':
    main()
