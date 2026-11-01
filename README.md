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

The class code was generated with AI assistance. Each executable class line has
a comment explaining what it does and why; `AI_DISCLOSURE.md` preserves the generated
classes. Read and understand each line before submitting, as required by the lab.

From the repository root, commit with a message containing `lab 10`, push to your
public GitHub repository, and paste that repository URL into Canvas.
