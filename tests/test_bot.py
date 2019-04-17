from labelbot import bot
import pytest
SECRET = "d653a60adc0a16a93e99f0620a67f4a67ef901df"
BODY = "Hello, World!"
SIGN = "sha1=8727505c9c036b2337a06d2e63f091a7aa41ae60"

class TestAuthenticateRequest:
    def test_correct_hash(self):
        result = bot.authenticate_request(SECRET,BODY, SIGN)
        assert result

    def test_incorrect_hash(self):
        result = bot.authenticate_request(SECRET,BODY.lower(), SIGN)
        assert not result

    def test_no_signature(self):
        result = bot.authenticate_request(SECRET,BODY, None)
        assert not result



@pytest.fixture
def env_setup(mocker):
    values = {"APP_ID": "243554", "SECRET_KEY": "66535665634", "BUCKET_NAME": "My_bucket", "BUCKET_KEY": "my_file"}
    mocker.patch("os.getenv", autospec=True, side_effect=values.get)
    yield values

def test_lambda_handler_authentication(env_setup):
    event = {"headers": {"X-Hub-Signature": "sha1=4afefa55e46cc2ac696127dae55b49aeb999b7e8"},"body": jsonstring}
    result = bot.lambda_handler(event, None)
    assert result

jsonstring = """{
  "action": "reopened",
  "issue": {
    "url": "https://api.github.com/repos/jcroona/testrepo/issues/10",
    "repository_url": "https://api.github.com/repos/jcroona/testrepo",
    "labels_url": "https://api.github.com/repos/jcroona/testrepo/issues/10/labels{/name}",
    "comments_url": "https://api.github.com/repos/jcroona/testrepo/issues/10/comments",
    "events_url": "https://api.github.com/repos/jcroona/testrepo/issues/10/events",
    "html_url": "https://github.com/jcroona/testrepo/issues/10",
    "id": 434163632,
    "node_id": "MDU6SXNzdWU0MzQxNjM2MzI=",
    "number": 10,
    "title": "test new code",
    "user": {
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
      "site_admin": false
    },
    "labels": [

    ],
    "state": "open",
    "locked": false,
    "assignee": null,
    "assignees": [

    ],
    "milestone": null,
    "comments": 0,
    "created_at": "2019-04-17T08:47:17Z",
    "updated_at": "2019-04-17T08:52:14Z",
    "closed_at": null,
    "author_association": "OWNER",
    "body": ":label:`kaka`"
  },
  "repository": {
    "id": 179567397,
    "node_id": "MDEwOlJlcG9zaXRvcnkxNzk1NjczOTc=",
    "name": "testrepo",
    "full_name": "jcroona/testrepo",
    "private": false,
    "owner": {
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
      "site_admin": false
    },
    "html_url": "https://github.com/jcroona/testrepo",
    "description": "Repo for testing aws lambda",
    "fork": false,
    "url": "https://api.github.com/repos/jcroona/testrepo",
    "forks_url": "https://api.github.com/repos/jcroona/testrepo/forks",
    "keys_url": "https://api.github.com/repos/jcroona/testrepo/keys{/key_id}",
    "collaborators_url": "https://api.github.com/repos/jcroona/testrepo/collaborators{/collaborator}",
    "teams_url": "https://api.github.com/repos/jcroona/testrepo/teams",
    "hooks_url": "https://api.github.com/repos/jcroona/testrepo/hooks",
    "issue_events_url": "https://api.github.com/repos/jcroona/testrepo/issues/events{/number}",
    "events_url": "https://api.github.com/repos/jcroona/testrepo/events",
    "assignees_url": "https://api.github.com/repos/jcroona/testrepo/assignees{/user}",
    "branches_url": "https://api.github.com/repos/jcroona/testrepo/branches{/branch}",
    "tags_url": "https://api.github.com/repos/jcroona/testrepo/tags",
    "blobs_url": "https://api.github.com/repos/jcroona/testrepo/git/blobs{/sha}",
    "git_tags_url": "https://api.github.com/repos/jcroona/testrepo/git/tags{/sha}",
    "git_refs_url": "https://api.github.com/repos/jcroona/testrepo/git/refs{/sha}",
    "trees_url": "https://api.github.com/repos/jcroona/testrepo/git/trees{/sha}",
    "statuses_url": "https://api.github.com/repos/jcroona/testrepo/statuses/{sha}",
    "languages_url": "https://api.github.com/repos/jcroona/testrepo/languages",
    "stargazers_url": "https://api.github.com/repos/jcroona/testrepo/stargazers",
    "contributors_url": "https://api.github.com/repos/jcroona/testrepo/contributors",
    "subscribers_url": "https://api.github.com/repos/jcroona/testrepo/subscribers",
    "subscription_url": "https://api.github.com/repos/jcroona/testrepo/subscription",
    "commits_url": "https://api.github.com/repos/jcroona/testrepo/commits{/sha}",
    "git_commits_url": "https://api.github.com/repos/jcroona/testrepo/git/commits{/sha}",
    "comments_url": "https://api.github.com/repos/jcroona/testrepo/comments{/number}",
    "issue_comment_url": "https://api.github.com/repos/jcroona/testrepo/issues/comments{/number}",
    "contents_url": "https://api.github.com/repos/jcroona/testrepo/contents/{+path}",
    "compare_url": "https://api.github.com/repos/jcroona/testrepo/compare/{base}...{head}",
    "merges_url": "https://api.github.com/repos/jcroona/testrepo/merges",
    "archive_url": "https://api.github.com/repos/jcroona/testrepo/{archive_format}{/ref}",
    "downloads_url": "https://api.github.com/repos/jcroona/testrepo/downloads",
    "issues_url": "https://api.github.com/repos/jcroona/testrepo/issues{/number}",
    "pulls_url": "https://api.github.com/repos/jcroona/testrepo/pulls{/number}",
    "milestones_url": "https://api.github.com/repos/jcroona/testrepo/milestones{/number}",
    "notifications_url": "https://api.github.com/repos/jcroona/testrepo/notifications{?since,all,participating}",
    "labels_url": "https://api.github.com/repos/jcroona/testrepo/labels{/name}",
    "releases_url": "https://api.github.com/repos/jcroona/testrepo/releases{/id}",
    "deployments_url": "https://api.github.com/repos/jcroona/testrepo/deployments",
    "created_at": "2019-04-04T19:54:23Z",
    "updated_at": "2019-04-12T08:28:32Z",
    "pushed_at": "2019-04-12T08:28:31Z",
    "git_url": "git://github.com/jcroona/testrepo.git",
    "ssh_url": "git@github.com:jcroona/testrepo.git",
    "clone_url": "https://github.com/jcroona/testrepo.git",
    "svn_url": "https://github.com/jcroona/testrepo",
    "homepage": null,
    "size": 1,
    "stargazers_count": 0,
    "watchers_count": 0,
    "language": null,
    "has_issues": true,
    "has_projects": true,
    "has_downloads": true,
    "has_wiki": true,
    "has_pages": false,
    "forks_count": 0,
    "mirror_url": null,
    "archived": false,
    "disabled": false,
    "open_issues_count": 8,
    "license": null,
    "forks": 0,
    "open_issues": 8,
    "watchers": 0,
    "default_branch": "master"
  },
  "sender": {
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
    "site_admin": false
  },
  "installation": {
    "id": 825958,
    "node_id": "MDIzOkludGVncmF0aW9uSW5zdGFsbGF0aW9uODI1OTU4"
  }
}"""


