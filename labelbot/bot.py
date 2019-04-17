import json
from jwcrypto import jwk
import python_jwt
import os
import boto3
import botocore
import hmac
import hashlib
from labelbot import auth
from labelbot import github_api
from labelbot import parse


def lambda_handler(event, context):
    headers = event["headers"]
    auth_header = headers.get("X-Hub-Signature")
    body = json.loads(event["body"])
    installation_id = body["installation"]["id"]
    owner = body["repository"]["owner"]["login"]
    repo = body["repository"]["name"]
    issue_nr = body["issue"]["number"]
    issue_body = body["issue"]["body"]
    current_labels = [label["name"] for label in body["issue"]["labels"]]

    app_id = int(os.environ["APP_ID"])
    secret_key = os.environ["SECRET_KEY"]
    authenticated = authenticate_request(secret_key, body, auth_header)
    if not authenticated:
        return {"statuscode": 403}
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

def authenticate_request(key: str, body: str, signature: str) -> bool:
    """ Chacks if the X-Hub-Signature header exists, and if it does, verifies that the body 
    matches the hash sent from github."""
    if signature is None:
        return False
    
    sha_body = hmac.new(key.encode("utf8"), body.encode("utf8"), hashlib.sha1).hexdigest()
    alg, sha_github = signature.split("=")
    return hmac.compare_digest(sha_body, sha_github)