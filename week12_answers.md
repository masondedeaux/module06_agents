# Week 12 answers

## Exercise 1

1. The customer typed:
   - I want to change my shipping address
   - It's order A102
   - 9 Pine Street, Tampa
2. Two tool requests were refused. The first used an order ID the customer hadn't given. The second used a new address the customer hadn't given.
3. Ollama receives 14 messages: one system message, four customer messages including "thanks," three assistant replies, and six messages representing the three tool requests and their results.
4. "Do you sell gift cards?" goes to a person because the handoff rule finds `card` inside `cards`. That's acceptable because staff can answer the gift card question, and the same rule sends sensitive card questions to staff.

## Exercise 3

I temporarily bypassed `customer_said` for this run. Sunny queued a request using details I had not supplied. I rejected it at review. The guardrail was restored after the run.

```text
Type a message, or type quit to stop.
You: I want to change my shipping address
Sunny: Your request to change the shipping address for order A100 has been submitted and will need staff approval before it can be updated.
You: quit
Messages in this conversation: 3
Staff review
Request 1: A100 to 123 Main St, Anytown, AN 12345
Approve? yes or no: no
Request 1 rejected.
A100 14 Bay Road
A101 3 Gull Lane
A102 88 Pier Street
```
