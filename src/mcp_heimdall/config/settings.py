import os

BASE_URL = os.environ.get("AUTO_POST_API_BASE_URL", "")
API_VERSION = "v1"
DEFAULT_PER_PAGE = 20

from ..auth.bearer import get_auth_headers

ENDPOINTS = {
    # article
    "list_articles": f"/{API_VERSION}/article",
    "get_article": f"/{API_VERSION}/article/{{article_id}}",
    # article-template
    "list_article_templates": f"/{API_VERSION}/article-template",
    "get_article_template": f"/{API_VERSION}/article-template/{{article_template_id}}",
    # avatar
    "list_avatars": f"/{API_VERSION}/avatar",
    "get_avatar": f"/{API_VERSION}/avatar/{{avatar_id}}",
    # account
    "list_accounts": f"/{API_VERSION}/account",
    "get_account": f"/{API_VERSION}/account/{{account_id}}",
    "get_accounts_by_avatar": f"/{API_VERSION}/account/by-avatar/{{avatar_id}}",
    # app
    "list_apps": f"/{API_VERSION}/app",
    "get_app": f"/{API_VERSION}/app/{{app_id}}",
    # blob
    "list_blobs": f"/{API_VERSION}/blob",
    # content-source
    "list_content_sources": f"/{API_VERSION}/content-source",
    "get_content_source": f"/{API_VERSION}/content-source/{{content_source_id}}",
    # mission
    "list_missions": f"/{API_VERSION}/mission",
    "get_mission": f"/{API_VERSION}/mission/{{mission_id}}",
    "export_mission": f"/{API_VERSION}/mission/{{mission_id}}/export",
    # mission-content
    "list_mission_contents": f"/{API_VERSION}/mission-content",
    "get_mission_content": f"/{API_VERSION}/mission-content/{{mission_content_id}}",
    # publication
    "list_publications": f"/{API_VERSION}/publication",
    "get_publication": f"/{API_VERSION}/publication/{{publication_id}}",
    # topic
    "list_topics": f"/{API_VERSION}/topic",
    "get_topic": f"/{API_VERSION}/topic/{{topic_id}}",
    "list_topic_categories": f"/{API_VERSION}/topic/categories",
    # workspace
    "list_workspaces": f"/{API_VERSION}/workspace",
    "get_workspace": f"/{API_VERSION}/workspace/{{workspace_id}}",
}


def get_headers() -> dict:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    headers.update(get_auth_headers())
    return headers


def get_url(endpoint_key: str, **kwargs) -> str:
    path = ENDPOINTS[endpoint_key]
    if kwargs:
        path = path.format(**kwargs)
    return f"{BASE_URL}{path}"
