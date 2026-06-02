"""Tools for topic resources."""

from typing import Annotated, Optional

from pydantic import Field

from app import mcp
from connectors.rest_client import api_get


def _workspace_header(workspace_id: str) -> dict:
    return {"x-asgard-workspace": workspace_id}


@mcp.tool()
def list_topics(
    workspace_id: Annotated[str, Field(description="Workspace ID")],
    page: Annotated[int, Field(description="Page number")] = 1,
    size: Annotated[int, Field(description="Page size")] = 20,
    name: Annotated[Optional[str], Field(description="Filter by name")] = None,
) -> dict:
    """List topics for a workspace."""
    params: dict = {"page": page, "size": size}
    if name:
        params["name"] = name
    return api_get("list_topics", params=params, extra_headers=_workspace_header(workspace_id))


@mcp.tool()
def get_topic(
    workspace_id: Annotated[str, Field(description="Workspace ID")],
    topic_id: Annotated[str, Field(description="Topic ID")],
) -> dict:
    """Get a topic by ID."""
    return api_get(
        "get_topic",
        path_params={"topic_id": topic_id},
        extra_headers=_workspace_header(workspace_id),
    )


@mcp.tool()
def list_topic_categories(
    workspace_id: Annotated[str, Field(description="Workspace ID")],
) -> dict:
    """List all available topic categories."""
    return api_get(
        "list_topic_categories",
        extra_headers=_workspace_header(workspace_id),
    )
