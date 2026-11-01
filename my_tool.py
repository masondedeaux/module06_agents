class FaqLookup:  # Keep cafe FAQ data independent of conversation code.
    def __init__(self, answers):  # Receive topic names mapped to factual replies.
        self.answers = answers  # Store the made-up cafe's FAQ dictionary.

    def find_answer(self, text):  # Find an answer for a topic in the message.
        for topic in self.answers:  # Check each known FAQ keyword in order.
            if topic.lower() in text.lower():  # Match regardless of letter case.
                return self.answers[topic]  # Return only a stored FAQ answer.
        return None  # Signal that the tool has no matching information.
