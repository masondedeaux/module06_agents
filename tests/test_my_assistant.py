from my_assistant import CafeAssistant
from my_tool import FaqLookup


def make_assistant():
    return CafeAssistant("Bean", FaqLookup({"hours": "Open 7 am to 4 pm."}))


def test_faq_uses_supplied_tool():
    bot = make_assistant()
    assert bot.respond("What are your HOURS?") == "Open 7 am to 4 pm."


def test_failed_lookup_is_helpful():
    bot = make_assistant()
    assert "don't have that information" in bot.respond("Do you have a patio?")
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
