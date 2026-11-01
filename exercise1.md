# Exercise 1

1. The two original classes are `OrderLookup` and `SupportChatbot`.
2. One object of each class in `main.py`: `order_tool` and `bot`.
3. The four original attributes of `SupportChatbot` are `name`, `instructions`,
   `order_tool`, and `history`. Exercise 3 adds `stock_tool` as a fifth attribute.
4. Every method of `OrderLookup`: `__init__`, `find_order_id`, and `find_status`.
5. The composition line in `chatbot.py` is `self.order_tool = order_tool`.
   Exercise 3 adds another example: `self.stock_tool = stock_tool`.
6. In `bot.respond("hello")`, `self` is the object named `bot`.
