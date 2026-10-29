import sys
from PyQt6.QtWidgets import QApplication

from Network.Client import Client
from App.Window import Window


app = QApplication(sys.argv)

client = Client("127.0.0.1", 8000)

window = Window(client)
client.signal.connect(window.update_state)
window.show()

sys.exit(app.exec())