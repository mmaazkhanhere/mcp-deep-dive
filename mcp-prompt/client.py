import requests

url = "http://localhost:8000/mcp/"
headers = {"Accept": "application/json, text/event-stream"}

# Step 1: List all prompts
list_body = {
    "jsonrpc": "2.0",
    "method": "prompts/list",
    "params": {},
    "id": 1
}

list_response = requests.post(url, headers=headers, json=list_body)
print("Prompts List:\n", list_response.text)

# Step 2: Get a specific prompt (with input)
get_body = {
    "jsonrpc": "2.0",
    "method": "prompts/get",
    "params": {"name": "greeting_prompt", "arguments": {"name": "Maaz"}},
    "id": 2
}

get_response = requests.post(url, headers=headers, json=get_body)
print("\nPrompt Content:\n", get_response.text)
