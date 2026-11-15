# my_main.py
# Author: Mason Dedeaux

from my_assistant import CafeAssistant
from my_tool import CafeToolbox, FaqLookup, ReservationQueue
from ollama_model import OllamaModel

ANSWERS = {
    "hours": "Our mock cafe is open Monday through Friday, 7 am to 4 pm.",
    "parking": "Free parking is available behind our mock cafe.",
    "wi-fi": "Our mock cafe has free guest Wi-Fi; ask staff for the password.",
}


def main():
    instructions = """You are Bean, a friendly cafe assistant. Answer briefly.
If the customer just says hello, greet them and ask how you can help.
Use look_up_faq to answer questions about hours, parking, or Wi-Fi.
Copy the relevant words exactly from the customer's message when asking the tool.
For a table reservation, ask for the customer's name and desired day and time.
Use request_reservation only when the customer asks for a table and supplies both details.
Use the exact name and time they gave you, and say staff will review any queued request.
If a tool refuses a detail, ask the customer for it. Always wait for staff approval.
If you do not know an answer, say so and ask the customer to contact staff.
Do not invent facts or confirm availability."""
    queue = ReservationQueue()
    tools = CafeToolbox(FaqLookup(ANSWERS), queue)
    bot = CafeAssistant("Bean", instructions, tools, OllamaModel("granite4.1:3b"))

    print("Type a message, or type quit to stop.")
    user_message = input("You: ")
    while user_message != "quit":
        print(f"{bot.name}: {bot.respond(user_message)}")
        user_message = input("You: ")
    print(f"Messages in this conversation: {len(bot.history)}")

    print("Staff review")
    for request in queue.waiting():
        number = request["number"]
        print(f"Request {number}: {request['name']} at {request['time']}")
        if input("Approve? yes or no: ").strip().lower() == "yes":
            print(queue.approve(number))
        else:
            print(queue.reject(number))
    print(f"Reservations: {len(queue.reservations)}")


if __name__ == "__main__":
    main()
