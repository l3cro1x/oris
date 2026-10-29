import time

from Props.Ball import Ball


class GameState:
    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.scores = [0,0]
        self.ball = Ball(195, 120)
        self.state = "waiting"

    def add_player(self, player):
        if self.player1 is None:
            self.player1 = player
            self.scores[0] = 0
        elif self.player2 is None:
            self.player2 = player
            self.scores[1] = 0
            self.state = "ready"
        else:
            return False
        return True

    def get_free_player_id(self):
        if self.player1 is None:
            return 0
        if self.player2 is None:
            return 1
        return None
    def remove_player(self, player_id):
        if self.player1 is not None and self.player1.id == player_id:
            self.player1 = None
        elif self.player2 is not None and self.player2.id == player_id:
            self.player2 = None
        else:
            return

        self.state = "waiting"
        self.ball.reset()

    def goal(self, player):
        match player.id :
            case 0:
                self.scores[0] += 1
            case 1:
                self.scores[1] += 1
        self.ball.check(self.player1,self.player2)
    def is_ready(self):
        return self.state == "ready"

    def get_player(self, id):
        if self.player1 is not None and self.player1.id == id:
            return self.player1

        if self.player2 is not None and self.player2.id == id:
            return self.player2

        return None
    def start_pos(self):
        return {
            "players": [
                {
                    "id": 0,
                    "x": 15,
                    "y": 95
                },
                {
                    "id": 1,
                    "x": 375,
                    "y": 95

                }

            ],
            "ball": {
                "x": self.ball.x,
                "y": self.ball.y,
                "vx": self.ball.vx,
                "vy": self.ball.vy
            }
        }
    def to_dict(self):
        return {
            "players": [
                {
                    "id": player.id,
                    "x": player.x,
                    "y": player.y
                }
                for player in (self.player1, self.player2)
                if player is not None
            ],
            "ball": {
                "x": self.ball.x,
                "y": self.ball.y,
                "vx":self.ball.vx,
                "vy":self.ball.vy
            }
        }
