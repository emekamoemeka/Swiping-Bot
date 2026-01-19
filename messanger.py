from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("prompt.txt", "r") as f:
    system_prompt = f.read()

DB_FILE = "conversations.json"

def load_database():
    """Load conversations from database file"""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_database(db):
    """Save conversations to database file"""
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

def print_conversation_history(history):
    """Print conversation history"""
    print("\n=== Conversation History ===")
    for msg in history:
        if msg["role"] == "user":
            print(f"You: {msg['content']}")
        elif msg["role"] == "assistant":
            print(f"AI: {msg['content']}")
    print("=" * 30 + "\n")

db = load_database()

name = input("Enter name: ").strip()

if name in db:
    print(f"\n✓ Found conversation with {name}")
    conversation_history = db[name]
    print_conversation_history(conversation_history)
else:
    print(f"\n✓ Starting new conversation with {name}")
    conversation_history = [
        {"role": "system", "content": system_prompt}
    ]

user_message = input("Enter your message: ").strip()

conversation_history.append({"role": "user", "content": user_message})

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=conversation_history,
    max_tokens=50
)

ai_response = response.choices[0].message.content

conversation_history.append({"role": "assistant", "content": ai_response})

# Print AI response
print(f"\nAI: {ai_response}\n")

# Save conversation to database
db[name] = conversation_history
save_database(db)

print(f"✓ Conversation saved to database")
