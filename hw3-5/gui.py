import socket

from PyQt6.QtWidgets import QApplication
import sys

from window import Window

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ("127.0.0.1", 9000)
    sock.connect(address)
    app = QApplication(sys.argv)
    window = Window(sock)
    app.exec()
