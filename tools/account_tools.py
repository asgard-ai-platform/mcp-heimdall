"""Tools for account (platform account) resources."""

from typing import Annotated, Optional

from pydantic import Field

from app import mcp
from connectors.rest_client import api_get


def _workspace_header(workspace_id: str) -> dict:
    return {"x-asgard-workspace": workspace_id}


@mcp.tool()
def list_accounts(
    workspace_id: Annotated[str, Field(description="Workspace ID")],
    page: Annotated[int, Field(description="Page number")] = 1,
    size: Annotated[int, Field(description="Page size")] = 20,
    provider_type: Annotated[Optional[str], Field(description="Filter by provider type")] = None,
    app_id: Annotated[Optional[str], Field(description="Filter by app ID")] = None,
) -> dict:
    """List platform accounts for a workspace."""
    params: dict = {"page": page, "size": size}
    if provider_type:
        params["provider_type"] = provider_type
    if app_id:
        params["app_id"] = app_id
    return api_get("list_accounts", params=params, extra_headers=_workspace_header(workspace_id))


@mcp.tool()
def get_account(
    workspace_id: Annotated[str, Field(description="Workspace ID")],
    account_id: Annotated[str, Field(description="Account ID")],
) -> dict:
    """Get a platform account by ID."""
    return api_get(
        "get_account",
        path_params={"account_id": account_id},
        extra_headers=_workspace_header(workspace_id),
    )


@mcp.tool()
def get_accounts_by_avatar(
    workspace_id: Annotated[str, Field(description="Workspace ID")],
    avatar_id: Annotated[str, Field(description="Avatar ID")],
) -> dict:
    """Get all platform accounts linked to an avatar."""
    return api_get(
        "get_accounts_by_avatar",
        path_params={"avatar_id": avatar_id},
        extra_headers=_workspace_header(workspace_id),
    )
