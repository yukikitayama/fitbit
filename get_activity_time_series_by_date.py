import boto3
import requests
import json
import pprint


SECRET_NAME = 'fitbit'
REGION_NAME = 'us-west-1'
DATE = '2021-12-04'  # I ran this day by using running mode, so GPS should have worked
PERIOD = '1d'
# RESOURCE = 'steps'
# RESOURCE = 'calories'  # Calories burned
RESOURCE = 'distance'
RESPONSE_JSON = f'data/activity_time_series_{RESOURCE}_{DATE}.json'


def get_secret(region_name: str, secret_name: str) -> dict:
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    secret_value = client.get_secret_value(SecretId=secret_name)
    secret_string = secret_value['SecretString']
    secret = json.loads(secret_string)
    return secret


def main():

    # Get secret
    secret = get_secret(REGION_NAME, SECRET_NAME)
    access_token = secret['access-token']
    encoded_id = secret['encoded-id']

    # Get activity
    url = f'https://api.fitbit.com/1/user/{encoded_id}/activities/{RESOURCE}/date/{DATE}/{PERIOD}.json'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.request('GET', url, headers=headers)
    print('Response headers')
    pprint.pprint(response.headers)
    print()
    print('Response contents')
    pprint.pprint(response.json())
    print()

    # Save data
    with open(RESPONSE_JSON, 'w') as f:
        json.dump(response.json(), f, indent=2)
    print(f'Saved the data from fitbit API to {RESPONSE_JSON}')


if __name__ == '__main__':
    main()
