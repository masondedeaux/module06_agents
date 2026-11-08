# my_main.py
# Author: Mason Dedeaux

from my_assistant import CafeAssistant
from my_tool import FaqLookup
from ollama_model import OllamaModel

ANSWERS = {
    "hours": "Our mock cafe is open Monday through Friday, 7 am to 4 pm.",
    "parking": "Free parking is available behind our mock cafe.",
    "wi-fi": "Our mock cafe has free guest Wi-Fi; ask staff for the password.",
}


def main():
    instructions = """You are Bean, a friendly cafe assistant.
The cafe is open Monday through Friday, 7 am to 4 pm.
Free parking is available behind the cafe.
The cafe has free guest Wi-Fi; ask staff for the password.
If you do not know an answer, say so and ask the customer to contact staff.
Do not invent facts. Answer briefly."""

    bot = CafeAssistant(
        "Bean",
        FaqLookup(ANSWERS),
        instructions,
        OllamaModel("granite4.1:3b"),
    )
    print("Type a message, or type quit to stop.")
    user_message = input("You: ")
    while user_message != "quit":
        print(f"{bot.name}: {bot.respond(user_message)}")
        user_message = input("You: ")
    print(f"Messages in this conversation: {len(bot.history)}")


if __name__ == "__main__":
    main()
