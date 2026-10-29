import socket
from threading import Thread
from PyQt6.QtCore import QObject, pyqtSignal
from Utils.Communication import Communication


class Client(QObject):
    signal = pyqtSignal(dict)
    def __init__(self, addr, port):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((addr, port))

        self.comm = Communication(self.sock)

        self.receive_thread = Thread(target=self.receive_loop)
        self.receive_thread.start()

    def receive_loop(self):
        while True:
            state = self.comm.recv_all()
            self.signal.emit(state)


