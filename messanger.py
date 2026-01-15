from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt_path = os.path.join(os.path.dirname(__file__), "prompt.txt")
with open(prompt_path, "r", encoding="utf-8") as f:
    prompt_text = f.read()
lines = prompt_text.splitlines()
clean_lines = [line for line in lines if not line.strip().startswith("```")]
prompt_text = "\n".join(clean_lines).strip()

conversation_history = [
    {"role": "system", "content": prompt_text},
    {"role": "user", "content": "Hey, how’s it going?"}
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=conversation_history,
    max_tokens=50
)

print(response.choices[0].message.content)
