# Changelog

## [0.1.0] - 2026-06-08

### Added
- Initial release of Heimdall MCP server
- Read-only tools for Asgard Heimdall
- 23 MCP tools across 12 resource types:
  - Workspace (list, get)
  - Article (list, get, list templates, get template)
  - Avatar (list, get)
  - Account (list, get, get by avatar)
  - App (list, get)
  - Blob (list)
  - Content Source (list, get)
  - Mission (list, get, export, list contents, get content)
  - Publication (list, get)
  - Topic (list, get, list categories)
- Bearer token authentication via HEIMDALL_API_TOKEN environment variable
- Workspace-scoped requests via x-asgard-workspace header
- Pagination support with configurable page/size parameters
- Optional filtering parameters (name, provider_type, status, etc.)
- Comprehensive unit test suite (39 tests)
- REST API connector with retry logic and error handling
- src-layout package structure following mcp-template standards
- MCP client configuration examples for Claude Desktop
- Multi-language documentation (English, 繁體中文)
