import json
from typing import Sequence, List
import requests

BASE_URL = "https://api.github.com"


class APIError(Exception):
    """Raise when something goes wrong with the api."""


def _create_auth_headers(access_token):
    """Generate authorization headers."""
    return {"Authorization": f"token {access_token}"}


def _issue_url(owner, repo, issue_nr):
    """Generate the url for an issue."""
    return f"{BASE_URL}/repos/{owner}/{repo}/issues/{issue_nr}"


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
