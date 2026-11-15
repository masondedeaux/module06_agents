# Lab 10: OOP for Agents

This folder contains the Week 10 lab, all four exercises, and the mini-project.
The programs use Python's standard library; pytest and Ruff are development tools.

## Set up and run

From this folder in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
.\.venv\Scripts\python.exe two_bots.py
.\.venv\Scripts\python.exe my_main.py
```

Type `quit` to end either interactive conversation.
Sunny can look up order A100, A101, or A102 and stock for rain jacket or hiking boots.
`exercise1.md` labels the original class parts; the other exercises add message
counting, stock lookup, and two bots that share tools but keep separate histories.

## Mini-project: Bean, a cafe FAQ assistant

Bean answers questions about the hours, parking, and Wi-Fi at a made-up cafe by using a separate FAQ lookup tool.
It is a mock because its answers come from a fixed dictionary and keyword rules rather than a live business system or an AI model.
Allergy, refund, payment, and card requests go to staff because they require human judgment or involve sensitive information and money.
Unknown questions get a helpful missing-information reply, and unsupported requests get a safe fallback.
If real customer data were used, the conversation history could accidentally retain private payment or health details that someone typed into the chat.

## Verification ritual

```powershell
.\.venv\Scripts\python.exe -m ruff format .
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m pytest -v
```

## AI assistance and submission
I used ChatGPT for explanations and debugging support while completing this lab. The specific assistance is documented in AI_DISCLOSURE.md.

## Week 11: Cafe Assistant with a Model

I added Ollama to my cafe assistant so it can respond to messages that its rules do not cover.
The model answered my greeting, "hello", with "Hello! How may I assist you today?"
When I asked whether the cafe sells blueberry muffins, it said it did not have that information and told me to contact staff.
I kept hours, parking, and Wi-Fi answers in the FAQ tool so those facts come from stored data.
I also kept allergy, refund, and payment handoffs in code because those requests need a staff member.
If the model returns no answer, the assistant gives a safe message asking the customer to contact staff.

## Week 12: Bean's tools and staff review

I gave Bean a tool for cafe questions and a second tool for requesting table reservations. In the tests, the hours question returned the hours stored in the FAQ. When the model tried to book Monday at 9 am and the customer had only given their name, the toolbox refused the time and the request stayed out of the queue. I told the model to copy the name and time exactly from the customer's messages and to greet the customer normally if they only say hello. A staff member can approve or reject a waiting request after the chat ends.

On my computer, Ollama runs in Ubuntu through WSL. I run the live demos from the project folder in Ubuntu with `~/.venvs/ism3232-week12/bin/python main.py` for Sunny and `~/.venvs/ism3232-week12/bin/python my_main.py` for Bean.
