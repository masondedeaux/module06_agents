from chatbot import SupportChatbot

STAFF_TOPICS = ("allerg", "refund", "payment", "card")


class CafeAssistant(
    SupportChatbot
):  # Reuse the limited tool loop and conversation history.
    """Bean answers cafe questions and sends sensitive topics to staff."""

    def choose_reply(
        self, user_message
    ):  # Check cafe staff rules before calling the model.
        text = user_message.lower()  # Match staff topics regardless of capitalization.
        if any(
            topic in text for topic in STAFF_TOPICS
        ):  # Stop sensitive requests here.
            return "Please ask a cafe staff member about that; I can't handle it here."
        return self.model_reply()  # Let the model request a checked cafe tool.
