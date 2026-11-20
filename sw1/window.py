from queue import Queue

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QDialog, QFrame, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt5.uic import loadUi

from communication import Communication


class SocketRecv(QThread):
    signal = pyqtSignal(str)

    def __init__(self, comm):
        super().__init__()
        self.comm = comm

    def run(self):
        while True:
            msg = self.comm.recvall()
            self.signal.emit(msg)


class SocketSend(QThread):
    def __init__(self, comm):
        super().__init__()
        self.comm = comm
        self.outcoming_queue = Queue()

    def run(self):
        while True:
            msg = self.outcoming_queue.get()
            self.comm.send(msg)


class Settings(QDialog):
    def __init__(self, queue):
        super().__init__()
        loadUi("settings.ui", self)
        self.queue = queue
        self.setWindowTitle(" ")
        self.setFixedSize(300, 500)
        self.nameInput.setPlaceholderText("Enter your nickname")
        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.save_settings)
        self.buttonBox.rejected.connect(self.reject)

    def save_settings(self):
        nickname = self.nameInput.text()
        self.queue.put("/setnickname " + nickname)
        self.nameInput.clear()
        super().accept()

class Creating(QDialog):
    def __init__(self, queue):
        super().__init__()
        loadUi("creating.ui", self)
        self.queue = queue
        self.setWindowTitle(" ")
        self.setFixedSize(300, 500)
        self.nameInput.setPlaceholderText("Enter name of your group")
        self.buttonBox.accepted.connect(self.create)
        self.buttonBox.rejected.connect(self.reject)

    def create(self):
        group_name = self.nameInput.text()
        self.queue.put("/create " + group_name)
        self.nameInput.clear()
        super().accept()

class Search(QWidget):
    selected_chat = pyqtSignal(str,str)
    def __init__(self, searchBar, outcoming_queue):
        super().__init__()
        self.searchBar = searchBar
        self.queue = outcoming_queue
        self.searchResult = QListWidget()
        self.searchResult.setFixedSize(300, 500)
        self.searchBar.textChanged.connect(self.search)

    def search(self):
        query = self.searchBar.text().strip()
        if not query:
            self.searchResult.hide()
            return
        self.searchResult.show()
        self.queue.put("/search " + query)




class Window(QWidget):
    def __init__(self, sock):
        super().__init__()
        self.current_chat = None
        self.comm = Communication(sock)
        self.sender = SocketSend(self.comm)
        self.receiver = SocketRecv(self.comm)
        self.ui()
        self.settings = Settings(self.sender.outcoming_queue)
        self.creating = Creating(self.sender.outcoming_queue)
        self.sender.start()
        self.receiver.start()
        self.search = Search(self.searchBar, self.sender.outcoming_queue)
        self.searchResult = self.search.searchResult
        self.searchResult.itemActivated.connect(self.open_chat)

        self.show()

    def ui(self):
        loadUi("markup.ui", self)
        width, height = 1200, 800
        self.setWindowTitle("Messenger")
        self.setFixedSize(width, height)
        self.settingsButton.setIcon(QIcon("icon.png"))
        self.settingsButton.setIconSize(QSize(20, 20))
        self.settingsButton_2.setIcon(QIcon("icon2.png"))
        self.settingsButton_2.setIconSize(QSize(20, 20))
        self.settingsButton.clicked.connect(self.settingsWindow)
        self.settingsButton_2.clicked.connect(self.creatingWindow)
        self.sendButton.clicked.connect(self.on_click_send)
        self.receiver.signal.connect(self.msg_received)
        self.receiver.signal.connect(self.handle_result)

    def on_click_send(self):
        text = self.textInput.toPlainText()
        self.sender.outcoming_queue.put("/direct " + text + " " +self.current_chat)
        self.textInput.clear()

    @pyqtSlot(str)
    def msg_received(self, text):
        if text.startswith("/r "):
            return
        return self.textEdit.append(text)

    def settingsWindow(self):
        self.settings.exec()
    def creatingWindow(self):
        self.creating.exec()
    def open_chat(self,item):
        user_id = item.data(Qt.UserRole)
        username = item.text()
        self.current_chat = user_id
        self.chatInfo.setText(username)
        self.searchResult.itemActivated.connect(self.searchResult.close)
        self.search.searchBar.clear()
    @pyqtSlot(str)
    def handle_result(self, result):
        if not result.startswith("/r "):
            return

        users = result[3:].split("\n")
        self.search.searchResult.clear()

        for user in users:
            user_id, username = user.split(",", 1)

            item = QListWidgetItem(username)
            item.setData(Qt.UserRole, user_id)

            self.search.searchResult.addItem(item)
