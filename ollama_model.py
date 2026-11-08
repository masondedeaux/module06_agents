# ollama_model.py
# Author: Mason Dedeaux

from httpx import RequestError
from ollama import Client, ResponseError


class OllamaModel:
    """Ask a local Ollama model for a reply."""

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
