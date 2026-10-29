from collections import deque


class MessageStore:
    def __init__(self):
        self.message_history = deque(maxlen=20)
    def add_message(self,message):
        msg = f"{message.username} [{message.date.strftime('%d.%m %H:%M:%S')}]: {message.text}"
        if len(self.message_history) < 20:
            self.message_history.append(msg)
    def last_five(self):
        recent = "\n".join( list(self.message_history)[-5:]) + "\n"
        return recent

