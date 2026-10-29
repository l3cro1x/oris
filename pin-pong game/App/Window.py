from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QWidget

from Utils.Communication import Communication
from PyQt6.QtCore import QObject


class Window(QWidget):
    def __init__(self, client):
        super().__init__()
        self.comm = Communication(client.sock)
        self.SCREEN_WIDTH = 400
        self.SCREEN_HEIGHT = 250
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)

        self.setFixedSize(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.setWindowTitle("Ping-Pong")
        self.goal = False
        self.countdown = 0
        self.player1 = (15, 95, 10, 60)
        self.player2 = (375, 95, 10, 60)
        self.ball = (195, 120, 10, 10)

    def tick(self):
        if self.countdown == 0:
            self.goal = False
            self.timer.stop()
            return
        self.countdown -= 1
        self.update()

    def update_state(self, data):
        type = data["type"]
        game_state = data["data"]
        players,ball = game_state.values()

        if type == "goal":
            self.countdown = 3
            self.goal = True
            self.timer.start(1000)
        if type == "disconnect":
            self.goal = False
            self.timer.stop()
            self.update()
            return
        if type == "state":
            for player in players:
                id = player["id"]
                x = player["x"]
                y = player["y"]
                if id == 0:
                    self.player1 = (x, y, self.player1[2], self.player1[3])
                if id == 1:
                    self.player2 = (x, y, self.player2[2], self.player2[3])
        self.ball = (ball['x'], ball['y'], self.ball[2], self.ball[3])
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.goal:

            painter.drawText(
                self.rect(),
                Qt.AlignmentFlag.AlignCenter,
                str(self.countdown)
            )
        painter.setBrush(Qt.BrushStyle.SolidPattern)
        painter.drawRect(*self.player1)
        painter.drawRect(*self.player2)
        painter.drawEllipse(*self.ball)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_W:
            print("Отправляю:", "W")
            self.comm.send("W")

        elif event.key() == Qt.Key.Key_S:
            print("Отправляю:", "S")
            self.comm.send("S")
