from dotenv import load_dotenv
from openai import OpenAI
from tools import list_files, read_file
import json

load_dotenv()

client = OpenAI()

tools = [
    {
        "name": "list_files",
        "type": "function",
        "description": "List all files in the current directory",
        "parameters": {
            "type": "object",
            "properties":{
                "path":{
                    "type": "string",
                    "description": "The directory path to inspect."
                }
            },
            "required": ["path"],
            "additionalProperties": False
        }
    },
    {
        "name": "read_file",
        "type": "function",
        "description": "Read and return the contents of a file.",
        "parameters": {
            "type": "object",
            "properties":{
                "path":{
                    "type": "string",
                    "description": "The file path to inspect."
                }
            },
            "required": ["path"],
            "additionalProperties": False
        }
    }
]

response = client.responses.create(
    model="gpt-5.6-luna",
    input="Inspect my project and explain what this application currently does. Read the relevant files before answering.",
    tools=tools
)

while True:
    tool_calls = []

    for item in response.output:
        if item.type == "function_call":
            tool_calls.append(item)

    if not tool_calls:
        print(response.output_text)
        break
      
    tool_outputs = []

    for tool_call in tool_calls:
        path = json.loads(tool_call.arguments)["path"]
        # Execute the correct tool call
        if tool_call.name == "list_files":
            result = list_files(path)
            # Add its result to the tool_outputs list
        elif tool_call.name == "read_file":
            result = read_file(path)
            
        tool_outputs.append({
            "type": "function_call_output",
            "call_id": tool_call.call_id,
            "output": json.dumps(result)
        })

    response = client.responses.create(
        model="gpt-5.6-luna",
        previous_response_id=response.id,
        input=tool_outputs,
        tools=tools
    )
