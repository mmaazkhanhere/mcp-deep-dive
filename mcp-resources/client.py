import json
import requests

url = "http://localhost:8000/mcp/"  # Only if using HTTP transport
headers = {"Accept": "application/json, text/event-stream"}

# 1. List resources
res = requests.post(
    url,
    headers=headers,
    json={"jsonrpc": "2.0", "method": "resources/list", "params": {}, "id": 1}
)
print("Resources List:", res.text)

# 2. Read the greeting resource
res = requests.post(
    url,
    headers=headers,
    json={
        "jsonrpc": "2.0",
        "method": "resources/read",
        "params": {"uri": "resource://greeting"},
        "id": 2,
    }
)

print("Resource Content:", res.text)

# Greeting
res = requests.post(
    url,
    headers=headers,
    json={
        "jsonrpc": "2.0",
        "method": "resources/read",
        "params": {
            "uri": "greeting://Alice"
        },
        "id": 3,
    }
)

print("Greeting Resource:", res.text)

# Tool call
res = requests.post(
    url,
    headers=headers,
    json={
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "add",
            "arguments":{
                "a": 5,
                "b": 10
            }
        },
        "id": 4
    }
)

print("Tool Call Result:", res.text)
