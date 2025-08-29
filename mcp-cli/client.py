import requests

url = "http://localhost:8000/mcp/"

headers = {
    "Accept": "application/json, text/event-stream" 
}


body = {
    "jsonrpc":"2.0",
    "method": "tools/call",
    "params":{
        "name":"add",
        "arguments":{
            "a": 21,
            "b": 10
        }
    },
    "id":1
}

response = requests.post(url, headers=headers, json=body)
print(response.text)