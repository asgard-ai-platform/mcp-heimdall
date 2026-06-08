# mcp-heimdall

MCP (Model Context Protocol) server that exposes read-only tools for the Asgard Auto Post API.

Provides `list` and `get` tools for all major resources: articles, blobs, content sources, article templates, avatars, accounts, apps, missions, mission contents, publications, topics, and workspaces.

---

## Setup

```bash
# 1. Install dependencies
uv sync

# 2. Copy and fill in your credentials
cp .env.example .env
# Edit .env — set both required variables:
#   AUTO_POST_API_TOKEN=<your bearer token>
#   AUTO_POST_API_BASE_URL=<API base URL>
```

---

## Run

```bash
uv run mcp-heimdall
```

Or explicitly:
```bash
uv run python -m mcp_heimdall.server
```

---

## Test

```bash
# Unit tests (mocked HTTP, no live API needed)
uv run python -m pytest tests/test_all_tools.py -v
```

---

## Configuration

| Environment Variable     | Required | Default                                      | Description                  |
|--------------------------|----------|----------------------------------------------|------------------------------|
| `AUTO_POST_API_TOKEN`    | Yes      | —  | Bearer token for the API     |
| `AUTO_POST_API_BASE_URL` | Yes      | —  | API base URL                 |

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

Add this to your MCP client config (e.g. Claude Desktop `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "heimdall": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/mcp-heimdall", "mcp-heimdall"],
      "env": {
        "AUTO_POST_API_TOKEN": "your_bearer_token_here",
        "AUTO_POST_API_BASE_URL": "https://auto-post-api.example.com"
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

## Architecture

```
stdio (JSON-RPC 2.0)
  → mcp-heimdall (console script entry point)
    → src/mcp_heimdall/server.py       — entry point, imports trigger tool registration
      → src/mcp_heimdall/app.py        — MCPServer singleton (FastMCP "mcp-heimdall")
        → src/mcp_heimdall/tools/*     — @mcp.tool() decorated functions
          → src/mcp_heimdall/connectors/rest_client.py  — HTTP client with retry + extra_headers support
            → src/mcp_heimdall/auth/bearer.py           — reads AUTO_POST_API_TOKEN env var
              → src/mcp_heimdall/config/settings.py     — base URL + endpoint map
```

## License

MIT
