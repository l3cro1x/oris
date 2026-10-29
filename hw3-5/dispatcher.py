import datetime
from copy import deepcopy
from queue import Queue
from threading import Thread

from message import Message
from clienthandler import ClientHandler
from store import MessageStore
from wordle import Wordle


class Dispatcher(Thread):
    msgstore: MessageStore
    client_handlers: list[ClientHandler]
    incoming_queue: Queue[Message]
    client_handler_map: dict[str, ClientHandler]
    game : Wordle
    def __init__(self,msgstore,game):
        super().__init__()
        self.msgstore = msgstore
        self.game = game
        self.client_handlers = []
        self.incoming_queue = Queue()
        self.client_handler_map = {}

    def send_to_all(self, msg: Message):
        for client_handler in self.client_handlers:  # type: ClientHandler
            if msg.username == client_handler.username:
                msg_copy = deepcopy(msg)
                msg_copy.username = "you"
                client_handler.outcoming_queue.put(msg_copy)
                self.msgstore.add_message(msg)
            else:
                client_handler.outcoming_queue.put(msg)

    def send_to(self, msg: Message):
        if not msg.destination_username:
            return

        for client_handler in self.client_handlers:
            if msg.destination_username == client_handler.username:
                client_handler.outcoming_queue.put(msg)
                self.msgstore.add_message(msg)
                break
    def start_wordle(self):
        self.game = Wordle()
        msg_new_game = Message(
            type="all",
            username="WORDLE GAME",
            date=datetime.datetime.now(),
            text="New game!: " + self.game.current(),
            destination_username=None
        )
        for client_handler in self.client_handlers:
            client_handler.outcoming_queue.put(msg_new_game)
    def wordle(self,msg):
        if not self.game.state == "over":
            is_guessed = self.game.check(msg.text)
            msg_copy = deepcopy(msg)
            msg_copy.username = "WORDLE GAME"
            msg_copy.text = self.game.current()
            for client_handler in self.client_handlers:  # type: ClientHandler
                client_handler.outcoming_queue.put(msg_copy)
            if is_guessed:
                for client_handler in self.client_handlers:  # type: ClientHandler
                    msg = Message(
                        type="all",
                        username="WORDLE GAME",
                        date=datetime.datetime.now(),
                        text="Word is guessed",
                        destination_username=None
                    )
                    client_handler.outcoming_queue.put(msg)




    def change_room(self, msg: Message):
        pass

    def run(self):
        while True:
            print(self.game.word)
            print(self.game.current())
            msg: Message = self.incoming_queue.get()

            match msg.type:
                case "/private":
                    self.send_to(msg)
                case "/all":
                    self.send_to_all(msg)
                case "/room":
                    self.change_room(msg)
                case "/game":
                    if msg.text != "start":
                        self.wordle(msg)
                    if msg.text == "start":
                        self.start_wordle()

                case _:
                    print("unknown message:", msg)

    def add(self, handler: ClientHandler):
        self.client_handlers.append(handler)
