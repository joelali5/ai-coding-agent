from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# response = client.responses.create(
#     model="gpt-5.6-luna",
#     input="What tools might a coding agent need?"
# )
response = client.responses.create(
    model="gpt-5.6-luna",
    input="What files are inside my project?"
)

print(response.output_text)