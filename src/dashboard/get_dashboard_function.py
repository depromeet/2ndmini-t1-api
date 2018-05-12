import os
import boto3
import json
import datetime
from operator import itemgetter
from botocore.vendored import requests

ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')

s3 = boto3.client('s3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY)


def lambda_handler(event, context):
    
    # bucket name & file
    bucket = os.environ.get('BUCKET')
    key = os.environ.get('KEY_FILE')
        
    try:
        data = s3.get_object(Bucket=bucket, Key=key)
        json_data = json.loads(data['Body'].read().decode('utf-8'))
        
        # Order by score
        res_data = sorted(json_data["data"], key=itemgetter('score'), reverse=True)
        
        # response
        return {
            "timestamp":json_data["timestamp"],
            "data":res_data[:5]
        }
    
    except Exception as e:
        print(e)
        raise e