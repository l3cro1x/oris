from queue import Queue

from PyQt6.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton

from communication import Communication


class SocketRecv(QThread):
    signal = pyqtSignal(str)

    def __init__(self, comm):
        super().__init__()
        self.comm = comm

    def run(self):
        while True:
            text = self.comm.recv()
            self.signal.emit(text)


class SocketSend(QThread):
    def __init__(self, comm):
        super().__init__()
        self.comm = comm
        self.outcoming_queue = Queue()

    def run(self):
        while True:
            msg = self.outcoming_queue.get()
            self.comm.send(msg)


class Window(QWidget):

    def __init__(self, sock):
        super().__init__()
        self.comm = Communication(sock)
        self.user_interface()
        self.sender = SocketSend(self.comm)
        self.receiver = SocketRecv(self.comm)
        self.receiver.signal.connect(self.msg_received)
        self.sender.start()
        self.receiver.start()

        self.show()

    def user_interface(self):
        self.setFixedSize(400, 400)
        central = QVBoxLayout(self)
        self.output_text = QTextEdit()
        self.input_text = QLineEdit()
        self.btn = QPushButton("Send")
        self.btn.clicked.connect(self.on_click_send)
        central.addWidget(self.output_text)
        central.addWidget(self.input_text)
        central.addWidget(self.btn)
    def on_click_send(self):
        text = self.input_text.text()
        self.sender.outcoming_queue.put(text)
        self.input_text.clear()
    @pyqtSlot(str)
    def msg_received(self,text):
        self.output_text.append(text)
