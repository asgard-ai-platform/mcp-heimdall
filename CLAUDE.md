# mcp-heimdall

**Heimdall** — Asgard 內容管理平台的 MCP (Model Context Protocol) 伺服器，提供 AI 可呼叫的只讀工具。

## 設置

```bash
# 安裝依賴
uv sync

# 設定認證
cp .env.example .env
# 編輯 .env — 設定 HEIMDALL_API_TOKEN；HEIMDALL_API_BASE_URL 可選
```

## 執行

```bash
uv run mcp-heimdall
```

## 測試

```bash
# 測試連線
uv run python scripts/auth/test_connection.py

# 執行所有工具測試
uv run pytest tests/test_all_tools.py -v
```

## 架構

```
stdio (JSON-RPC 2.0)
  → mcp-heimdall (console script entry point)
    → src/mcp_heimdall/server.py (entry point, side-effect imports trigger tool registration)
      → src/mcp_heimdall/app.py (MCPServer singleton)
        → src/mcp_heimdall/tools/*.py (@mcp.tool() decorated functions)
          → src/mcp_heimdall/connectors/rest_client.py (HTTP REST connector)
            → src/mcp_heimdall/auth/bearer.py (Bearer token authentication)
              → src/mcp_heimdall/config/settings.py (API endpoints, URL builder)
```

## 工具概覽

23 個 MCP 工具涵蓋 12 個資源類型：

- **Workspace**: list, get
- **Article**: list, get, list_templates, get_template
- **Avatar**: list, get
- **Account**: list, get, get_by_avatar
- **App**: list, get
- **Blob**: list
- **Content Source**: list, get
- **Mission**: list, get, export, list_contents, get_content
- **Publication**: list, get
- **Topic**: list, get, list_categories

## 關鍵模式

- **套件結構**: `src/mcp_heimdall/` — 標準 src-layout 結構
- **單例模式**: `app.py` 建立 `MCPServer` 實例
- **裝飾器註冊**: `@mcp.tool()` 配合 Pydantic `Annotated[type, Field(...)]`
- **工具發現**: `server.py` 匯入工具模組以觸發註冊
- **連接器**: 僅使用 REST API connector（`rest_client.py`）
- **認證**: Bearer Token 認證（`auth/bearer.py`）
- **相對匯入**: 所有工具使用相對匯入 (`from ..app import mcp`, `from ..connectors.rest_client import api_get`)

## 新增工具

1. 選擇適當的工具模組在 `src/mcp_heimdall/tools/` 中
2. 匯入連接器: `from ..connectors.rest_client import api_get`
3. 使用 `@mcp.tool()` 裝飾器編寫工具函數
4. 若建立新模組，在 `src/mcp_heimdall/server.py` 中新增匯入
5. 在 `tests/test_all_tools.py` 中新增測試

## 程式碼規範

- 英文編寫所有程式碼、文件字串和工具說明
- 使用 `Annotated[type, Field(...)]` 模式作為參數描述和預設值
- 所有工具返回 `dict`
- 在工具函數中絕不直接呼叫 `requests` — 使用連接器幫手
- 使用相對匯入以保持套件獨立性
