"""Tools for mission and mission content resources."""

from typing import Annotated, Optional

from pydantic import Field

from app import mcp
from connectors.rest_client import api_get


def _workspace_header(workspace_id: str) -> dict:
    return {"x-asgard-workspace": workspace_id}


@mcp.tool()
def list_missions(
    workspace_id: Annotated[str, Field(description="Workspace ID")],
    page: Annotated[int, Field(description="Page number")] = 1,
    size: Annotated[int, Field(description="Page size")] = 20,
    topic_id: Annotated[Optional[str], Field(description="Filter by topic ID")] = None,
    avatar_id: Annotated[Optional[str], Field(description="Filter by avatar ID")] = None,
    mission_type: Annotated[Optional[str], Field(description="Filter by mission type")] = None,
    q: Annotated[Optional[str], Field(description="Search by keywords in topic titles, avatar names, or descriptions")] = None,
    sort_by: Annotated[Optional[str], Field(description="Sort by field")] = None,
    sort_order: Annotated[Optional[str], Field(description="Sort order: asc or desc")] = None,
) -> dict:
    """List missions for a workspace."""
    params: dict = {"page": page, "size": size}
    if topic_id:
        params["topic_id"] = topic_id
    if avatar_id:
        params["avatar_id"] = avatar_id
    if mission_type:
        params["mission_type"] = mission_type
    if q:
        params["q"] = q
    if sort_by:
        params["sort_by"] = sort_by
    if sort_order:
        params["sort_order"] = sort_order
    return api_get("list_missions", params=params, extra_headers=_workspace_header(workspace_id))


@mcp.tool()
def get_mission(
    workspace_id: Annotated[str, Field(description="Workspace ID")],
    mission_id: Annotated[str, Field(description="Mission ID")],
) -> dict:
    """Get a mission by ID."""
    return api_get(
        "get_mission",
        path_params={"mission_id": mission_id},
        extra_headers=_workspace_header(workspace_id),
    )


@mcp.tool()
def export_mission(
    workspace_id: Annotated[str, Field(description="Workspace ID")],
    mission_id: Annotated[str, Field(description="Mission ID")],
) -> dict:
    """Export a mission with its contents."""
    return api_get(
        "export_mission",
        path_params={"mission_id": mission_id},
        extra_headers=_workspace_header(workspace_id),
    )


@mcp.tool()
def list_mission_contents(
    workspace_id: Annotated[str, Field(description="Workspace ID")],
    page: Annotated[int, Field(description="Page number")] = 1,
    size: Annotated[int, Field(description="Page size")] = 20,
    mission_id: Annotated[Optional[str], Field(description="Filter by mission ID")] = None,
    avatar_id: Annotated[Optional[str], Field(description="Filter by avatar ID")] = None,
    status: Annotated[Optional[str], Field(description="Filter by status: pending, generating, completed, failed")] = None,
) -> dict:
    """List mission contents for a workspace."""
    params: dict = {"page": page, "size": size}
    if mission_id:
        params["mission_id"] = mission_id
    if avatar_id:
        params["avatar_id"] = avatar_id
    if status:
        params["status"] = status
    return api_get("list_mission_contents", params=params, extra_headers=_workspace_header(workspace_id))


@mcp.tool()
def get_mission_content(
    workspace_id: Annotated[str, Field(description="Workspace ID")],
    mission_content_id: Annotated[str, Field(description="Mission content ID")],
) -> dict:
    """Get a mission content by ID."""
    return api_get(
        "get_mission_content",
        path_params={"mission_content_id": mission_content_id},
        extra_headers=_workspace_header(workspace_id),
    )
