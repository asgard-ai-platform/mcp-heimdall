"""Tools for avatar resources."""

from typing import Annotated, Optional

from pydantic import Field

from app import mcp
from connectors.rest_client import api_get


def _workspace_header(workspace_id: str) -> dict:
    return {"x-asgard-workspace": workspace_id}


@mcp.tool()
def list_avatars(
    workspace_id: Annotated[str, Field(description="Workspace ID")],
    page: Annotated[int, Field(description="Page number")] = 1,
    size: Annotated[int, Field(description="Page size")] = 20,
    name: Annotated[Optional[str], Field(description="Filter by name")] = None,
    gender: Annotated[Optional[str], Field(description="Filter by gender")] = None,
) -> dict:
    """List avatars for a workspace."""
    params: dict = {"page": page, "size": size}
    if name:
        params["name"] = name
    if gender:
        params["gender"] = gender
    return api_get("list_avatars", params=params, extra_headers=_workspace_header(workspace_id))


@mcp.tool()
def get_avatar(
    workspace_id: Annotated[str, Field(description="Workspace ID")],
    avatar_id: Annotated[str, Field(description="Avatar ID")],
) -> dict:
    """Get an avatar by ID."""
    return api_get(
        "get_avatar",
        path_params={"avatar_id": avatar_id},
        extra_headers=_workspace_header(workspace_id),
    )
