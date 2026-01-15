from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

conversation_history = [
    {"role": "system", "content": "” RULES: - Match their energy - If they reply with one word, keep it short - Avoid paragraphs - Don’t ask more than one question at a time"},
    {"role": "user", "content": "Hey, how’s it going?"}
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=conversation_history,
    max_tokens=50
)

print(response.choices[0].message.content)
