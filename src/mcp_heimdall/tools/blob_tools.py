"""Tools for blob resources."""

from typing import Annotated, Optional

from pydantic import Field

from ..app import mcp
from ..connectors.rest_client import api_get


def _workspace_header(workspace_id: str) -> dict:
    return {"x-asgard-workspace": workspace_id}


@mcp.tool()
def list_blobs(
    workspace_id: Annotated[str, Field(description="Workspace ID")],
    page: Annotated[int, Field(description="Page number")] = 1,
    size: Annotated[int, Field(description="Page size")] = 20,
    filter_by: Annotated[Optional[str], Field(description="Filter field name")] = None,
    filter_value: Annotated[Optional[str], Field(description="Filter field value")] = None,
) -> dict:
    """List blob records for a workspace."""
    params: dict = {"page": page, "size": size}
    if filter_by:
        params["filter_by"] = filter_by
    if filter_value:
        params["filter_value"] = filter_value
    return api_get("list_blobs", params=params, extra_headers=_workspace_header(workspace_id))
