"""Tools for OAuth app resources."""

from typing import Annotated, Optional

from pydantic import Field

from ..app import mcp
from ..connectors.rest_client import api_get


def _workspace_header(workspace_id: str) -> dict:
    return {"x-asgard-workspace": workspace_id}


@mcp.tool()
def list_apps(
    workspace_id: Annotated[str, Field(description="Workspace ID")],
    page: Annotated[int, Field(description="Page number")] = 1,
    size: Annotated[int, Field(description="Page size")] = 20,
    provider_type: Annotated[Optional[str], Field(description="Filter by provider type")] = None,
) -> dict:
    """List OAuth apps for a workspace."""
    params: dict = {"page": page, "size": size}
    if provider_type:
        params["provider_type"] = provider_type
    return api_get("list_apps", params=params, extra_headers=_workspace_header(workspace_id))


@mcp.tool()
def get_app(
    workspace_id: Annotated[str, Field(description="Workspace ID")],
    app_id: Annotated[str, Field(description="App ID")],
) -> dict:
    """Get an OAuth app by ID."""
    return api_get(
        "get_app",
        path_params={"app_id": app_id},
        extra_headers=_workspace_header(workspace_id),
    )
