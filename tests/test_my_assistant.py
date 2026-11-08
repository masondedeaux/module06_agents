from mock_model import MockModel
from my_assistant import CafeAssistant
from my_tool import FaqLookup


def make_assistant():
    return CafeAssistant(
        "Bean",
        FaqLookup({"hours": "Open 7 am to 4 pm."}),
        "You are a friendly cafe assistant. Ask staff if you do not know.",
        MockModel(),
    )


class SilentModel:
    def reply(self, instructions, history):
        return None


def test_faq_uses_supplied_tool():
    bot = make_assistant()
    assert bot.respond("What are your HOURS?") == "Open 7 am to 4 pm."


def test_failed_lookup_uses_model():
    bot = make_assistant()
    assert bot.respond("Do you have a patio?") == (
        "I'm not sure how to help with that. I can check an order or stock."
    )
    assert FaqLookup({}).find_answer("hours") is None


def test_unsupported_request_is_safe():
    assert "not sure" in make_assistant().respond("Write my essay")


def test_sensitive_request_goes_to_staff_before_faq():
    reply = make_assistant().respond("During your hours, can you handle my allergy?")
    assert "staff member" in reply


def test_history_records_exact_content():
    bot = make_assistant()
    reply = bot.respond("hello")
    assert bot.history == [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": reply},
    ]


def test_assistants_have_independent_histories():
    first = make_assistant()
    second = make_assistant()
    first.respond("hello")
    assert len(first.history) == 2
    assert second.history == []


def test_greeting_uses_model():
    bot = make_assistant()
    assert bot.respond("hello") == "Hello! How can I help you today?"


def test_silent_model_gets_safe_reply():
    bot = make_assistant()
    bot.model = SilentModel()
    assert bot.respond("hello") == (
        "Sorry, I can't answer that right now. Please ask a cafe staff member."
    )


def test_faq_works_with_silent_model():
    bot = make_assistant()
    bot.model = SilentModel()
    assert bot.respond("What are your hours?") == "Open 7 am to 4 pm."


def test_handoff_works_with_silent_model():
    bot = make_assistant()
    bot.model = SilentModel()
    assert "staff member" in bot.respond("I have a peanut allergy")
