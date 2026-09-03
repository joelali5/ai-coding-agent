from dotenv import load_dotenv
from openai import OpenAI
from tools import list_files
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
    }
]

first_response = client.responses.create(
    model="gpt-5.6-luna",
    input="What files are inside my project?",
    tools=tools
)

for item in first_response.output:
    if item.type == "function_call":
        if item.name == "list_files":
            path = json.loads(item.arguments)["path"]
            result = list_files(path)

            second_response = client.responses.create(
                model="gpt-5.6-luna",
                previous_response_id=first_response.id,
                input=[
                    {
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": json.dumps(result)
                    }
                ]
            )

            print(second_response.output_text)