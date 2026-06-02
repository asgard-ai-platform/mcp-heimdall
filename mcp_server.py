#!/usr/bin/env python3
import tools.article_tools  # noqa: F401
import tools.avatar_tools  # noqa: F401
import tools.account_tools  # noqa: F401
import tools.app_tools  # noqa: F401
import tools.blob_tools  # noqa: F401
import tools.content_source_tools  # noqa: F401
import tools.mission_tools  # noqa: F401
import tools.publication_tools  # noqa: F401
import tools.topic_tools  # noqa: F401
import tools.workspace_tools  # noqa: F401

from app import mcp


def main():
    mcp.run()


if __name__ == "__main__":
    main()
