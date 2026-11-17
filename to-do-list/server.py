import socket
import struct
from task import Task
class Server:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

        address = (host, port)
        self.sock.bind(address)
        self.sock.listen()
        self.tasks = []
        print(f"started listening on {address}")
    def recvdata(self, sock: socket.socket, length: int) -> bytes:
        data_bytes: bytes = bytearray()
        while length > len(data_bytes):
            if not (package := sock.recv(length - len(data_bytes))):
                break
            data_bytes += package
        return data_bytes
    def senddata(self, sock: socket.socket, text: str):
        text_bytes = text.encode("utf-8")
        header = struct.pack("!I", len(text_bytes))
        sock.sendall(header + text_bytes)
    def recvall(self, sock: socket.socket) -> str | None:
        data = self.recvdata(sock, 4)
        if len(data) < 4:
            return None
        header = struct.unpack("!I", data)[0]
        msg_bytes = self.recvdata(sock, header)
        if len(msg_bytes) < header:
            return None
        return msg_bytes.decode('utf-8')
    def splitter(self, message: str) -> tuple[str | None, str | None, str | None]:
        if not message.startswith('/'):
            return None, None, None
        parts = message.split(' ', 2)
        if len(parts) == 3:
            return parts[0], parts[1], parts[2]
        elif len(parts) == 2:
            return parts[0], None, parts[1]
        elif len(parts) == 1:
            return parts[0], None, None
        return None, None, None
    def get_tasks(self, sock):
        if self.tasks:
            texts = "\n".join([f"{task.task_text()} (Until: {task.left()})" for task in self.tasks])
            self.senddata(sock, texts)
        else:
            self.senddata(sock, "no tasks")
    def add_task(self, task: Task):
        self.tasks.append(task)
    def del_task(self, text):
        for task in self.tasks:
            if task.task_text() == text:
                self.tasks.remove(task)
                return True
        return False
    def exit_from(self, sock):
        sock.close()
    def serve(self):
        print(f"waiting for client to connect...")
        client_sock, client_addr = self.sock.accept()
        print(f"connected from: {client_addr}")
        while True:
            message: str | None = self.recvall(client_sock)
            if not message:
                break
            command, deadline, text = self.splitter(message)
            match command:
                case '/add':
                    if text:
                        task = Task(text, deadline)
                        self.add_task(task)
                        if deadline and not task.deadline_dt:
                            self.senddata(client_sock, "task added, but deadline format invalid (use DD.MM.YYYY_HH:MM)")
                        else:
                            self.senddata(client_sock, "task was added")
                    else:
                        self.senddata(client_sock, "error: missing task text")

                case '/remove':
                    if text and self.del_task(text):
                        self.senddata(client_sock, "task was deleted")
                    else:
                        self.senddata(client_sock, "task not found")

                case '/list':
                    self.get_tasks(client_sock)
                case "/quit":
                    self.senddata(client_sock, "exit done")
                    self.exit_from(client_sock)
                    break
                case _:
                    self.senddata(client_sock, "wtf is that")

        self.sock.close()


if __name__ == "__main__":
    server = Server('127.0.0.1', 8001)
    server.serve()
