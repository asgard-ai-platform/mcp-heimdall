#!/usr/bin/env python3
"""Unit tests for all MCP tools using mocked HTTP calls.

Run with:
    uv run python -m pytest tests/test_all_tools.py -v
"""

import sys
import os
import asyncio
from unittest.mock import patch, MagicMock, call

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("AUTO_POST_API_TOKEN", "test-token")
os.environ.setdefault("AUTO_POST_API_BASE_URL", "https://api.example.com")

import tools.article_tools
import tools.avatar_tools
import tools.account_tools
import tools.app_tools
import tools.blob_tools
import tools.content_source_tools
import tools.mission_tools
import tools.publication_tools
import tools.topic_tools
import tools.workspace_tools

from tools.article_tools import list_articles, get_article, list_article_templates, get_article_template
from tools.avatar_tools import list_avatars, get_avatar
from tools.account_tools import list_accounts, get_account, get_accounts_by_avatar
from tools.app_tools import list_apps, get_app
from tools.blob_tools import list_blobs
from tools.content_source_tools import list_content_sources, get_content_source
from tools.mission_tools import list_missions, get_mission, export_mission, list_mission_contents, get_mission_content
from tools.publication_tools import list_publications, get_publication
from tools.topic_tools import list_topics, get_topic, list_topic_categories
from tools.workspace_tools import list_workspaces, get_workspace
from app import mcp

BASE = "https://api.example.com"
FAKE_LIST = {"data": [], "total": 0, "page": 1, "size": 20}
FAKE_ITEM = {"data": {"id": "abc-123"}}


def _mock_response(data: dict):
    mock = MagicMock()
    mock.status_code = 200
    mock.json.return_value = data
    return mock


def mock_api_get(return_value=None):
    return patch("connectors.rest_client.requests.request", return_value=_mock_response(return_value or FAKE_LIST))


def get_call_kwargs(mock_req):
    """Extract keyword arguments from a mock request call."""
    return mock_req.call_args.kwargs if mock_req.call_args.kwargs else mock_req.call_args[1]


# ---------------------------------------------------------------------------
# Tool registration
# ---------------------------------------------------------------------------

def test_tool_registration():
    tools_list = asyncio.run(mcp.list_tools())
    names = {t.name for t in tools_list}
    expected = {
        "list_articles", "get_article",
        "list_article_templates", "get_article_template",
        "list_avatars", "get_avatar",
        "list_accounts", "get_account", "get_accounts_by_avatar",
        "list_apps", "get_app",
        "list_blobs",
        "list_content_sources", "get_content_source",
        "list_missions", "get_mission", "export_mission",
        "list_mission_contents", "get_mission_content",
        "list_publications", "get_publication",
        "list_topics", "get_topic", "list_topic_categories",
        "list_workspaces", "get_workspace",
    }
    assert expected.issubset(names), f"Missing tools: {expected - names}"


# ---------------------------------------------------------------------------
# Article tools
# ---------------------------------------------------------------------------

class TestArticleTools:
    def test_list_articles_url_and_params(self):
        with mock_api_get() as mock_req:
            list_articles(workspace_id="ws-1", page=2, size=10)
        kw = get_call_kwargs(mock_req)
        assert kw["url"] == f"{BASE}/v1/article"
        assert kw["params"] == {"page": 2, "size": 10}
        assert kw["headers"]["x-asgard-workspace"] == "ws-1"

    def test_list_articles_default_pagination(self):
        with mock_api_get() as mock_req:
            list_articles(workspace_id="ws-1")
        kw = get_call_kwargs(mock_req)
        assert kw["params"] == {"page": 1, "size": 20}

    def test_get_article_url_and_path_param(self):
        with mock_api_get(FAKE_ITEM) as mock_req:
            get_article(workspace_id="ws-1", article_id="art-42")
        kw = get_call_kwargs(mock_req)
        assert kw["url"] == f"{BASE}/v1/article/art-42"
        assert kw["headers"]["x-asgard-workspace"] == "ws-1"

    def test_list_article_templates_url(self):
        with mock_api_get() as mock_req:
            list_article_templates(workspace_id="ws-1")
        assert get_call_kwargs(mock_req)["url"] == f"{BASE}/v1/article-template"

    def test_get_article_template_url(self):
        with mock_api_get(FAKE_ITEM) as mock_req:
            get_article_template(workspace_id="ws-1", article_template_id="tmpl-7")
        assert get_call_kwargs(mock_req)["url"] == f"{BASE}/v1/article-template/tmpl-7"


# ---------------------------------------------------------------------------
# Avatar tools
# ---------------------------------------------------------------------------

class TestAvatarTools:
    def test_list_avatars_url_and_defaults(self):
        with mock_api_get() as mock_req:
            list_avatars(workspace_id="ws-1")
        kw = get_call_kwargs(mock_req)
        assert kw["url"] == f"{BASE}/v1/avatar"
        assert kw["params"] == {"page": 1, "size": 20}

    def test_list_avatars_optional_filters(self):
        with mock_api_get() as mock_req:
            list_avatars(workspace_id="ws-1", name="Alice", gender="female")
        assert get_call_kwargs(mock_req)["params"] == {"page": 1, "size": 20, "name": "Alice", "gender": "female"}

    def test_get_avatar_url(self):
        with mock_api_get(FAKE_ITEM) as mock_req:
            get_avatar(workspace_id="ws-1", avatar_id="av-99")
        assert get_call_kwargs(mock_req)["url"] == f"{BASE}/v1/avatar/av-99"


# ---------------------------------------------------------------------------
# Account tools
# ---------------------------------------------------------------------------

class TestAccountTools:
    def test_list_accounts_url_and_defaults(self):
        with mock_api_get() as mock_req:
            list_accounts(workspace_id="ws-1")
        kw = get_call_kwargs(mock_req)
        assert kw["url"] == f"{BASE}/v1/account"
        assert kw["params"] == {"page": 1, "size": 20}

    def test_list_accounts_optional_filters(self):
        with mock_api_get() as mock_req:
            list_accounts(workspace_id="ws-1", provider_type="twitter", app_id="app-1")
        assert get_call_kwargs(mock_req)["params"] == {"page": 1, "size": 20, "provider_type": "twitter", "app_id": "app-1"}

    def test_get_account_url(self):
        with mock_api_get(FAKE_ITEM) as mock_req:
            get_account(workspace_id="ws-1", account_id="acc-5")
        assert get_call_kwargs(mock_req)["url"] == f"{BASE}/v1/account/acc-5"

    def test_get_accounts_by_avatar_url(self):
        with mock_api_get() as mock_req:
            get_accounts_by_avatar(workspace_id="ws-1", avatar_id="av-1")
        assert get_call_kwargs(mock_req)["url"] == f"{BASE}/v1/account/by-avatar/av-1"


# ---------------------------------------------------------------------------
# App tools
# ---------------------------------------------------------------------------

class TestAppTools:
    def test_list_apps_url_and_defaults(self):
        with mock_api_get() as mock_req:
            list_apps(workspace_id="ws-1")
        kw = get_call_kwargs(mock_req)
        assert kw["url"] == f"{BASE}/v1/app"
        assert kw["params"] == {"page": 1, "size": 20}

    def test_list_apps_provider_type_filter(self):
        with mock_api_get() as mock_req:
            list_apps(workspace_id="ws-1", provider_type="twitter")
        assert get_call_kwargs(mock_req)["params"]["provider_type"] == "twitter"

    def test_get_app_url(self):
        with mock_api_get(FAKE_ITEM) as mock_req:
            get_app(workspace_id="ws-1", app_id="app-3")
        assert get_call_kwargs(mock_req)["url"] == f"{BASE}/v1/app/app-3"


# ---------------------------------------------------------------------------
# Blob tools
# ---------------------------------------------------------------------------

class TestBlobTools:
    def test_list_blobs_url_and_defaults(self):
        with mock_api_get() as mock_req:
            list_blobs(workspace_id="ws-1")
        kw = get_call_kwargs(mock_req)
        assert kw["url"] == f"{BASE}/v1/blob"
        assert kw["params"] == {"page": 1, "size": 20}

    def test_list_blobs_filter_params(self):
        with mock_api_get() as mock_req:
            list_blobs(workspace_id="ws-1", filter_by="type", filter_value="image")
        params = get_call_kwargs(mock_req)["params"]
        assert params["filter_by"] == "type"
        assert params["filter_value"] == "image"


# ---------------------------------------------------------------------------
# Content source tools
# ---------------------------------------------------------------------------

class TestContentSourceTools:
    def test_list_content_sources_url(self):
        with mock_api_get() as mock_req:
            list_content_sources(workspace_id="ws-1")
        assert get_call_kwargs(mock_req)["url"] == f"{BASE}/v1/content-source"

    def test_get_content_source_url(self):
        with mock_api_get(FAKE_ITEM) as mock_req:
            get_content_source(workspace_id="ws-1", content_source_id="cs-8")
        assert get_call_kwargs(mock_req)["url"] == f"{BASE}/v1/content-source/cs-8"


# ---------------------------------------------------------------------------
# Mission tools
# ---------------------------------------------------------------------------

class TestMissionTools:
    def test_list_missions_url_and_defaults(self):
        with mock_api_get() as mock_req:
            list_missions(workspace_id="ws-1")
        kw = get_call_kwargs(mock_req)
        assert kw["url"] == f"{BASE}/v1/mission"
        assert kw["params"] == {"page": 1, "size": 20}

    def test_list_missions_all_filters(self):
        with mock_api_get() as mock_req:
            list_missions(
                workspace_id="ws-1",
                topic_id="t-1", avatar_id="av-1",
                mission_type="scheduled", q="keyword",
                sort_by="created_at", sort_order="desc",
            )
        params = get_call_kwargs(mock_req)["params"]
        assert params["topic_id"] == "t-1"
        assert params["avatar_id"] == "av-1"
        assert params["mission_type"] == "scheduled"
        assert params["q"] == "keyword"
        assert params["sort_by"] == "created_at"
        assert params["sort_order"] == "desc"

    def test_get_mission_url(self):
        with mock_api_get(FAKE_ITEM) as mock_req:
            get_mission(workspace_id="ws-1", mission_id="m-42")
        assert get_call_kwargs(mock_req)["url"] == f"{BASE}/v1/mission/m-42"

    def test_export_mission_url(self):
        with mock_api_get(FAKE_ITEM) as mock_req:
            export_mission(workspace_id="ws-1", mission_id="m-42")
        assert get_call_kwargs(mock_req)["url"] == f"{BASE}/v1/mission/m-42/export"

    def test_list_mission_contents_url_and_defaults(self):
        with mock_api_get() as mock_req:
            list_mission_contents(workspace_id="ws-1")
        kw = get_call_kwargs(mock_req)
        assert kw["url"] == f"{BASE}/v1/mission-content"
        assert kw["params"] == {"page": 1, "size": 20}

    def test_list_mission_contents_filters(self):
        with mock_api_get() as mock_req:
            list_mission_contents(workspace_id="ws-1", mission_id="m-1", avatar_id="av-1", status="completed")
        params = get_call_kwargs(mock_req)["params"]
        assert params["mission_id"] == "m-1"
        assert params["status"] == "completed"

    def test_get_mission_content_url(self):
        with mock_api_get(FAKE_ITEM) as mock_req:
            get_mission_content(workspace_id="ws-1", mission_content_id="mc-7")
        assert get_call_kwargs(mock_req)["url"] == f"{BASE}/v1/mission-content/mc-7"


# ---------------------------------------------------------------------------
# Publication tools
# ---------------------------------------------------------------------------

class TestPublicationTools:
    def test_list_publications_url(self):
        with mock_api_get() as mock_req:
            list_publications(workspace_id="ws-1")
        assert get_call_kwargs(mock_req)["url"] == f"{BASE}/v1/publication"

    def test_get_publication_url(self):
        with mock_api_get(FAKE_ITEM) as mock_req:
            get_publication(workspace_id="ws-1", publication_id="pub-9")
        assert get_call_kwargs(mock_req)["url"] == f"{BASE}/v1/publication/pub-9"


# ---------------------------------------------------------------------------
# Topic tools
# ---------------------------------------------------------------------------

class TestTopicTools:
    def test_list_topics_url_and_defaults(self):
        with mock_api_get() as mock_req:
            list_topics(workspace_id="ws-1")
        kw = get_call_kwargs(mock_req)
        assert kw["url"] == f"{BASE}/v1/topic"
        assert kw["params"] == {"page": 1, "size": 20}

    def test_list_topics_name_filter(self):
        with mock_api_get() as mock_req:
            list_topics(workspace_id="ws-1", name="tech")
        assert get_call_kwargs(mock_req)["params"]["name"] == "tech"

    def test_get_topic_url(self):
        with mock_api_get(FAKE_ITEM) as mock_req:
            get_topic(workspace_id="ws-1", topic_id="tp-3")
        assert get_call_kwargs(mock_req)["url"] == f"{BASE}/v1/topic/tp-3"

    def test_list_topic_categories_url(self):
        with mock_api_get() as mock_req:
            list_topic_categories(workspace_id="ws-1")
        assert get_call_kwargs(mock_req)["url"] == f"{BASE}/v1/topic/categories"


# ---------------------------------------------------------------------------
# Workspace tools
# ---------------------------------------------------------------------------

class TestWorkspaceTools:
    def test_list_workspaces_url(self):
        with mock_api_get() as mock_req:
            list_workspaces()
        assert get_call_kwargs(mock_req)["url"] == f"{BASE}/v1/workspace"

    def test_get_workspace_url(self):
        with mock_api_get(FAKE_ITEM) as mock_req:
            get_workspace(workspace_id="ws-42")
        assert get_call_kwargs(mock_req)["url"] == f"{BASE}/v1/workspace/ws-42"

    def test_get_workspace_no_fieldinfo_leak(self):
        """Ensure workspace_id is a real string, not a FieldInfo object."""
        with mock_api_get(FAKE_ITEM) as mock_req:
            get_workspace(workspace_id="ws-1")
        url = get_call_kwargs(mock_req)["url"]
        assert "FieldInfo" not in url
        assert "annotation" not in url
        assert url == f"{BASE}/v1/workspace/ws-1"


# ---------------------------------------------------------------------------
# Request header checks
# ---------------------------------------------------------------------------

class TestRequestHeaders:
    def test_workspace_header_sent(self):
        with mock_api_get() as mock_req:
            list_articles(workspace_id="my-workspace")
        headers = get_call_kwargs(mock_req)["headers"]
        assert headers["x-asgard-workspace"] == "my-workspace"

    def test_bearer_token_sent(self):
        with mock_api_get() as mock_req:
            list_articles(workspace_id="ws-1")
        headers = get_call_kwargs(mock_req)["headers"]
        assert headers["Authorization"] == "Bearer test-token"

    def test_workspace_header_not_sent_for_list_workspaces(self):
        """list_workspaces is not workspace-scoped — no x-asgard-workspace header."""
        with mock_api_get() as mock_req:
            list_workspaces()
        headers = get_call_kwargs(mock_req)["headers"]
        assert "x-asgard-workspace" not in headers
