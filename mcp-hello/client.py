import requests


url = "http://localhost:8000/mcp/"

headers = {
    "Accept": "application/json, text/event-stream" # client is ready to receive JSON or streaming events (SSE). Matches with MCP transport layer spec
}

body = {
    "jsonrpc": "2.0",
    "method":"tools/list", # asks the server for a list of available tools
    "params":{}, # we are not passing any extra argument because function doesn't requires
    "id":1
}

response = requests.post(url, headers=headers, json=body)
print("-"*100)
print(f"Response:\n")
print(response.text)
print("-"*100)