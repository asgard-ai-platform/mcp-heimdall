#!/usr/bin/env python3
"""Test API connection and validate credentials.

Verifies that environment variables are set and the API is reachable.

Usage:
    python scripts/auth/test_connection.py
"""

import os
import sys

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "src",
    ),
)

from mcp_heimdall.config.settings import BASE_URL, get_headers, get_url


def check_env_vars():
    """Check that required environment variables are set."""
    print("Checking environment variables...")

    required_vars = ["HEIMDALL_API_TOKEN"]

    missing = [var for var in required_vars if not os.environ.get(var)]

    if missing:
        print("  FAIL: Missing environment variables:")
        for var in missing:
            print(f"    - {var}")
        return False

    print("  OK: All required environment variables are set.")
    if not os.environ.get("HEIMDALL_API_BASE_URL"):
        print(f"  INFO: HEIMDALL_API_BASE_URL not set; using default {BASE_URL}")
    return True


def check_connection():
    """Test API connectivity with a simple request."""
    import requests

    print(f"\nTesting connection to {BASE_URL}...")

    try:
        headers = get_headers()
        url = get_url("list_workspaces")
        response = requests.get(
            url,
            headers=headers,
            timeout=15,
        )

        print(f"  Status: {response.status_code}")

        if response.status_code == 200:
            print("  OK: Connection successful.")
            return True
        elif response.status_code == 401:
            print("  FAIL: Authentication failed. Check your credentials.")
            return False
        elif response.status_code == 403:
            print("  FAIL: Access forbidden. Check your permissions/scopes.")
            return False
        else:
            print(f"  WARN: Unexpected status code {response.status_code}")
            print(f"  Response: {response.text[:300]}")
            return False

    except requests.exceptions.ConnectionError:
        print(f"  FAIL: Cannot connect to {BASE_URL}")
        return False
    except requests.exceptions.Timeout:
        print("  FAIL: Connection timed out.")
        return False
    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def main():
    print("=" * 50)
    print("MCP Server — Connection Test")
    print("=" * 50)

    env_ok = check_env_vars()
    if not env_ok:
        print("\nFix the missing environment variables and try again.")
        sys.exit(1)

    conn_ok = check_connection()
    if not conn_ok:
        print("\nConnection test failed.")
        sys.exit(1)

    print("\nAll checks passed. Ready to use.")


if __name__ == "__main__":
    main()
