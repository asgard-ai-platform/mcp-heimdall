"""Public import smoke tests."""

import importlib.metadata


def test_package_imports():
    import mcp_heimdall
    from mcp_heimdall.app import mcp
    from mcp_heimdall.server import main

    assert mcp_heimdall is not None
    assert mcp is not None
    assert callable(main)


def test_console_script_registered():
    entry_points = importlib.metadata.distribution("mcp-heimdall").entry_points
    scripts = {entry.name: entry.value for entry in entry_points if entry.group == "console_scripts"}

    assert scripts["mcp-heimdall"] == "mcp_heimdall.server:main"
