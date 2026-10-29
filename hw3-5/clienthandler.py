import datetime
import socket
from queue import Queue
from threading import Thread

from communication import Communication
from message import Message


class ClientHandler:
    def __init__(self, sock: socket.socket, incoming_queue: Queue,store):
        super().__init__()
        self.username: str | None = None
        self.communication = Communication(sock)
        self.store = store
        self.incoming_queue: Queue[Message] = incoming_queue
        self.outcoming_queue: Queue[Message] = Queue()

        self.welcome_thread = Thread(target=self.welcome, daemon=True)
        self.writer_thread = Thread(target=self.write, daemon=True)
        self.reader_thread = Thread(target=self.read, daemon=True)

        # take the username
        self.welcome_thread.start()
        self.welcome_thread.join()

        if self.username:
            self.writer_thread.start()
            self.reader_thread.start()

    def get_history(self):
        recent = self.store.last_five()
        self.communication.send(recent)
    def welcome(self):
        while True:
            self.communication.send("Write your username here")
            msg: str | None = self.communication.recv()
            if msg is None:
                break
            msg = msg.strip()
            if len(msg) < 3:
                continue
            self.username = msg
            self.get_history()
            return

    def write(self):
        while True:
            message: Message = self.outcoming_queue.get()
            text: str = f"{message.username} [{message.date.strftime('%d.%m %H:%M:%S')}]: {message.text}"
            self.communication.send(text)

    def read(self):
        while True:
            text: str | None = self.communication.recv()
            if text is None:
                break
            command, *body = text.split(" ", maxsplit=1)
            if not body:
                continue
            destination = None
            match command:
                case "/private":
                    destination, msg = body[0].split(" ", maxsplit=1)
                case "/all":
                    msg = body[0]
                case "/game":
                    msg = body[0]
                case _:
                    msg = "?????"

            message = Message(
                type=command,
                username=self.username,
                date=datetime.datetime.now(),
                text=msg,
                destination_username=destination
            )
            self.incoming_queue.put(message)


