#!/usr/bin/env python3
"""Entry point for the MCP server."""

# Import tool modules to trigger @mcp.tool() decorator registration.
from . import tools  # noqa: F401
from .tools import article_tools  # noqa: F401
from .tools import avatar_tools  # noqa: F401
from .tools import account_tools  # noqa: F401
from .tools import app_tools  # noqa: F401
from .tools import blob_tools  # noqa: F401
from .tools import content_source_tools  # noqa: F401
from .tools import mission_tools  # noqa: F401
from .tools import publication_tools  # noqa: F401
from .tools import topic_tools  # noqa: F401
from .tools import workspace_tools  # noqa: F401

from .app import mcp


def main():
    mcp.run()


if __name__ == "__main__":
    main()
