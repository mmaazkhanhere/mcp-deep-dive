from pydantic import Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="mcp-with-tools-server",
    stateless_http=True
)

@mcp.tool()
def search_web(query: str) -> str:
    """
    A function that takes users query and search website. 
    
    Args:
    query: str -> The user query

    Response:
    Web search result
    """
    return f"Result for {query} is ...."

@mcp.tool(
    name="get_temperature",
    description="A function that returns the current temperature for a given city"
) # a different way to let the LLM know which tools are available
def get_temperature(city: str = Field(description="The name of the city")) -> str:
    """
    A function that takes a city name and returns the current temperature.

    Args:
    city: str -> The name of the city

    Response:
    Current temperature in the city
    """
    return f"Current temperature in {city} is ...."

mcp_app = mcp.streamable_http_app()