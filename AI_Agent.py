
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

response = client.responses.create(
    model="gpt-5",
    input="Explain to a 5 year old the different species of butterflies and the importantance of biodiversity"
)

print(response.output_text)