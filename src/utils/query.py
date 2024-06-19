import os
from io import StringIO

import boto3
import dotenv
import pandas as pd

from utils.setup import *

dotenv.load_dotenv()

@verbose
def load_sql_response(response):
    csv_data = ''
    for event in response['Payload']:
        if 'Records' in event:
            records = event['Records']['Payload'].decode('utf-8')
            csv_data += records
    df = pd.read_csv(StringIO(csv_data))
    return df

@verbose
def set_aws_session(access_key, secret_key, region):
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )
    return session

@verbose
def set_s3_client(session):
    s3_client = session.client('s3')
    return s3_client

@verbose
def fetch_sql_data(sql_query, s3_client):
    response = s3_client.select_object_content(
        Bucket='YOUR_BUCKET_NAME',
        Key='YOUR_OBJECT_KEY',
        ExpressionType='SQL',
        Expression=sql_query,
        InputSerialization={
            'CSV': {
                'FileHeaderInfo': 'USE',
                'RecordDelimiter': '\n',
                'FieldDelimiter': ','
            }
        },
        OutputSerialization={
            'CSV': {}
        }
    )
        
    return response
