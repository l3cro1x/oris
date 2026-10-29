import socket
from queue import Queue
from threading import Thread

from Game.GameEngine import GameEngine
from Game.GameState import GameState
from Props.Ball import Ball
from Props.Player import Player
from Serv.Dispatcher import Dispatcher
from Network.ClientHandler import ClientHandler


class Server:

    def __init__(self, addr, port):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((addr, port))
        self.sock.listen()
        self.state = GameState()
        self.incoming_queue = Queue()
        self.engine = GameEngine(self.incoming_queue,self.state)
        self.dispatcher = Dispatcher(self.incoming_queue, self.engine)

    def serve(self):
        while True:
            client, addr = self.sock.accept()

            player_id = self.state.get_free_player_id()

            if player_id is None:
                client.close()
                continue

            handler = ClientHandler(
                client=client,
                incoming_queue=self.incoming_queue,
                player_id=player_id
            )

            x = 15 if player_id == 0 else 375
            player = Player(id=player_id, x=x, y=95)

            self.state.add_player(player)
            self.dispatcher.add_handler(handler)

            handler.start()


server = Server("127.0.0.1", 8000)
server.serve()

