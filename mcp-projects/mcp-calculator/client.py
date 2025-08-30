import asyncio
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP

load_dotenv()

url = "http://localhost:8000/mcp/"

server = MCPServerStreamableHTTP(url=url)

agent = Agent("openai:gpt-4.1", toolsets=[server], instructions="You can only access MCP. ANything unrelated to MCP should be ignored")

async def main():
    async with agent:
        user_input = input("Hi. How can I help you with maths. I can do basic arithmetic operation: ")
        while user_input not in ['q', 'Q']:
            
            result = await agent.run(user_input)
            print(result.output)
            user_input = input("Enter 'q' to quit or continue ") 

asyncio.run(main())