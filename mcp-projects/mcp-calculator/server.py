from mcp.server.fastmcp import FastMCP

mcp: FastMCP = FastMCP(
    name="MCP Calculator",
    debug=True,
    log_level="INFO",
    stateless_http=True
)

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@mcp.tool()
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

@mcp.prompt()
def calculator_prompt() -> str:
    return (
        "You are a calculator. You can perform addition, subtraction, multiplication, and division. "
        "Use the provided tools to perform calculations as needed. Explain the math step-by-step for students"
    )

mcp_app = mcp.streamable_http_app()

if __name__ == "__main__":
    mcp.run()