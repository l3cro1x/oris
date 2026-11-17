import socket
import struct


class Client:
	def __init__(self,addr,port):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		address = (addr,port)
		self.sock.connect(address)
	def recvdata(self, sock: socket.socket,length:int) -> bytes:
		data_bytes: bytes = bytearray()
		while length > len(data_bytes):
			if not (package:=sock.recv(length - len(data_bytes))):
				break
			data_bytes += package
		return data_bytes
	def senddata(self, sock: socket.socket, text: str):
		text_bytes = text.encode("utf-8")
		header = struct.pack("!I",len(text_bytes))
		sock.sendall(header + text_bytes)
	def recvall(self,sock:socket.socket) -> str|None:
		data = self.recvdata(sock,4)
		if len(data) < 4:
			return None
		header = struct.unpack("!I",data)[0]
		msg_bytes = self.recvdata(sock,header)
		if len(msg_bytes) < header:
			return None
		return msg_bytes.decode('utf-8')
	def action(self):
		print("Connected")
		while True:
			msg: str = input("Enter the command: ")
			self.senddata(self.sock,msg)
			data = self.recvall(self.sock)
			print(data)
			if msg == "/quit":
				break
		self.sock.close()

client = Client('127.0.0.1', 8001)
client.action()



