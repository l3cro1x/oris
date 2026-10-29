import socket
import struct


class Communication:
	def __init__(self, sock: socket.socket):
		self.sock = sock

	def send(self, message: str):
		message_bytes: bytes = message.encode("utf-8")
		header: bytes = struct.pack('!I', len(message_bytes))  # create a header (4 bytes)
		self.sock.sendall(header + message_bytes)  # send header and message

	def recv(self) -> str | None:
		header = self.recv_all(nbytes=4)  # read header (4 bytes)
		if not header:
			self.sock.close()
			return None
		message_len = struct.unpack('!I', header)[0]  # unpack header
		message_bytes = self.recv_all(nbytes=message_len)  # read N-bytes
		if not message_bytes:
			self.sock.close()
			return None
		return message_bytes.decode("utf-8")

	def recv_all(self, nbytes):
		data = bytearray()
		while len(data) < nbytes:
			if not (packet := self.sock.recv(nbytes - len(data))):
				break
			data += packet
		return data

	def close(self):
		self.sock.close()
