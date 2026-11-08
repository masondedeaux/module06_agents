# first_chat.py
# Author: Mason Dedeaux

from ollama import Client

client = Client(host="http://127.0.0.1:11434", trust_env=False)

MODEL_NAME = "granite4.1:3b"

INSTRUCTIONS = """You are Sunny, a support assistant for Bayside Outfitters.
Answer in one short sentence."""

messages = [
    {"role": "system", "content": INSTRUCTIONS},
    {"role": "user", "content": "What are your store hours?"},
]

response = client.chat(model=MODEL_NAME, messages=messages)
print(response.message.content)
