from dotenv import load_dotenv
from openai import OpenAI
from tools import list_files, read_file, write_file, run_python_file
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
    input="Create a Python file called self_test.py that prints the result of adding 5 and 7. Run the file to verify it works. If execution fails, inspect the error, fix the code, and run it again until it succeeds.",
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
        arguments = json.loads(tool_call.arguments)
        path = arguments["path"]

        # Execute the correct tool call
        if tool_call.name == "list_files":
            result = list_files(path)
            # Add its result to the tool_outputs list
        elif tool_call.name == "read_file":
            result = read_file(path)
        elif tool_call.name == "write_file":
            content = arguments["content"]
            result = write_file(path, content)
        elif tool_call.name == "run_python_file":
            result = run_python_file(path)

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
