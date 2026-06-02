#!/usr/bin/env python3
"""Unit tests for all MCP tools using mocked HTTP calls.

Run with:
    uv run python -m pytest tests/test_all_tools.py -v
"""

import sys
import os
import asyncio
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("AUTO_POST_API_TOKEN", "test-token")

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


FAKE_LIST = {"data": [], "total": 0, "page": 1, "size": 20}
FAKE_ITEM = {"data": {"id": "abc-123"}}


def mock_api_get(return_value=None):
    return patch("connectors.rest_client.requests.request", return_value=_mock_response(return_value or FAKE_LIST))


def _mock_response(data: dict):
    mock = MagicMock()
    mock.status_code = 200
    mock.json.return_value = data
    return mock


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
    def test_list_articles(self):
        with mock_api_get():
            result = list_articles(workspace_id="ws-1")
        assert result is not None

    def test_list_articles_with_pagination(self):
        with mock_api_get():
            result = list_articles(workspace_id="ws-1", page=2, size=10)
        assert result is not None

    def test_get_article(self):
        with mock_api_get(FAKE_ITEM):
            result = get_article(workspace_id="ws-1", article_id="art-1")
        assert result is not None

    def test_list_article_templates(self):
        with mock_api_get():
            result = list_article_templates(workspace_id="ws-1")
        assert result is not None

    def test_get_article_template(self):
        with mock_api_get(FAKE_ITEM):
            result = get_article_template(workspace_id="ws-1", article_template_id="tmpl-1")
        assert result is not None


# ---------------------------------------------------------------------------
# Avatar tools
# ---------------------------------------------------------------------------

class TestAvatarTools:
    def test_list_avatars(self):
        with mock_api_get():
            result = list_avatars(workspace_id="ws-1")
        assert result is not None

    def test_list_avatars_with_filters(self):
        with mock_api_get():
            result = list_avatars(workspace_id="ws-1", name="Alice", gender="female")
        assert result is not None

    def test_get_avatar(self):
        with mock_api_get(FAKE_ITEM):
            result = get_avatar(workspace_id="ws-1", avatar_id="av-1")
        assert result is not None


# ---------------------------------------------------------------------------
# Account tools
# ---------------------------------------------------------------------------

class TestAccountTools:
    def test_list_accounts(self):
        with mock_api_get():
            result = list_accounts(workspace_id="ws-1")
        assert result is not None

    def test_list_accounts_with_filters(self):
        with mock_api_get():
            result = list_accounts(workspace_id="ws-1", provider_type="twitter", app_id="app-1")
        assert result is not None

    def test_get_account(self):
        with mock_api_get(FAKE_ITEM):
            result = get_account(workspace_id="ws-1", account_id="acc-1")
        assert result is not None

    def test_get_accounts_by_avatar(self):
        with mock_api_get():
            result = get_accounts_by_avatar(workspace_id="ws-1", avatar_id="av-1")
        assert result is not None


# ---------------------------------------------------------------------------
# App tools
# ---------------------------------------------------------------------------

class TestAppTools:
    def test_list_apps(self):
        with mock_api_get():
            result = list_apps(workspace_id="ws-1")
        assert result is not None

    def test_list_apps_with_filter(self):
        with mock_api_get():
            result = list_apps(workspace_id="ws-1", provider_type="twitter")
        assert result is not None

    def test_get_app(self):
        with mock_api_get(FAKE_ITEM):
            result = get_app(workspace_id="ws-1", app_id="app-1")
        assert result is not None


# ---------------------------------------------------------------------------
# Blob tools
# ---------------------------------------------------------------------------

class TestBlobTools:
    def test_list_blobs(self):
        with mock_api_get():
            result = list_blobs(workspace_id="ws-1")
        assert result is not None

    def test_list_blobs_with_filter(self):
        with mock_api_get():
            result = list_blobs(workspace_id="ws-1", filter_by="type", filter_value="image")
        assert result is not None


# ---------------------------------------------------------------------------
# Content source tools
# ---------------------------------------------------------------------------

class TestContentSourceTools:
    def test_list_content_sources(self):
        with mock_api_get():
            result = list_content_sources(workspace_id="ws-1")
        assert result is not None

    def test_get_content_source(self):
        with mock_api_get(FAKE_ITEM):
            result = get_content_source(workspace_id="ws-1", content_source_id="cs-1")
        assert result is not None


# ---------------------------------------------------------------------------
# Mission tools
# ---------------------------------------------------------------------------

class TestMissionTools:
    def test_list_missions(self):
        with mock_api_get():
            result = list_missions(workspace_id="ws-1")
        assert result is not None

    def test_list_missions_with_filters(self):
        with mock_api_get():
            result = list_missions(
                workspace_id="ws-1",
                topic_id="t-1",
                avatar_id="av-1",
                mission_type="scheduled",
                q="keyword",
                sort_by="created_at",
                sort_order="desc",
            )
        assert result is not None

    def test_get_mission(self):
        with mock_api_get(FAKE_ITEM):
            result = get_mission(workspace_id="ws-1", mission_id="m-1")
        assert result is not None

    def test_export_mission(self):
        with mock_api_get(FAKE_ITEM):
            result = export_mission(workspace_id="ws-1", mission_id="m-1")
        assert result is not None

    def test_list_mission_contents(self):
        with mock_api_get():
            result = list_mission_contents(workspace_id="ws-1")
        assert result is not None

    def test_list_mission_contents_with_filters(self):
        with mock_api_get():
            result = list_mission_contents(
                workspace_id="ws-1",
                mission_id="m-1",
                avatar_id="av-1",
                status="completed",
            )
        assert result is not None

    def test_get_mission_content(self):
        with mock_api_get(FAKE_ITEM):
            result = get_mission_content(workspace_id="ws-1", mission_content_id="mc-1")
        assert result is not None


# ---------------------------------------------------------------------------
# Publication tools
# ---------------------------------------------------------------------------

class TestPublicationTools:
    def test_list_publications(self):
        with mock_api_get():
            result = list_publications(workspace_id="ws-1")
        assert result is not None

    def test_get_publication(self):
        with mock_api_get(FAKE_ITEM):
            result = get_publication(workspace_id="ws-1", publication_id="pub-1")
        assert result is not None


# ---------------------------------------------------------------------------
# Topic tools
# ---------------------------------------------------------------------------

class TestTopicTools:
    def test_list_topics(self):
        with mock_api_get():
            result = list_topics(workspace_id="ws-1")
        assert result is not None

    def test_list_topics_with_name_filter(self):
        with mock_api_get():
            result = list_topics(workspace_id="ws-1", name="tech")
        assert result is not None

    def test_get_topic(self):
        with mock_api_get(FAKE_ITEM):
            result = get_topic(workspace_id="ws-1", topic_id="tp-1")
        assert result is not None

    def test_list_topic_categories(self):
        with mock_api_get():
            result = list_topic_categories(workspace_id="ws-1")
        assert result is not None


# ---------------------------------------------------------------------------
# Workspace tools
# ---------------------------------------------------------------------------

class TestWorkspaceTools:
    def test_list_workspaces(self):
        with mock_api_get():
            result = list_workspaces()
        assert result is not None

    def test_get_workspace(self):
        with mock_api_get(FAKE_ITEM):
            result = get_workspace(workspace_id="ws-1")
        assert result is not None


# ---------------------------------------------------------------------------
# Request header checks
# ---------------------------------------------------------------------------

class TestWorkspaceHeader:
    """Verify that the x-asgard-workspace header is sent for workspace-scoped calls."""

    def test_workspace_header_sent(self):
        mock_resp = _mock_response(FAKE_LIST)
        with patch("connectors.rest_client.requests.request", return_value=mock_resp) as mock_req:
            list_articles(workspace_id="my-workspace")
            call_kwargs = mock_req.call_args
            headers = call_kwargs.kwargs.get("headers") or call_kwargs[1].get("headers", {})
            assert headers.get("x-asgard-workspace") == "my-workspace"

    def test_bearer_token_sent(self):
        mock_resp = _mock_response(FAKE_LIST)
        with patch("connectors.rest_client.requests.request", return_value=mock_resp) as mock_req:
            list_articles(workspace_id="ws-1")
            call_kwargs = mock_req.call_args
            headers = call_kwargs.kwargs.get("headers") or call_kwargs[1].get("headers", {})
            assert headers.get("Authorization") == "Bearer test-token"
