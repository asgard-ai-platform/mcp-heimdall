# mcp-heimdall

**Heimdall** — Asgard 內容管理平台的 MCP (Model Context Protocol) 伺服器，提供只讀工具。

提供所有主要資源的 `list` 和 `get` 工具：文章、內容源、文章範本、頭像、帳戶、應用程式、任務、任務內容、發佈物、主題和工作區。

---

## 設置

```bash
# 1. 安裝依賴
uv sync

# 2. 複製並填入認證資訊
cp .env.example .env
# 編輯 .env — 設定兩個必需變數：
#   HEIMDALL_API_TOKEN=<your bearer token>
#   HEIMDALL_API_BASE_URL=<API base URL>
```

---

## 執行

```bash
uv run mcp-heimdall
```

或明確指定：
```bash
uv run python -m mcp_heimdall.server
```

---

## 測試

```bash
# 單元測試（模擬 HTTP，無需連接真實 API）
uv run python -m pytest tests/test_all_tools.py -v
```

---

## 組態

| 環境變數             | 必需 | 預設值 | 說明                 |
|----------------------|------|--------|----------------------|
| `HEIMDALL_API_TOKEN` | 是   | —     | API Bearer Token     |
| `HEIMDALL_API_BASE_URL` | 是 | —     | API 基礎 URL          |

---

## MCP 工具

所有工作區範圍的工具都需要 `workspace_id` 參數。  
使用 `list_workspaces` 先發現可用的工作區 ID。

### 工作區

| 工具 | 說明 | 參數 |
|------|------|------|
| `list_workspaces` | 列出目前使用者的所有工作區 | — |
| `get_workspace` | 按 ID 取得工作區 | `workspace_id` |

### 文章

| 工具 | 說明 | 參數 |
|------|------|------|
| `list_articles` | 列出工作區中的文章 | `workspace_id`, `page`, `size` |
| `get_article` | 按 ID 取得文章 | `workspace_id`, `article_id` |

### 文章範本

| 工具 | 說明 | 參數 |
|------|------|------|
| `list_article_templates` | 列出工作區中的文章範本 | `workspace_id`, `page`, `size` |
| `get_article_template` | 按 ID 取得文章範本 | `workspace_id`, `article_template_id` |

### 頭像

| 工具 | 說明 | 參數 |
|------|------|------|
| `list_avatars` | 列出工作區中的頭像 | `workspace_id`, `page`, `size`, `name`\*, `gender`\* |
| `get_avatar` | 按 ID 取得頭像 | `workspace_id`, `avatar_id` |

### 帳戶（平台帳戶）

| 工具 | 說明 | 參數 |
|------|------|------|
| `list_accounts` | 列出工作區中的平台帳戶 | `workspace_id`, `page`, `size`, `provider_type`\*, `app_id`\* |
| `get_account` | 按 ID 取得平台帳戶 | `workspace_id`, `account_id` |
| `get_accounts_by_avatar` | 取得連結到頭像的所有帳戶 | `workspace_id`, `avatar_id` |

### 應用程式（OAuth 應用程式）

| 工具 | 說明 | 參數 |
|------|------|------|
| `list_apps` | 列出工作區中的 OAuth 應用程式 | `workspace_id`, `page`, `size`, `provider_type`\* |
| `get_app` | 按 ID 取得 OAuth 應用程式 | `workspace_id`, `app_id` |

### Blob

| 工具 | 說明 | 參數 |
|------|------|------|
| `list_blobs` | 列出工作區中的 Blob 記錄 | `workspace_id`, `page`, `size`, `filter_by`\*, `filter_value`\* |

### 內容源

| 工具 | 說明 | 參數 |
|------|------|------|
| `list_content_sources` | 列出工作區中的內容源 | `workspace_id`, `page`, `size` |
| `get_content_source` | 按 ID 取得內容源 | `workspace_id`, `content_source_id` |

### 任務

| 工具 | 說明 | 參數 |
|------|------|------|
| `list_missions` | 列出工作區中的任務 | `workspace_id`, `page`, `size`, `topic_id`\*, `avatar_id`\*, `mission_type`\*, `q`\*, `sort_by`\*, `sort_order`\* |
| `get_mission` | 按 ID 取得任務 | `workspace_id`, `mission_id` |
| `export_mission` | 匯出任務及其所有內容 | `workspace_id`, `mission_id` |

### 任務內容

| 工具 | 說明 | 參數 |
|------|------|------|
| `list_mission_contents` | 列出工作區中的任務內容 | `workspace_id`, `page`, `size`, `mission_id`\*, `avatar_id`\*, `status`\* |
| `get_mission_content` | 按 ID 取得任務內容 | `workspace_id`, `mission_content_id` |

### 發佈物

| 工具 | 說明 | 參數 |
|------|------|------|
| `list_publications` | 列出工作區中的發佈物 | `workspace_id`, `page`, `size` |
| `get_publication` | 按 ID 取得發佈物 | `workspace_id`, `publication_id` |

### 主題

| 工具 | 說明 | 參數 |
|------|------|------|
| `list_topics` | 列出工作區中的主題 | `workspace_id`, `page`, `size`, `name`\* |
| `get_topic` | 按 ID 取得主題 | `workspace_id`, `topic_id` |
| `list_topic_categories` | 列出所有可用的主題分類 | `workspace_id` |

\* 選用的篩選參數

---

## MCP 客戶端組態

將下列內容新增到你的 MCP 客戶端組態中（例如 Claude Desktop `claude_desktop_config.json`）：

```json
{
  "mcpServers": {
    "heimdall": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/mcp-heimdall", "mcp-heimdall"],
      "env": {
        "HEIMDALL_API_TOKEN": "your_bearer_token_here",
        "HEIMDALL_API_BASE_URL": "https://heimdall.example.com"
      }
    }
  }
}
```

或使用 `.env` 檔案：

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

## 架構

```
stdio (JSON-RPC 2.0)
  → mcp-heimdall (console script entry point)
    → src/mcp_heimdall/server.py       — 入口點，匯入觸發工具註冊
      → src/mcp_heimdall/app.py        — MCPServer 單例 (FastMCP "mcp-heimdall")
        → src/mcp_heimdall/tools/*     — @mcp.tool() 裝飾的函數
          → src/mcp_heimdall/connectors/rest_client.py  — HTTP 客戶端（含重試 + extra_headers 支援）
            → src/mcp_heimdall/auth/bearer.py           — 讀取 HEIMDALL_API_TOKEN 環境變數
              → src/mcp_heimdall/config/settings.py     — 基礎 URL + 端點對應表
```

## 授權

MIT
