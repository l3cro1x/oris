import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

address = ('127.0.0.1', 8000)
sock.connect(address)
print("Connected")


while True:
	msg: str = (input("Enter the guess: "))
	if msg == "quit":
		break
	data: bytes = msg.encode("utf-8")

	print('sending data...')
	sock.sendall(data)

	print('answer is...')
	data: bytes = sock.recv(5120)
	result: str = data.decode("utf-8")
	print(result)

sock.close()
