# Security Policy

## Reporting a Vulnerability

If you discover a security issue in `mcp-heimdall`, please do not open a public issue with exploit details.

Report the issue to Asgard AI Platform through GitHub Security Advisories or by contacting the maintainers listed in the repository metadata.

Please include:

- Affected version or commit
- Steps to reproduce
- Impact and affected configuration
- Any relevant logs or error messages, with secrets removed

## Scope

`mcp-heimdall` is a read-only MCP server. It uses `HEIMDALL_API_TOKEN` to call Heimdall API endpoints with the permissions granted to that token.

The server does not bypass Heimdall authorization checks and does not expose write operations through MCP tools.

## Secret Handling

- Never commit `.env` files or real API tokens.
- Use `.env.example` only as a public template.
- Rotate `HEIMDALL_API_TOKEN` immediately if it is exposed.
