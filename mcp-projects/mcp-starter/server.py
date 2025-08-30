from mcp.server.fastmcp import FastMCP
from datetime import datetime

mcp: FastMCP = FastMCP(
    name="MCP Starter",
    log_level="INFO",
    debug=True,
    stateless_http=True
)
@mcp.tool()
def get_current_datetime():
    """
    A tool that returns current date and time
    """
    return datetime.now().isoformat()


@mcp.prompt()
def greeting_prompt(user_name: str):
    """
    A function that gives prompt for greeting user
    """
    return f"You are helpful friendly assistant that greets user {user_name}"

mcp_app = mcp.streamable_http_app()

if __name__ == "__main__":
    mcp.run() #run the command `uv run mcp dev server.py`