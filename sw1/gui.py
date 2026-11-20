import socket

from PyQt5.QtWidgets import QApplication
import sys

from window import Window


def app():
    app = QApplication(sys.argv)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 8000))
    window = Window(sock)
    sys.exit(app.exec())
if __name__=="__main__":
    app()
