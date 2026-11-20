import socket
import sqlite3
print(sqlite3.sqlite_version)
from queue import Queue
from threading import Thread

from clienthandler import ClientHandler
from dispatcher import Dispatcher
from room_repository import RoomRepository

print("Started")

class Server(Thread):
    def __init__(self):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("127.0.0.1", 8000))
        self.sock.listen()
        self.incoming_queue = Queue()
        self.room_repository = RoomRepository()
        self.dispatcher = Dispatcher(self.incoming_queue,self.room_repository)

    def run(self):
        while True:
            conn, addr = self.sock.accept()
            client = ClientHandler(conn,self.incoming_queue)
            self.dispatcher.add(client)

server = Server()
server.start()
