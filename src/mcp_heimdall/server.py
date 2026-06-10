#!/usr/bin/env python3
"""Entry point for the MCP server."""

# Import tool modules to trigger @mcp.tool() decorator registration.
from . import tools  # noqa: F401
from .app import mcp
from .tools import (
    account_tools,  # noqa: F401
    app_tools,  # noqa: F401
    article_tools,  # noqa: F401
    avatar_tools,  # noqa: F401
    blob_tools,  # noqa: F401
    content_source_tools,  # noqa: F401
    mission_tools,  # noqa: F401
    publication_tools,  # noqa: F401
    topic_tools,  # noqa: F401
    workspace_tools,  # noqa: F401
)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
