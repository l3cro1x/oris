import datetime
from queue import Queue
from threading import Thread

from communication import Communication
from message import Message


class ClientHandler:
    counter = 0

    def __init__(self, conn, incoming_queue):
        self.id = ClientHandler.counter
        self.name = f"user_{self.id}"
        ClientHandler.counter += 1
        self.sock = conn
        self.comm = Communication(self.sock)
        self.outcoming_queue = Queue()
        self.incoming_queue = incoming_queue
        w = Thread(target=self.writer)
        r = Thread(target=self.reader)
        w.start()
        r.start()

    def writer(self):
        while True:
            msg = self.outcoming_queue.get()
            if not isinstance(msg,list):
                output = f"{msg.sender_name} " + f"[{msg.time}]: " + msg.text
                self.comm.send(output)
            else:
                output = "\n".join(msg)
                self.comm.send("/r " + output)

    def reader(self):
        while True:
            message = self.comm.recvall().strip()
            parts = message.split(" ")
            command = parts[0]

            match command:
                case "/direct":
                    recipient = parts[-1]
                    text = " ".join(parts[1:-1])
                    msg = Message(
                        type="DIRECT",
                        sender_id=self.id,
                        sender_name=self.name,
                        recipient=int(recipient),
                        text=text,
                        time=datetime.datetime.now(),
                        room=None
                    )
                    self.incoming_queue.put(msg)

                case "/group":
                    recipient = parts[-1]
                    text = " ".join(parts[1:-1])
                    msg = Message(
                        type="GROUP",
                        sender_id=self.id,
                        sender_name=self.name,
                        recipient=self.id,
                        text=text,
                        time=datetime.datetime.now(),
                        room=recipient
                    )
                    self.incoming_queue.put(msg)
                case "/setnickname":
                    self.name = " ".join(parts[1:])
                case "/create":
                    groupname = " ".join(parts[1:])
                    msg = Message(
                        type="CREATE",
                        sender_id=self.id,
                        sender_name=self.name,
                        recipient=None,
                        text=groupname,
                        time=datetime.datetime.now(),
                        room=None
                    )
                    self.incoming_queue.put(msg)
                case "/search":
                    msg = Message(
                        type="SEARCH",
                        sender_id=self.id,
                        sender_name=self.name,
                        recipient=None,
                        text=" ".join(parts[1:]),
                        time=datetime.datetime.now(),
                        room=None
                    )
                    self.incoming_queue.put(msg)



