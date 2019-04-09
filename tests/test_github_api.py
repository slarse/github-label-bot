import json
import pytest

from labelbot import github_api

import responses

OWNER = "someone"
REPO = "best-repo"
ISSUE_NR = 231
ACCESS_TOKEN = "8924ab4"
ISSUE_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/issues/{ISSUE_NR}"

def create_authed_callback(status, headers, payload):
    """Return a callback that returns a 404 if the request does not have the
    correct authorization header.
    """

    def request_callback(request):
        auth = request.headers.get("Authorization", None)
        if auth != f"token {ACCESS_TOKEN}":
            return (404, {}, NOT_FOUND_PAYLOAD)
        return (status, headers, payload)

    return request_callback


class TestSetLabels:
    """Tests for the set_labels function."""

    @responses.activate
    def test_returns_true_on_200_ok(self):
        """Test that a 200 OK response results in True."""
        responses.add(responses.PATCH, url=ISSUE_URL, status=200)

        assert github_api.set_labels(
            ["bug", "enhancement"], OWNER, REPO, ISSUE_NR, ACCESS_TOKEN
        )

    @responses.activate
    def test_returns_false_on_404(self):
        """Test that a 404 NOT FOUND response results in False."""
        responses.add(responses.PATCH, url=ISSUE_URL, status=404)

        assert not github_api.set_labels(
            ["bug", "enhancement"], OWNER, REPO, ISSUE_NR, ACCESS_TOKEN
        )


class TestGetLabels:
    """Test for the get_labels function."""

    @responses.activate
    def test_returns_correct_labels(self):
        """Test that get_labels correctly extracts labels from the JSON
        payload.
        """
        resp_callback = create_authed_callback(200, {}, JSON_PAYLOAD)

        responses.add_callback(responses.GET, url=ISSUE_URL, callback=resp_callback)

        labels = github_api.get_labels(OWNER, REPO, ISSUE_NR, ACCESS_TOKEN)

        assert sorted(labels) == sorted(LABELS)

    @responses.activate
    def test_handles_incorrect_auth(self):
        """Test that get_labels handles a situation where the access token is
        rejected.
        """
        resp_callback = create_authed_callback(200, {}, JSON_PAYLOAD)
        invalid_token = ACCESS_TOKEN + "2345tr"

        responses.add_callback(responses.GET, url=ISSUE_URL, callback=resp_callback)

        with pytest.raises(github_api.APIError) as exc_info:
            github_api.get_labels(OWNER, REPO, ISSUE_NR, invalid_token)

        assert "could not get labels" in str(exc_info)



# real JSON payload from the API
LABELS = ["enhancement", "info"]
JSON_PAYLOAD = json.dumps(
    {
        "url": "https://api.github.com/repos/slarse/github-label-bot/issues/9",
        "repository_url": "https://api.github.com/repos/slarse/github-label-bot",
        "labels_url": "https://api.github.com/repos/slarse/github-label-bot/issues/9/labels{/name}",
        "comments_url": "https://api.github.com/repos/slarse/github-label-bot/issues/9/comments",
        "events_url": "https://api.github.com/repos/slarse/github-label-bot/issues/9/events",
        "html_url": "https://github.com/slarse/github-label-bot/issues/9",
        "id": 429297673,
        "node_id": "MDU6SXNzdWU0MjkyOTc2NzM=",
        "number": 9,
        "title": "Access token for privileged operations with the GitHub API",
        "user": {
            "login": "slarse",
            "id": 14223379,
            "node_id": "MDQ6VXNlcjE0MjIzMzc5",
            "avatar_url": "https://avatars1.githubusercontent.com/u/14223379?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/slarse",
            "html_url": "https://github.com/slarse",
            "followers_url": "https://api.github.com/users/slarse/followers",
            "following_url": "https://api.github.com/users/slarse/following{/other_user}",
            "gists_url": "https://api.github.com/users/slarse/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/slarse/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/slarse/subscriptions",
            "organizations_url": "https://api.github.com/users/slarse/orgs",
            "repos_url": "https://api.github.com/users/slarse/repos",
            "events_url": "https://api.github.com/users/slarse/events{/privacy}",
            "received_events_url": "https://api.github.com/users/slarse/received_events",
            "type": "User",
            "site_admin": False,
        },
        "labels": [
            {
                "id": 1302321832,
                "node_id": "MDU6TGFiZWwxMzAyMzIxODMy",
                "url": "https://api.github.com/repos/slarse/github-label-bot/labels/enhancement",
                "name": "enhancement",
                "color": "a2eeef",
                "default": True,
            },
            {
                "id": 1302323545,
                "node_id": "MDU6TGFiZWwxMzAyMzIzNTQ1",
                "url": "https://api.github.com/repos/slarse/github-label-bot/labels/info",
                "name": "info",
                "color": "fc58cd",
                "default": False,
            },
        ],
        "state": "open",
        "locked": False,
        "assignee": {
            "login": "jcroona",
            "id": 19162784,
            "node_id": "MDQ6VXNlcjE5MTYyNzg0",
            "avatar_url": "https://avatars0.githubusercontent.com/u/19162784?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/jcroona",
            "html_url": "https://github.com/jcroona",
            "followers_url": "https://api.github.com/users/jcroona/followers",
            "following_url": "https://api.github.com/users/jcroona/following{/other_user}",
            "gists_url": "https://api.github.com/users/jcroona/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/jcroona/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/jcroona/subscriptions",
            "organizations_url": "https://api.github.com/users/jcroona/orgs",
            "repos_url": "https://api.github.com/users/jcroona/repos",
            "events_url": "https://api.github.com/users/jcroona/events{/privacy}",
            "received_events_url": "https://api.github.com/users/jcroona/received_events",
            "type": "User",
            "site_admin": False,
        },
        "assignees": [
            {
                "login": "jcroona",
                "id": 19162784,
                "node_id": "MDQ6VXNlcjE5MTYyNzg0",
                "avatar_url": "https://avatars0.githubusercontent.com/u/19162784?v=4",
                "gravatar_id": "",
                "url": "https://api.github.com/users/jcroona",
                "html_url": "https://github.com/jcroona",
                "followers_url": "https://api.github.com/users/jcroona/followers",
                "following_url": "https://api.github.com/users/jcroona/following{/other_user}",
                "gists_url": "https://api.github.com/users/jcroona/gists{/gist_id}",
                "starred_url": "https://api.github.com/users/jcroona/starred{/owner}{/repo}",
                "subscriptions_url": "https://api.github.com/users/jcroona/subscriptions",
                "organizations_url": "https://api.github.com/users/jcroona/orgs",
                "repos_url": "https://api.github.com/users/jcroona/repos",
                "events_url": "https://api.github.com/users/jcroona/events{/privacy}",
                "received_events_url": "https://api.github.com/users/jcroona/received_events",
                "type": "User",
                "site_admin": False,
            }
        ],
        "milestone": None,
        "comments": 0,
        "created_at": "2019-04-04T14:02:40Z",
        "updated_at": "2019-04-09T19:38:52Z",
        "closed_at": None,
        "author_association": "OWNER",
        "body": "As we want to set labels on issues (a privileged operation) via the API, we need to generate an access token. [The process is described here](https://developer.github.com/apps/building-github-apps/authenticating-with-github-apps/#generating-a-private-key). There's a Python package [python_jwt](https://pypi.org/project/python_jwt/) that can do the hard parts for us. I've got an example of how to do this in an old project (although I wasn't the one who implemented it, so I'm not privvy to the details).\r\n\r\nOnce an access token has been generated, it's valid for 1 hour. If we want to optimize for performance, we could store the token for 1 hour in DynamoDB using the [TTL functionality](https://aws.amazon.com/about-aws/whats-new/2017/02/amazon-dynamodb-now-supports-automatic-item-expiration-with-time-to-live-ttl/). Won't be necessary for a prototype, but could be cool if we've got time left to do it.",
        "closed_by": None,
    }
)
NOT_FOUND_PAYLOAD = json.dumps(
    {
        "message": "Not Found",
        "documentation_url": "https://developer.github.com/v3/issues/#get-a-single-issue",
    }
)
