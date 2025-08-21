import requests


url = "http://localhost:8000/mcp/"

headers = {
    "Accept": "application/json, text/event-stream" 
}

# body = {
#     "jsonrpc": "2.0",
#     "method":"tools/list", 
#     "params":{}, 
#     "id":1
# }

web_body = {
    "jsonrpc": "2.0",
    "method":"tools/call", # This is the method to call a tool
    "params":{
        "name": "search_web", # Name of the function
        "arguments":{ # arguments that need to pass to the function to call it
            "query":"What is MCP?"
        }
    }, 
    "id":1
}

temperature_body = {
    "jsonrpc": "2.0",
    "method":"tools/call", 
    "params":{
        "name": "get_temperature", 
        "arguments":{
            "city":"New York"
        }
    }, 
    "id":2
}

web_response = requests.post(url, headers=headers, json=web_body)
temperature_response = requests.post(url, headers=headers, json=temperature_body)

print("-"*100)
print(f"Response:")
print(web_response.text)
print("-"*100)
print("\n")
print(f"Response:")
print(temperature_response.text)
print("-"*100)