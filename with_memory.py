# with_memory.py
# Author: Mason Dedeaux

from ollama import Client

client = Client(host="http://127.0.0.1:11434", trust_env=False)
MODEL_NAME = "granite4.1:3b"

INSTRUCTIONS = """You are Sunny, a support assistant for Bayside Outfitters.
Answer in one short sentence."""

messages = [{"role": "system", "content": INSTRUCTIONS}]

messages.append({"role": "user", "content": "Hello, my name is Dana."})
response = client.chat(model=MODEL_NAME, messages=messages)
print(response.message.content)
messages.append({"role": "assistant", "content": response.message.content})

messages.append({"role": "user", "content": "What is my name?"})
response = client.chat(model=MODEL_NAME, messages=messages)
print(response.message.content)
messages.append({"role": "assistant", "content": response.message.content})

print(len(messages))