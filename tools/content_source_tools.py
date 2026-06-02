"""Tools for content source resources."""

from typing import Annotated

from pydantic import Field

from app import mcp
from connectors.rest_client import api_get


def _workspace_header(workspace_id: str) -> dict:
    return {"x-asgard-workspace": workspace_id}


@mcp.tool()
def list_content_sources(
    workspace_id: Annotated[str, Field(description="Workspace ID")],
    page: Annotated[int, Field(description="Page number")] = 1,
    size: Annotated[int, Field(description="Page size")] = 20,
) -> dict:
    """List content sources for a workspace."""
    return api_get(
        "list_content_sources",
        params={"page": page, "size": size},
        extra_headers=_workspace_header(workspace_id),
    )


@mcp.tool()
def get_content_source(
    workspace_id: Annotated[str, Field(description="Workspace ID")],
    content_source_id: Annotated[str, Field(description="Content source ID")],
) -> dict:
    """Get a content source by ID."""
    return api_get(
        "get_content_source",
        path_params={"content_source_id": content_source_id},
        extra_headers=_workspace_header(workspace_id),
    )
