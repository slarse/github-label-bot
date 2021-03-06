import json
import contextlib
from unittest.mock import patch

import responses
import pytest

from labelbot import github_api

OWNER = "someone"
REPO = "best-repo"
ISSUE_NR = 231
ACCESS_TOKEN = "8924ab4"
ISSUE_URL = f"{github_api.BASE_URL}/repos/{OWNER}/{REPO}/issues/{ISSUE_NR}"
ALLOWED_LABELS_URL = f"{github_api.BASE_URL}/repos/{OWNER}/{REPO}/contents/{github_api.ALLOWED_LABELS_FILE}"


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
        resp_callback = create_authed_callback(200, {}, JSON_GET_LABELS_PAYLOAD)

        responses.add_callback(responses.GET, url=ISSUE_URL, callback=resp_callback)

        labels = github_api.get_labels(OWNER, REPO, ISSUE_NR, ACCESS_TOKEN)

        assert sorted(labels) == sorted(LABELS)

    @responses.activate
    def test_handles_incorrect_auth(self):
        """Test that get_labels handles a situation where the access token is
        rejected.
        """
        resp_callback = create_authed_callback(200, {}, JSON_GET_LABELS_PAYLOAD)
        invalid_token = ACCESS_TOKEN + "2345tr"

        responses.add_callback(responses.GET, url=ISSUE_URL, callback=resp_callback)

        with pytest.raises(github_api.APIError) as exc_info:
            github_api.get_labels(OWNER, REPO, ISSUE_NR, invalid_token)

        assert "could not get labels" in str(exc_info)


class TestGetFileContents:
    """Tests for get_file_contents"""

    @responses.activate
    def test_correctly_fetches_file_contents(self):
        resp_callback = create_authed_callback(200, {}, JSON_ALLOWED_LABELS_PAYLOAD)
        responses.add_callback(
            responses.GET, url=ALLOWED_LABELS_URL, callback=resp_callback
        )
        expected_contents = ALLOWED_LABELS_CONTENT

        actual_contents = github_api.get_file_contents(
            OWNER, REPO, github_api.ALLOWED_LABELS_FILE, ACCESS_TOKEN
        )

        assert actual_contents == expected_contents

    @responses.activate
    def test_handles_incorrect_auth(self):
        resp_callback = create_authed_callback(200, {}, JSON_ALLOWED_LABELS_PAYLOAD)
        responses.add_callback(
            responses.GET, url=ALLOWED_LABELS_URL, callback=resp_callback
        )
        invalid_token = ACCESS_TOKEN + "23ptwf"

        with pytest.raises(github_api.APIError) as exc_info:
            github_api.get_file_contents(
                OWNER, REPO, github_api.ALLOWED_LABELS_FILE, invalid_token
            )

        assert f"could not fetch {github_api.ALLOWED_LABELS_FILE}" in str(exc_info)


class TestSetAllowedLabels:
    """Tests for set_allowed_labels."""

    @contextlib.contextmanager
    def _mocked_apis(self, allowed_labels, wanted_labels, set_labels_result):
        """All apis mocked out returning the specified values. Yields the
        set_labels mock.
        """
        with patch(
            "labelbot.github_api.parse.parse_allowed_labels",
            autospec=True,
            return_value=allowed_labels,
        ), patch(
            "labelbot.github_api.parse.parse_wanted_labels",
            autospec=True,
            return_value=wanted_labels,
        ), patch(
            "labelbot.github_api.get_file_contents", autospec=True, return_value=""
        ):
            with patch(
                "labelbot.github_api.set_labels", autospec=True, return_value=True
            ) as set_labels:
                yield set_labels

    def test_happy_path(self):
        current_labels = ["enhancement"]
        allowed_labels = ["bug", "feature request"]
        wanted_labels = ["feature request", "help", "feature"]
        expected_labels = {"enhancement", "feature request"}

        with self._mocked_apis(
            allowed_labels, wanted_labels, set_labels_result=True
        ) as set_labels:
            res = github_api.set_allowed_labels(
                OWNER, REPO, ISSUE_NR, "", current_labels, ACCESS_TOKEN
            )

        assert res
        set_labels.assert_called_once_with(
            expected_labels, OWNER, REPO, ISSUE_NR, ACCESS_TOKEN
        )


ALLOWED_LABELS_CONTENT = "# labels that the labelbot are allowed to set\n# at the behest of users without read-access\nhelp\nbug\nfeature request\n"

JSON_ALLOWED_LABELS_PAYLOAD = json.dumps(
    {
        "name": ".allowed-labels",
        "path": ".allowed-labels",
        "sha": "f5dba9638257d949a4858ddfbd471cda77a7e416",
        "size": 116,
        "url": "https://api.github.com/repos/slarse/labelbot/contents/.allowed-labels?ref=master",
        "html_url": "https://github.com/slarse/labelbot/blob/master/.allowed-labels",
        "git_url": "https://api.github.com/repos/slarse/labelbot/git/blobs/f5dba9638257d949a4858ddfbd471cda77a7e416",
        "download_url": "https://raw.githubusercontent.com/slarse/labelbot/master/.allowed-labels",
        "type": "file",
        "content": "IyBsYWJlbHMgdGhhdCB0aGUgbGFiZWxib3QgYXJlIGFsbG93ZWQgdG8gc2V0\nCiMgYXQgdGhlIGJlaGVzdCBvZiB1c2VycyB3aXRob3V0IHJlYWQtYWNjZXNz\nCmhlbHAKYnVnCmZlYXR1cmUgcmVxdWVzdAo=\n",
        "encoding": "base64",
        "_links": {
            "self": "https://api.github.com/repos/slarse/labelbot/contents/.allowed-labels?ref=master",
            "git": "https://api.github.com/repos/slarse/labelbot/git/blobs/f5dba9638257d949a4858ddfbd471cda77a7e416",
            "html": "https://github.com/slarse/labelbot/blob/master/.allowed-labels",
        },
    }
)

# real JSON payload from the API
LABELS = ["enhancement", "info"]
JSON_GET_LABELS_PAYLOAD = json.dumps(
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
