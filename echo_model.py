# echo_model.py
# Author: Mason Dedeaux

class EchoModel:
    def reply(self, instructions, history):
        return "You said: " + history[-1]["content"]