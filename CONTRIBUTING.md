# Contributing

Thank you for contributing to mcp-heimdall!

## Setup

```bash
git clone https://github.com/asgard-ai-platform/mcp-heimdall.git
cd mcp-heimdall
uv sync
cp .env.example .env
# Edit .env with your credentials
```

## Adding a New Tool

1. **Choose module**: Pick an existing file in `src/mcp_heimdall/tools/` or create a new `src/mcp_heimdall/tools/{domain}_tools.py`
2. **Import helpers**: 
   ```python
   from ..connectors.rest_client import api_get
   from ..app import mcp
   ```
3. **Write the tool**:
   ```python
   from typing import Annotated
   from pydantic import Field
   from ..app import mcp
   from ..connectors.rest_client import api_get

   @mcp.tool()
   def my_new_tool(
       workspace_id: Annotated[str, Field(description="Workspace ID")],
       param: Annotated[str, Field(description="What this param does")] = "default",
   ) -> dict:
       """What this tool does — shown in MCP tools/list."""
       data = api_get("endpoint_key", path_params={"id": param})
       return {"result": data}
   ```
4. **Register**: If you created a new module, add it to the imports in `src/mcp_heimdall/server.py`:
   ```python
   from .tools import your_new_module  # noqa: F401
   ```
5. **Test**: Add a test case in `tests/test_all_tools.py`
6. **Verify**: Run `uv run pytest tests/test_all_tools.py -v`

## Code Conventions

- English for code, docstrings, and tool descriptions
- Use connector helpers from `src/mcp_heimdall/connectors/` — never call `requests` directly in tool functions
- Use relative imports within the package: `from ..app import mcp`, `from ..config.settings import ...`
- All tools return `dict`
- Use Pydantic `Field()` with `Annotated` for parameter descriptions and defaults
- Use `Annotated[type, Field(...)]` pattern to avoid FieldInfo leaks when calling functions directly

## Testing

All tests use mocked HTTP responses:
```bash
# Validate credentials against live API
uv run python scripts/auth/test_connection.py

# Run all tool unit tests (no live API needed)
uv run pytest tests/test_all_tools.py -v
```

## Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/add-workspace-export`
3. Make your changes
4. Run tests to ensure they pass
5. Submit a PR with a clear description of the changes and any new tools added
