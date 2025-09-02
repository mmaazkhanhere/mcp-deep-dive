# client.py
import asyncio
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP

load_dotenv()

server = MCPServerStreamableHTTP(url="http://localhost:8000/mcp/")

SUMMARY_PROMPT = """
You can ONLY use MCP resources/tools.

Goal:
- Summarize a selected Markdown note into EXACTLY 3 bullet points.

How to behave:
1) To discover notes, call resource `notes://index`.
2) If the user named a note, use that. Otherwise, use tool `search_notes(query)` to find candidates,
   pick the best match, and then read it with tool `read_note(name)`.
3) Produce OUTPUT as exactly three concise bullet points. No intro, no outro, no code fences.

Examples of valid outputs:
- Point one...
- Point two...
- Point three...
"""

agent = Agent(
    "openai:gpt-4.1",
    toolsets=[server],
    instructions=SUMMARY_PROMPT,
)

async def main():
    async with agent:
        user_input = input("Notes Assistant › Ask me to summarize a note (q to quit): ")
        while user_input not in ("q", "Q"):
            result = await agent.run(user_input)
            print(result.output)
            user_input = input("\n(q to quit) › ")

asyncio.run(main())
