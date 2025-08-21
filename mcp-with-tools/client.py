import requests


url = "http://localhost:8000/mcp/"

headers = {
    "Accept": "application/json, text/event-stream" 
}

body = {
    "jsonrpc": "2.0",
    "method":"tools/list", 
    "params":{}, 
    "id":1
}

response = requests.post(url, headers=headers, json=body)
print("-"*100)
print(f"Response:")
print(response.text)
print("-"*100)