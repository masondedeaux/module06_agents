from my_assistant import CafeAssistant
from my_tool import FaqLookup

ANSWERS = {
    "hours": "Our mock cafe is open Monday through Friday, 7 am to 4 pm.",
    "parking": "Free parking is available behind our mock cafe.",
    "wi-fi": "Our mock cafe has free guest Wi-Fi; ask staff for the password.",
}


def main():
    bot = CafeAssistant("Bean", FaqLookup(ANSWERS))
    print("Type a message, or type quit to stop.")
    user_message = input("You: ")
    while user_message != "quit":
        print(f"{bot.name}: {bot.respond(user_message)}")
        user_message = input("You: ")
    print(f"Messages in this conversation: {len(bot.history)}")


if __name__ == "__main__":
    main()
