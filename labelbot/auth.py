"""Functions for handling authentication procedures.

.. module:: auth
    :synopsis: Functions for handling authentication procedures.
.. moduleauthor:: Lars Hummelgren <larshum@kth.se> & Joakim Croona <jcroona@kth.se>
"""

import datetime
import http.client
import json
import jwcrypto
import python_jwt
import requests
import boto3
import botocore
import hmac
import hashlib

USER_AGENT = "label-bot"


def generate_jwt_token(private_pem: bytes, app_id: int) -> str:
    """Generates a JWT token valid for 10 minutes using the private key.

    Args:
        private_pem: the private key that is used to generate a JWT
        app_id the Application id
    Returns:
        The JWT that was generated using the private key and the app id
    """
    private_key = jwcrypto.jwk.JWK.from_pem(private_pem)
    payload = {"iss": app_id}
    duration = datetime.timedelta(minutes=10)
    return python_jwt.generate_jwt(payload, private_key, "RS256", duration)


def generate_installation_access_token(jwt_token: str, installation_id) -> str:
    """Generates an installation access token using a JWT token and an installation id.

    An installation access token is valid for 1 hour.

    Args:
        jwt_token: a valid JWT token
        installation_id: the installation id of the app.
    Returns:
        An installation access token from the GitHub API
    """
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github.machine-man-preview+json",
        "User-Agent": USER_AGENT,
    }
    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    r = requests.post(url, headers=headers)
    return r.json()["token"]


def get_pem(bucket_name: str, bucket_key: str) -> bytes:
    """Reads a private PEM file from an S3 bucket.

    Args:
        bucket_name: Name of the S3 bucket.
        bucket_key: Bucket key for the PEM file.
    Returns:
        Contents of the PEM file.
    """
    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).download_file(bucket_key, "/tmp/key.pem")
    with open("/tmp/key.pem", "rb") as f:
        return f.read()


def authenticate_request(shared_secret: str, body: str, signature: str) -> bool:
    """Checks if the MAC (message authentication code) sent in the request is really
    from GitHub.

    Args:
        shared_secret: A secret shared between GitHub and the bot.
        body: Body of the HTTP request.
        signature: The header containing the MAC.
    Returns:
        True iff the signature is a MAC computed with the body of the request and the
        shared secret.
    """
    if signature is None:
        return False

    sha_body = hmac.new(
        shared_secret.encode("utf8"), body.encode("utf8"), hashlib.sha1
    ).hexdigest()
    _, sha_github = signature.split("=")
    return hmac.compare_digest(sha_body, sha_github)
