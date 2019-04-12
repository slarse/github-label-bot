import json
from jwcrypto import jwk
import python_jwt
import os
import boto3
import botocore
from labelbot import auth
from labelbot import github_api
from labelbot import parse


def lambda_handler(event, context):
    body = json.loads(event["body"])
    installation_id = body["installation"]["id"]
    owner = body["repository"]["owner"]["login"]
    repo = body["repository"]["name"]
    issue_nr = body["issue"]["number"]
    issue_body = body["issue"]["body"]
    current_labels = [label["name"] for label in body["issue"]["labels"]]

    app_id = int(os.environ["APP_ID"])
    bucket_name = os.environ["BUCKET_NAME"]
    bucket_key = os.environ["BUCKET_KEY"]
    pem = get_pem(bucket_name, bucket_key)

    jwt_token = auth.generate_jwt_token(pem, app_id)
    access_token = auth.generate_installation_access_token(jwt_token, installation_id)

    success = github_api.set_allowed_labels(
        owner, repo, issue_nr, issue_body, current_labels, access_token
    )

    return {"statusCode": 200 if success else 403, "body": json.dumps("temp")}


def get_pem(bucket_name, key):
    """Reads key from s3"""
    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).download_file(key, "/tmp/key.pem")
    with open("/tmp/key.pem", "rb") as f:
        pem = f.read()
    return pem
