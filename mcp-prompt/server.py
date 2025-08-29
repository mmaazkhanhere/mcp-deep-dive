from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="mcp-prompt-server",
    stateless_http=True,
    debug=True,
    log_level="INFO"
)

@mcp.prompt()
def greeting_prompt(name: str):
    """
    A simple reusable prompt template that greets user
    """
    return f"You are a helpful assistant. Greet the user named {name}"

mcp_app = mcp.streamable_http_app()