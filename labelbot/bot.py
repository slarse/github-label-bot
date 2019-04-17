import json
import os
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

    app_id = int(os.getenv("APP_ID"))
    secret_key = os.getenv("SECRET_KEY")
    authenticated = auth.authenticate_request(
        secret_key, event["body"], event["headers"]["X-Hub-Signature"]
    )
    if not authenticated:
        return {"statuscode": 403}
    bucket_name = os.getenv("BUCKET_NAME")
    bucket_key = os.getenv("BUCKET_KEY")
    pem = auth.get_pem(bucket_name, bucket_key)

    jwt_token = auth.generate_jwt_token(pem, app_id)
    access_token = auth.generate_installation_access_token(jwt_token, installation_id)

    success = github_api.set_allowed_labels(
        owner, repo, issue_nr, issue_body, current_labels, access_token
    )

    return {"statusCode": 200 if success else 403, "body": json.dumps("temp")}
