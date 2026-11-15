# ollama_model.py
# Author: Mason Dedeaux

from httpx import RequestError
from ollama import Client, ResponseError


class OllamaModel:
    """Ask a local Ollama model for a reply or a tool request."""

    def __init__(self, model_name):
        self.model_name = model_name
        self.client = Client(
            host="http://127.0.0.1:11434",
            trust_env=False,
            timeout=120.0,
        )

    def reply(self, instructions, history):
        messages = [{"role": "system", "content": instructions}]
        messages = messages + history
        try:
            response = self.client.chat(
                model=self.model_name,
                messages=messages,
            )
            return response.message.content
        except (ConnectionError, ResponseError, RequestError):
            return None

    def decide(self, instructions, history, tools):
        """Send the conversation and tools. Return a reply or a tool request."""
        messages = [{"role": "system", "content": instructions}]
        for message in history:
            if message["role"] == "tool":
                messages.extend(self.tool_messages(message))
            else:
                messages.append(message)

        try:
            response = self.client.chat(
                model=self.model_name,
                messages=messages,
                tools=tools,
            )
        except (ConnectionError, ResponseError, RequestError):
            return None

        if response.message.tool_calls:
            call = response.message.tool_calls[0]
            return {"tool": call.function.name, "arguments": call.function.arguments}
        return {"text": response.message.content}

    def tool_messages(self, message):
        """Turn one recorded tool use into the two messages Ollama expects."""
        name = message["tool_name"]
        request = {"function": {"name": name, "arguments": message["arguments"]}}
        return [
            {"role": "assistant", "content": "", "tool_calls": [request]},
            {"role": "tool", "tool_name": name, "content": message["content"]},
        ]
