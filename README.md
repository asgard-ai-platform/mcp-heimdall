# mcp-heimdall

[![CI](https://github.com/asgard-ai-platform/mcp-heimdall/actions/workflows/ci.yml/badge.svg)](https://github.com/asgard-ai-platform/mcp-heimdall/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/mcp-heimdall.svg)](https://pypi.org/project/mcp-heimdall/)
[![Python versions](https://img.shields.io/pypi/pyversions/mcp-heimdall.svg)](https://pypi.org/project/mcp-heimdall/)
[![GitHub tag](https://img.shields.io/github/v/tag/asgard-ai-platform/mcp-heimdall)](https://github.com/asgard-ai-platform/mcp-heimdall/tags)
[![GitHub stars](https://img.shields.io/github/stars/asgard-ai-platform/mcp-heimdall)](https://github.com/asgard-ai-platform/mcp-heimdall/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/asgard-ai-platform/mcp-heimdall)](https://github.com/asgard-ai-platform/mcp-heimdall/issues)
[![GitHub last commit](https://img.shields.io/github/last-commit/asgard-ai-platform/mcp-heimdall)](https://github.com/asgard-ai-platform/mcp-heimdall/commits/main)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-compatible-blue)](https://modelcontextprotocol.io/)

Heimdall — an MCP (Model Context Protocol) server that exposes read-only tools for Asgard's content management platform.

Provides `list` and `get` tools for all major resources: articles, blobs, content sources, article templates, avatars, accounts, apps, missions, mission contents, publications, topics, and workspaces.

[繁體中文](README.zh-TW.md)

Part of the [Asgard AI Platform](https://github.com/asgard-ai-platform) open-source ecosystem.

---

## What This Does

- **23 MCP tools** covering workspace, article, avatar, account, app, blob, content source, mission, publication, and topic resources
- **Read-only tool surface** for safe AI assistant access
- **Bearer token authentication** through `HEIMDALL_API_TOKEN`
- **Public-safe configuration** through environment variables and `.env.example`
- **stdio transport** for local MCP clients

See [docs/tools.md](docs/tools.md) for the full public tool reference.

---

## Quick Start

### Install

```bash
pip install mcp-heimdall
```

Run with `uvx` without installing globally:

```bash
uvx mcp-heimdall
```

For local development:

```bash
git clone https://github.com/asgard-ai-platform/mcp-heimdall.git
cd mcp-heimdall
uv sync
```

### Configure

```bash
cp .env.example .env
# Edit .env — set your token. The base URL is optional unless you need an override:
#   HEIMDALL_API_TOKEN=<your bearer token>
#   HEIMDALL_API_BASE_URL=<API base URL override>
```

See [docs/configuration.md](docs/configuration.md) for details.

### Run

```bash
uv run mcp-heimdall
```

Or explicitly:
```bash
uv run python -m mcp_heimdall.server
```

### Use with Claude Desktop

Package install / `uvx` example:

```json
{
  "mcpServers": {
    "heimdall": {
      "command": "uvx",
      "args": ["mcp-heimdall"],
      "env": {
        "HEIMDALL_API_TOKEN": "your_bearer_token_here"
      }
    }
  }
}
```

For a local checkout, run it through `uv` from the repository directory:

```json
{
  "mcpServers": {
    "heimdall": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/mcp-heimdall", "mcp-heimdall"],
      "env": {
        "HEIMDALL_API_TOKEN": "your_bearer_token_here"
      }
    }
  }
}
```

More examples are available in [examples/](examples/).

### Use with Claude Code

After installing the package and configuring environment variables, add the stdio MCP server:

```bash
claude mcp add heimdall -- mcp-heimdall
```

For a local checkout:

```bash
claude mcp add heimdall -- uv --directory /path/to/mcp-heimdall run mcp-heimdall
```

---

## Test

```bash
# Public import smoke test
uv run python tests/test_imports.py

# Unit tests (mocked HTTP, no live API needed)
uv run python -m pytest tests/test_all_tools.py -v

# Compile source and tests
uv run python -m compileall src tests

# Build source distribution and wheel
uv build
```

---

## Configuration

| Environment Variable     | Required | Default | Description                  |
|--------------------------|----------|---------|------------------------------|
| `HEIMDALL_API_TOKEN`     | Yes      | —       | Bearer token for the API     |
| `HEIMDALL_API_BASE_URL`  | No       | `https://heimdall-api.asgard-ai.com` | API base URL override |

---

## MCP Tools

All workspace-scoped tools require a `workspace_id` parameter.  
Use `list_workspaces` first to discover available workspace IDs.

### Workspace

| Tool | Description | Parameters |
|------|-------------|------------|
| `list_workspaces` | List all workspaces for the current user | — |
| `get_workspace` | Get a workspace by ID | `workspace_id` |

### Article

| Tool | Description | Parameters |
|------|-------------|------------|
| `list_articles` | List articles in a workspace | `workspace_id`, `page`, `size` |
| `get_article` | Get an article by ID | `workspace_id`, `article_id` |

### Article Template

| Tool | Description | Parameters |
|------|-------------|------------|
| `list_article_templates` | List article templates in a workspace | `workspace_id`, `page`, `size` |
| `get_article_template` | Get an article template by ID | `workspace_id`, `article_template_id` |

### Avatar

| Tool | Description | Parameters |
|------|-------------|------------|
| `list_avatars` | List avatars in a workspace | `workspace_id`, `page`, `size`, `name`\*, `gender`\* |
| `get_avatar` | Get an avatar by ID | `workspace_id`, `avatar_id` |

### Account (Platform Account)

| Tool | Description | Parameters |
|------|-------------|------------|
| `list_accounts` | List platform accounts in a workspace | `workspace_id`, `page`, `size`, `provider_type`\*, `app_id`\* |
| `get_account` | Get a platform account by ID | `workspace_id`, `account_id` |
| `get_accounts_by_avatar` | Get all accounts linked to an avatar | `workspace_id`, `avatar_id` |

### App (OAuth App)

| Tool | Description | Parameters |
|------|-------------|------------|
| `list_apps` | List OAuth apps in a workspace | `workspace_id`, `page`, `size`, `provider_type`\* |
| `get_app` | Get an OAuth app by ID | `workspace_id`, `app_id` |

### Blob

| Tool | Description | Parameters |
|------|-------------|------------|
| `list_blobs` | List blob records in a workspace | `workspace_id`, `page`, `size`, `filter_by`\*, `filter_value`\* |

### Content Source

| Tool | Description | Parameters |
|------|-------------|------------|
| `list_content_sources` | List content sources in a workspace | `workspace_id`, `page`, `size` |
| `get_content_source` | Get a content source by ID | `workspace_id`, `content_source_id` |

### Mission

| Tool | Description | Parameters |
|------|-------------|------------|
| `list_missions` | List missions in a workspace | `workspace_id`, `page`, `size`, `topic_id`\*, `avatar_id`\*, `mission_type`\*, `q`\*, `sort_by`\*, `sort_order`\* |
| `get_mission` | Get a mission by ID | `workspace_id`, `mission_id` |
| `export_mission` | Export a mission with all its contents | `workspace_id`, `mission_id` |

### Mission Content

| Tool | Description | Parameters |
|------|-------------|------------|
| `list_mission_contents` | List mission contents in a workspace | `workspace_id`, `page`, `size`, `mission_id`\*, `avatar_id`\*, `status`\* |
| `get_mission_content` | Get a mission content by ID | `workspace_id`, `mission_content_id` |

### Publication

| Tool | Description | Parameters |
|------|-------------|------------|
| `list_publications` | List publications in a workspace | `workspace_id`, `page`, `size` |
| `get_publication` | Get a publication by ID | `workspace_id`, `publication_id` |

### Topic

| Tool | Description | Parameters |
|------|-------------|------------|
| `list_topics` | List topics in a workspace | `workspace_id`, `page`, `size`, `name`\* |
| `get_topic` | Get a topic by ID | `workspace_id`, `topic_id` |
| `list_topic_categories` | List all available topic categories | `workspace_id` |

\* optional filter parameter

---

## MCP Client Configuration

Add this to your MCP client config (e.g. Claude Desktop `claude_desktop_config.json`) when running from a local checkout:

```json
{
  "mcpServers": {
    "heimdall": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/mcp-heimdall", "mcp-heimdall"],
      "env": {
        "HEIMDALL_API_TOKEN": "your_bearer_token_here"
      }
    }
  }
}
```

Or with a `.env` file:

```json
{
  "mcpServers": {
    "heimdall": {
      "command": "uv",
      "args": [
        "run",
        "--env-file", "/path/to/mcp-heimdall/.env",
        "--directory", "/path/to/mcp-heimdall",
        "mcp-heimdall"
      ]
    }
  }
}
```

---

## Documentation

- [Configuration](docs/configuration.md)
- [Tools](docs/tools.md)

---

## Boundaries

- The server exposes read-only MCP tools only.
- The server operates with the permissions of the configured `HEIMDALL_API_TOKEN`.
- Heimdall write APIs are intentionally not exposed through this MCP server.
- Public documentation intentionally avoids linking to private backend API documents.

---

## Architecture

```
stdio (JSON-RPC 2.0)
  → mcp-heimdall (console script entry point)
    → src/mcp_heimdall/server.py       — entry point, imports trigger tool registration
      → src/mcp_heimdall/app.py        — MCPServer singleton (FastMCP "mcp-heimdall")
        → src/mcp_heimdall/tools/*     — @mcp.tool() decorated functions
          → src/mcp_heimdall/connectors/rest_client.py  — HTTP client with retry + extra_headers support
            → src/mcp_heimdall/auth/bearer.py           — reads HEIMDALL_API_TOKEN env var
              → src/mcp_heimdall/config/settings.py     — base URL + endpoint map
```

## License

MIT
