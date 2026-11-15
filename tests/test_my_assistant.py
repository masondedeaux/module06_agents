from fake_model import FakeModel
from my_assistant import CafeAssistant
from my_tool import CafeToolbox, FaqLookup, ReservationQueue


def make_assistant(decisions):
    faq = FaqLookup({"hours": "Open 7 am to 4 pm."})
    return CafeAssistant(
        "Bean",
        "You are a friendly cafe assistant. Ask staff if you do not know.",
        CafeToolbox(faq, ReservationQueue()),
        FakeModel(decisions),
    )


def tool_request(tool_name, **arguments):
    return {"tool": tool_name, "arguments": arguments}


def test_faq_uses_supplied_tool():
    bot = make_assistant(
        [tool_request("look_up_faq", topic="hours"), {"text": "Open 7 am to 4 pm."}]
    )
    assert bot.respond("What are your HOURS?") == "Open 7 am to 4 pm."
    assert bot.history[1]["content"] == "Open 7 am to 4 pm."


def test_failed_lookup_points_to_staff():
    bot = make_assistant(
        [tool_request("look_up_faq", topic="patio"), {"text": "Please ask staff."}]
    )
    bot.respond("Do you have a patio?")
    assert "Please ask staff" in bot.history[1]["content"]


def test_unsupported_request_is_safe():
    bot = make_assistant([{"text": "I can help with cafe questions."}])
    assert bot.respond("Write my essay") == "I can help with cafe questions."


def test_sensitive_request_goes_to_staff_before_the_model():
    bot = make_assistant([])
    reply = bot.respond("During your hours, can you handle my allergy?")
    assert "staff member" in reply
    assert bot.model.calls == 0


def test_history_records_exact_content():
    bot = make_assistant([{"text": "Hello! How can I help you today?"}])
    reply = bot.respond("hello")
    assert bot.history == [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": reply},
    ]


def test_assistants_have_independent_histories():
    first = make_assistant([{"text": "Hello!"}])
    second = make_assistant([])
    first.respond("hello")
    assert len(first.history) == 2
    assert second.history == []


def test_greeting_uses_model():
    bot = make_assistant([{"text": "Hello! How can I help you today?"}])
    assert bot.respond("hello") == "Hello! How can I help you today?"


def test_unavailable_model_gets_safe_reply():
    bot = make_assistant([None])
    assert "try again" in bot.respond("What are your hours?")


def test_unknown_and_incomplete_tool_requests_are_refused():
    bot = make_assistant([])
    assert "no tool named" in bot.tools.run("delete_reservation", {}, [])
    assert "their name" in bot.tools.run(
        "request_reservation", {"name": None, "time": "Monday 9 am"}, []
    )
    assert bot.tools.queue.waiting() == []


def test_made_up_reservation_time_is_refused():
    bot = make_assistant(
        [
            tool_request("request_reservation", name="Dana Cruz", time="Monday 9 am"),
            {"text": "What day and time would you like?"},
        ]
    )
    bot.respond("Please reserve a table for Dana Cruz.")
    assert "has not given that time" in bot.history[1]["content"]
    assert bot.tools.queue.waiting() == []


def test_reservation_waits_and_can_be_approved_once():
    bot = make_assistant(
        [
            tool_request("request_reservation", name="Dana Cruz", time="Monday 9 am"),
            {"text": "I sent your request to staff."},
        ]
    )
    bot.respond("Please reserve a table for Dana Cruz at Monday 9 am.")
    queue = bot.tools.queue
    assert queue.waiting()[0]["status"] == "waiting"
    assert queue.reservations == []
    assert queue.approve(1) == "Request 1 approved."
    assert queue.approve(1) == "Request 1 is already approved."
    assert queue.reservations == [{"name": "Dana Cruz", "time": "Monday 9 am"}]
    assert queue.waiting() == []
