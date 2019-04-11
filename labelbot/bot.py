import json
from jwcrypto import jwk
import python_jwt
import os
import boto3
import botocore
import labelbot.auth as auth
import labelbot.github_api as github_api




def get_pem(bucket_name, key):
    """Reads key from s3"""
    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).download_file(key, '/tmp/key.pem')
    with open('/tmp/key.pem', "rb") as f:
        pem = f.read()
    return pem


def lambda_handler(event, context):
    # TODO implement
    
    body = json.loads(event["body"])
    installation_id = body['installation']['id']
    owner = body['repository']['owner']['login']
    repo = body['repository']['name']
    number = body['issue']['number']
    issue_url = body['issue']['url']
    issue_body = body['issue']['body']

    app_id = int(os.environ['APP_ID'])
    bucket_name = os.environ['BUCKET_NAME']
    bucket_key = os.environ['BUCKET_KEY']
    pem = files.get_pem(bucket_name, bucket_key)



    return {"statusCode": 200, "body": json.dumps("temp")}


