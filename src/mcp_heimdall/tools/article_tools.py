"""Tools for article and article template resources."""

from typing import Annotated

from pydantic import Field

from ..app import mcp
from ..connectors.rest_client import api_get


def _workspace_header(workspace_id: str) -> dict:
    return {"x-asgard-workspace": workspace_id}


@mcp.tool()
def list_articles(
    workspace_id: Annotated[str, Field(description="Workspace ID")],
    page: Annotated[int, Field(description="Page number")] = 1,
    size: Annotated[int, Field(description="Page size")] = 20,
) -> dict:
    """List articles for a workspace."""
    return api_get(
        "list_articles",
        params={"page": page, "size": size},
        extra_headers=_workspace_header(workspace_id),
    )


@mcp.tool()
def get_article(
    workspace_id: Annotated[str, Field(description="Workspace ID")],
    article_id: Annotated[str, Field(description="Article ID")],
) -> dict:
    """Get an article by ID."""
    return api_get(
        "get_article",
        path_params={"article_id": article_id},
        extra_headers=_workspace_header(workspace_id),
    )


@mcp.tool()
def list_article_templates(
    workspace_id: Annotated[str, Field(description="Workspace ID")],
    page: Annotated[int, Field(description="Page number")] = 1,
    size: Annotated[int, Field(description="Page size")] = 20,
) -> dict:
    """List article templates for a workspace."""
    return api_get(
        "list_article_templates",
        params={"page": page, "size": size},
        extra_headers=_workspace_header(workspace_id),
    )


@mcp.tool()
def get_article_template(
    workspace_id: Annotated[str, Field(description="Workspace ID")],
    article_template_id: Annotated[str, Field(description="Article template ID")],
) -> dict:
    """Get an article template by ID."""
    return api_get(
        "get_article_template",
        path_params={"article_template_id": article_template_id},
        extra_headers=_workspace_header(workspace_id),
    )
