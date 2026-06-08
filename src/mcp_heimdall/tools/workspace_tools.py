"""Tools for workspace resources."""

from typing import Annotated

from pydantic import Field

from ..app import mcp
from ..connectors.rest_client import api_get


@mcp.tool()
def list_workspaces() -> dict:
    """List all workspaces accessible to the current user."""
    return api_get("list_workspaces")


@mcp.tool()
def get_workspace(
    workspace_id: Annotated[str, Field(description="Workspace ID")],
) -> dict:
    """Get a workspace by ID."""
    return api_get(
        "get_workspace",
        path_params={"workspace_id": workspace_id},
    )
