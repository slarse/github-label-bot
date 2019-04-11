"""Functions for interacting with the GitHub API.

.. module:: github_api
    :synopsis: Functions for interacting with the GitHub API.
"""
import json
import sys
import base64
from typing import Sequence, List
import requests

BASE_URL = "https://api.github.com"
ALLOWED_LABELS_FILE = ".allowed-labels"


class APIError(Exception):
    """Raise when something goes wrong with the api."""


def _create_auth_headers(access_token):
    """Generate authorization headers."""
    return {"Authorization": f"token {access_token}"}


def _issue_url(owner, repo, issue_nr):
    """Generate the url for an issue."""
    return f"{BASE_URL}/repos/{owner}/{repo}/issues/{issue_nr}"


def _allowed_labels_url(owner, repo):
    return f"{BASE_URL}/repos/{owner}/{repo}/contents/{ALLOWED_LABELS_FILE}"


def set_labels(
    labels: Sequence[str], owner: str, repo: str, issue_nr: int, access_token: str
) -> bool:
    """Unconditionally set the provided labels on a repository issue.

    Args:
        labels: A sequence of labels to set.
        owner: User/Organization that owns the repo.
        repo: Name of the repo.
        issue_nr: Number of the issue.
        access_token: An installation access token for the repo.
    Returns:
        True if the API request was succesful
    """
    headers = _create_auth_headers(access_token)
    payload = json.dumps({"labels": list(labels)})
    url = _issue_url(owner, repo, issue_nr)
    req = requests.patch(url, headers=headers, data=payload)
    return req.status_code == 200


def get_labels(owner: str, repo: str, issue_nr: int, access_token: str) -> List[str]:
    """Get the labels from the given repository issue.

    Args:
        owner: User/Organization that owns the repo.
        repo: Name of the repo.
        issue_nr: Number of the issue.
        access_token: An installation access token for the repo.
    Returns:
        A list of labels.
    """
    headers = _create_auth_headers(access_token)
    url = _issue_url(owner, repo, issue_nr)
    req = requests.get(url, headers=headers)
    try:
        labels = [lab["name"] for lab in req.json()["labels"]]
    except KeyError:
        raise APIError(f"could not get labels from {owner}/{repo}#{issue_nr}")
    return labels


def get_file_contents(owner: str, repo: str, filepath: str, access_token: str) -> str:
    """Fetch the contents of a file in the repo.

    Args:
        owner: User/Organization that owns the repo.
        repo: Name of the repo.
        filepath: Path to the file from the repo root.
        access_token: A API access token.
    Returns:
        The contents of the the specified file.
    """
    headers = {
        **_create_auth_headers(access_token),
        "Content-Type": "application/vnd.github.VERSION.raw",
    }
    url = _allowed_labels_url(owner, repo)
    req = requests.get(url, headers=headers)
    try:
        content = req.json()["content"]
    except KeyError:
        raise APIError(f"could not fetch {filepath} from {owner}/{repo}")
    return base64.b64decode(content).decode(encoding=sys.getdefaultencoding())
