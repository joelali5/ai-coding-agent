from dotenv import load_dotenv
from openai import OpenAI
from tools import list_files, read_file, write_file, run_python_file
import json

load_dotenv()

client = OpenAI()

user_request = input("What would you like me to do? ")

tool_registry = {
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
    "run_python_file": run_python_file
}

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
    },
    {
    "name": "write_file",
    "type": "function",
    "description": "Write content to a file inside the project directory.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The file path to write to."
            },
            "content": {
                "type": "string",
                "description": "The content to write to the file."
            }
        },
        "required": ["path", "content"],
        "additionalProperties": False
    }
},
    {
    "name": "run_python_file",
    "type": "function",
    "description": "Run a Python file and return its output.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The file path to run."
            }
        },
        "required": ["path"],
        "additionalProperties": False
    }
}]

response = client.responses.create(
    model="gpt-5.6-luna",
    input=user_request,
    tools=tools
)

max_iterations = 10
iteration = 0

while iteration < max_iterations:
    iteration += 1
    tool_calls = []

    for item in response.output:
        if item.type == "function_call":
            tool_calls.append(item)

    if not tool_calls:
        print(response.output_text)
        break
      
    tool_outputs = []

    for tool_call in tool_calls:
        try:
            arguments = json.loads(tool_call.arguments)

            tool_function = tool_registry[tool_call.name]

            result = tool_function(**arguments)
    
        except Exception as error:
            result = {
                "error": str(error)
            }

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
else:
    print("Agent stopped: maximum number of iterations reached.")