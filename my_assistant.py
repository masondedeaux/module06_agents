class CafeAssistant:  # Organize a mock cafe assistant's state and behavior.
    def __init__(self, name, tool):  # Receive a name and a separate FAQ tool.
        self.name = name  # Store the name used in greetings.
        self.tool = tool  # Composition: store the tool instead of cafe facts.
        self.history = []  # Give each assistant its own conversation history.

    def respond(self, user_message):  # Process one message and save both sides.
        self.history.append({"role": "user", "content": user_message})  # Record input.
        reply = self.choose_reply(user_message)  # Select a response for this turn.
        self.history.append({"role": "assistant", "content": reply})  # Record output.
        return reply  # Let the CLI or a test read the chosen answer.

    def choose_reply(self, user_message):  # Use rules rather than an AI model.
        text = user_message.lower()  # Normalize the message for keyword matching.
        for word in ["allerg", "refund", "payment", "card"]:  # Identify staff topics.
            if word in text:  # Check handoff rules before informational replies.
                return "Please ask a cafe staff member about that; I can't handle it here."  # Handoff.
        if "hello" in text:  # Handle a simple greeting.
            return f"Hello! I'm {self.name}. Ask about our hours, parking, or Wi-Fi."  # Explain scope.
        if "?" in text or any(
            word in text for word in ["hours", "parking", "wi-fi"]
        ):  # FAQ route.
            answer = self.tool.find_answer(user_message)  # Ask the separate tool.
            if answer is None:  # Handle a lookup with no matching stored fact.
                return "I don't have that information. Try hours, parking, or Wi-Fi, or ask staff."  # Clarify.
            return answer  # Return the stored fact without inventing details.
        return "I'm not sure how to help with that. I can answer cafe FAQs."  # Safe fallback.
