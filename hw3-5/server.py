import socket
from clienthandler import ClientHandler
from dispatcher import Dispatcher
from store import MessageStore
from wordle import Wordle


class Server:
	def __init__(self, host: str, port: int):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

		address: tuple[str, int] = (host, port)
		self.sock.bind(address)
		self.sock.listen()
		self.game = Wordle()
		self.store = MessageStore()
		self.dispatcher = Dispatcher(self.store,self.game)
		self.dispatcher.start()
		print(f"started listening on {address}")



	def serve(self):
		while True:
			print(f"waiting for client to connect...")
			client_sock, client_addr = self.sock.accept()

			print(f"connected from: {client_addr}")
			client_thread = ClientHandler(
				sock=client_sock,
				incoming_queue=self.dispatcher.incoming_queue,
				store=self.store
			)
			self.dispatcher.add(client_thread)
		# end while loop
		self.sock.close()

server = Server("127.0.0.1", 9000)
server.serve()
