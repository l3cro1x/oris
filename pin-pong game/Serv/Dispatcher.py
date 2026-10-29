from queue import Empty
from threading import Thread

from Game.GameEngine import GameEngine


class Dispatcher:
    def __init__(self, incoming_queue, engine: GameEngine):
        self.incoming_queue = incoming_queue
        self.handlers = []
        self.engine = engine
        self.thread = Thread(target=self.dispatch)
        self.thread.start()

    def dispatch(self):
        while True:
            data = self.incoming_queue.get()
            action_type = data["type"]

            print("DISPATCHER GOT:", data)

            if action_type == "state":
                game_state = data["data"]

                for handler in self.handlers:
                    handler.outcoming_queue.put({
                        "type": "state",
                        "data": game_state
                    })

            elif action_type == "action":
                self.engine.handle_action(data["data"])

            elif action_type == "goal":
                game_state = data["data"]

                for handler in self.handlers:
                    handler.outcoming_queue.put({
                        "type": "goal",
                        "data": game_state
                    })

            elif action_type == "disconnect":
                player_id = data["data"]["player_id"]

                handler = next(
                    (h for h in self.handlers if h.player_id == player_id),
                    None
                )

                if handler is not None:
                    self.handlers.remove(handler)

                self.engine.state.remove_player(player_id)

                for handler in self.handlers:
                    handler.outcoming_queue.put({
                        "type": "disconnect",
                        "data": {"player_id": player_id}
                    })
    def add_handler(self, handler):
        print("ADDED :",handler)
        self.handlers.append(handler)
