# Configuration

`mcp-heimdall` is configured with environment variables.

## Environment Variables

| Variable | Required | Default | Description |
|---|---:|---|---|
| `HEIMDALL_API_TOKEN` | Yes | - | Bearer token used to authenticate with the Heimdall API. |
| `HEIMDALL_API_BASE_URL` | No | `https://heimdall-api.asgard-ai.com` | API base URL override. Do not include `/v1`; versioned paths are added by the server. |

## Example `.env`

```env
HEIMDALL_API_TOKEN=your_access_token_here
HEIMDALL_API_BASE_URL=https://heimdall-api.asgard-ai.com
```

`HEIMDALL_API_BASE_URL` can be omitted when using the default production API.

## MCP Client Configuration

Claude Desktop example:

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

For a local checkout, use `uv --directory`:

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
