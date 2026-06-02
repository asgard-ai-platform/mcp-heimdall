"""Tools for publication resources."""

from typing import Annotated

from pydantic import Field

from app import mcp
from connectors.rest_client import api_get


def _workspace_header(workspace_id: str) -> dict:
    return {"x-asgard-workspace": workspace_id}


@mcp.tool()
def list_publications(
    workspace_id: Annotated[str, Field(description="Workspace ID")],
    page: Annotated[int, Field(description="Page number")] = 1,
    size: Annotated[int, Field(description="Page size")] = 20,
) -> dict:
    """List publications for a workspace."""
    return api_get(
        "list_publications",
        params={"page": page, "size": size},
        extra_headers=_workspace_header(workspace_id),
    )


@mcp.tool()
def get_publication(
    workspace_id: Annotated[str, Field(description="Workspace ID")],
    publication_id: Annotated[str, Field(description="Publication ID")],
) -> dict:
    """Get a publication by ID."""
    return api_get(
        "get_publication",
        path_params={"publication_id": publication_id},
        extra_headers=_workspace_header(workspace_id),
    )
