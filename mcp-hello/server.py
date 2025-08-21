# Defines a MCP Server

from mcp.server.fastmcp import FastMCP # A helper for spinning up an MCP Server

mcp = FastMCP(
    name="mcp-hello-server", # name of the server
    stateless_http=True # whether the server is stateless. Here, this server doesn't keep session state b/w requests
)

mcp_app = mcp.streamable_http_app() # creates a FastAPI compatible ASGI app that speaks MCP over Streamable HTTP transport. (Transport Layer)