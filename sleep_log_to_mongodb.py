import pandas as pd
import requests
from pymongo import MongoClient
import boto3
from datetime import datetime
import json
import time


SECRET_NAME_01 = 'fitbit'
SECRET_NAME_02 = 'mongodb-website'
REGION_NAME = 'us-west-1'
START = datetime(2021, 12, 1)
END = datetime(2021, 12, 31)  # Inclusive
SLEEP = 3  # Sleep 3 seconds
DATABASE = 'fitbit'
COLLECTION = 'sleep-log'


def get_secret(region_name: str, secret_name: str) -> dict:
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    secret_string = get_secret_value_response['SecretString']
    secret = json.loads(secret_string)
    return secret


def get_sleep_log_by_date(
        date: str,
        encoded_id: str,
        access_token: str
) -> dict:
    url = f'https://api.fitbit.com/1.2/user/{encoded_id}/sleep/date/{date}.json'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.request('GET', url, headers=headers)
    print(f'  Status code: {response.status_code}')
    return response.json()


def main():

    # Get secrets
    secret_fitbit = get_secret(region_name=REGION_NAME, secret_name=SECRET_NAME_01)
    access_token = secret_fitbit['access-token']
    encoded_id = secret_fitbit['encoded-id']
    secret_mongodb = get_secret(region_name=REGION_NAME, secret_name=SECRET_NAME_02)
    cluster = secret_mongodb['mongodb-cluster']
    username = secret_mongodb['mongodb-username']
    password = secret_mongodb['mongodb-password']

    # MongoDB client
    host = f'mongodb+srv://{username}:{password}@{cluster}/{DATABASE}?retryWrites=true&w=majority'
    client_mongo = MongoClient(host)
    db = client_mongo[DATABASE]
    collection = db[COLLECTION]

    # Date range
    dates = [d.strftime('%Y-%m-%d') for d in pd.date_range(start=START, end=END, freq='D')]
    for date in dates[:1]:

        print(f'Date: {date}')

        # Get sleep log data by date
        data = get_sleep_log_by_date(
            date=date,
            encoded_id=encoded_id,
            access_token=access_token
        )
        data['date'] = date

        # Upload it to MongoDB
        collection.insert_one(data)

        # Sleep
        print(f'Sleeping {SLEEP} seconds')
        time.sleep(SLEEP)


if __name__ == '__main__':
    main()
