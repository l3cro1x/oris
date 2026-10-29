import time
from threading import Thread


class GameEngine:
    def __init__(self, incoming_queue, state):
        self.state = state
        self.incoming_queue = incoming_queue
        self.pause_until = None

        self.logic = Thread(target=self.gameLogic)
        self.logic.start()

    def handle_action(self, data):
        if data["action"] == "key":
            if not (player := self.state.get_player(data["player_id"])):
                return None

            match data["key"]:
                case "W":
                    if player.y > 0:
                        player.move_up()
                case "S":
                    if player.y < 190:
                        player.move_down()

            self.incoming_queue.put({
                "type": "state",
                "data": self.state.to_dict()
            })

    def gameLogic(self):
        while True:
            if self.state.state != "ready":
                time.sleep(0.1)
                continue

            if self.pause_until is not None:
                if time.monotonic() < self.pause_until:
                    time.sleep(0.05)
                    continue

                self.pause_until = None

            time.sleep(0.13)

            ball = self.state.ball
            player1 = self.state.player1
            player2 = self.state.player2

            ball.check(player1, player2)

            if ball.x + 10 < 0:
                ball.reset(2)
                self.state.goal(player2)
                self.pause_until = time.monotonic() + 3

                self.incoming_queue.put({
                    "type": "goal",
                    "data": self.state.start_pos()
                })
                continue

            elif ball.x > 400:
                ball.reset(1)
                self.state.goal(player1)
                self.pause_until = time.monotonic() + 3

                self.incoming_queue.put({
                    "type": "goal",
                    "data": self.state.start_pos()
                })
                continue

            self.incoming_queue.put({
                "type": "state",
                "data": self.state.to_dict()
            })
