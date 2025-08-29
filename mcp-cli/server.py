from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

mcp: FastMCP = FastMCP(
    name="Calculator",
    log_level="INFO",
    debug=True,
    stateless_http=True
)

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

if __name__ == "__main__":
    load_dotenv()
    mcp.run() #run the command `uv run mcp dev server.py`
# mcp_app = mcp.streamable_http_app()