# Tools

All workspace-scoped tools require a `workspace_id` parameter. Use `list_workspaces` first to discover available workspace IDs.

## Workspace

| Tool | Purpose |
|---|---|
| `list_workspaces` | List workspaces available to the current token. |
| `get_workspace` | Get a workspace by ID. |

## Article

| Tool | Purpose |
|---|---|
| `list_articles` | List articles in a workspace. |
| `get_article` | Get an article by ID. |
| `list_article_templates` | List article templates in a workspace. |
| `get_article_template` | Get an article template by ID. |

## Avatar And Account

| Tool | Purpose |
|---|---|
| `list_avatars` | List avatars in a workspace. |
| `get_avatar` | Get an avatar by ID. |
| `list_accounts` | List platform accounts in a workspace. |
| `get_account` | Get a platform account by ID. |
| `get_accounts_by_avatar` | Get all accounts linked to an avatar. |

## App

| Tool | Purpose |
|---|---|
| `list_apps` | List OAuth apps in a workspace. |
| `get_app` | Get an OAuth app by ID. |

## Blob And Content Source

| Tool | Purpose |
|---|---|
| `list_blobs` | List blob records in a workspace. |
| `list_content_sources` | List content sources in a workspace. |
| `get_content_source` | Get a content source by ID. |

## Mission

| Tool | Purpose |
|---|---|
| `list_missions` | List missions in a workspace. |
| `get_mission` | Get a mission by ID. |
| `export_mission` | Export a mission with its contents. |
| `list_mission_contents` | List mission contents in a workspace. |
| `get_mission_content` | Get a mission content by ID. |

## Publication

| Tool | Purpose |
|---|---|
| `list_publications` | List publications in a workspace. |
| `get_publication` | Get a publication by ID. |

## Topic

| Tool | Purpose |
|---|---|
| `list_topics` | List topics in a workspace. |
| `get_topic` | Get a topic by ID. |
| `list_topic_categories` | List available topic categories. |

## Boundaries

- Tools are read-only from the MCP server perspective.
- Access is limited by the permissions attached to `HEIMDALL_API_TOKEN`.
- The server does not expose Heimdall write APIs through MCP tools.
- Public documentation intentionally does not link to private backend API documents.
