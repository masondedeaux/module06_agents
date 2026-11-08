HANDOFF_WORDS = ["address", "payment", "card"]


class SupportChatbot:  # Bundle conversation state and response methods.
    def __init__(self, name, instructions, order_tool, stock_tool, model):
        self.name = name  # Keep this bot's name for its greeting.
        self.instructions = instructions  # Store instructions as mock metadata.
        self.order_tool = order_tool  # Composition: give the bot an order tool.
        self.stock_tool = stock_tool  # Composition: give it a separate stock tool.
        self.model = model  # Store the model this bot will use.
        self.history = []  # Create a fresh list so bots do not share messages.

    def respond(self, user_message):  # Handle and record one conversation turn.
        self.history.append({"role": "user", "content": user_message})  # Log input.
        reply = self.choose_reply(user_message)  # Apply this bot's reply rules.
        self.history.append({"role": "assistant", "content": reply})  # Log output.
        return reply  # Give the response to the calling program.

    def choose_reply(self, user_message):  # Pick a reply with mock keyword rules.
        text = user_message.lower()  # Normalize text for case-insensitive checks.
        if self.needs_human(text):  # Give sensitive requests highest priority.
            return "I can't help with that here. I'm passing you to a human agent."  # Handoff.
        if "order" in text:  # Route order questions to the order tool method.
            return self.order_reply(user_message)  # Return the lookup reply.
        if "stock" in text:  # Route stock questions to the second tool method.
            return self.stock_reply(user_message)  # Return the stock lookup reply.
        reply = self.model.reply(self.instructions, self.history)
        if not isinstance(reply, str) or not reply.strip():
            return "Sorry, I can't answer that right now. Please try again in a moment."
        return reply

    def needs_human(self, text):  # Decide whether a person must handle the request.
        for word in HANDOFF_WORDS:  # Examine each sensitive keyword.
            if word in text:  # Use the lab's simple substring matching rule.
                return True  # Stop as soon as a handoff word is found.
        return False  # Allow normal routing when no handoff word occurs.

    def order_reply(self, user_message):  # Answer using the injected order tool.
        order_id = self.order_tool.find_order_id(user_message)  # Find a known ID.
        if order_id is None:  # Handle messages with no recognized order ID.
            return "Which order? Please send an order ID like A100."  # Ask for an ID.
        status = self.order_tool.find_status(order_id)  # Read the stored status.
        if status is None:  # Handle a tool that cannot supply a status.
            return "I couldn't find that order's status. Please ask a human agent."  # Avoid guessing.
        return f"Order {order_id} is {status}."  # Report the tool's actual result.

    def stock_reply(self, user_message):  # Answer using the injected stock tool.
        product = self.stock_tool.find_product(user_message)  # Find a known item.
        if product is None:  # Handle missing or unrecognized product names.
            return (
                "Which product? Please name the item you want me to check."  # Clarify.
            )
        count = self.stock_tool.count_for(product)  # Look up the available count.
        if count is None:  # Handle a failed count lookup without inventing stock.
            return "I couldn't find that stock count. Please ask a human agent."  # Explain.
        return f"We have {count} of the {product} in stock."  # Include zero honestly.

    def count_user_messages(self):  # Exercise 2: count user entries in history.
        count = 0  # Start with no counted messages.
        for message in self.history:  # Visit every recorded conversation entry.
            if message["role"] == "user":  # Exclude assistant replies from counting.
                count += 1  # Count this user message once.
        return count  # Return the number of user turns.
