class MockModel:
    """A stand-in for an AI model. It gives the same simple replies every time."""

    def reply(self, instructions, history):
        last_message = history[-1]["content"].lower()
        if "hello" in last_message:
            return "Hello! How can I help you today?"
        return "I'm not sure how to help with that. I can check an order or stock."


if __name__ == "__main__":
    model = MockModel()
    history = [{"role": "user", "content": "Hello there"}]
    print(model.reply("Be friendly.", history))

    history = [{"role": "user", "content": "Do you price match?"}]
    print(model.reply("Be friendly.", history))
