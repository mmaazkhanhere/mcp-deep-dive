from mcp.server.fastmcp import FastMCP
from mcp.types import Resource

mcp: FastMCP = FastMCP(
    name="mcp-resource-server",
    stateless_http=True
)

@mcp.tool()
def add(a: int, b: int) ->  int:
    """Add two integers"""
    return a + b

@mcp.resource("resource://config")
def get_config()->dict:
    """Return application configuration"""
    return {
        "version": "1.0",
        "maintainer": "yourname@example.com"
    }

@mcp.resource("resource://config/version")
def get_version()->str:
    """Return application version"""
    return "1.0"

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Return a greeting message"""
    return f"Hello, {name}! Welcome to our service."

@mcp.resource("resource://greeting")
def greeting_resource() -> str:
    """Returns a greeting message dynamically."""
    from datetime import datetime
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning from MCP!"
    elif hour < 18:
        return "Good afternoon from MCP!"
    else:
        return "Good evening from MCP!"

mcp_app = mcp.streamable_http_app()