import asyncio
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP

load_dotenv()

url = "http://localhost:8000/mcp/"

server = MCPServerStreamableHTTP(url=url)  
agent = Agent("openai:gpt-4.1", toolsets=[server])

async def main():
    async with agent:
        user_input = input("Ask the agent something: ")
        result = await agent.run(user_input)
        print(result.output)

asyncio.run(main())