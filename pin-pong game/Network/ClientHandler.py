from queue import Queue
from threading import Thread
from Utils.Communication import Communication


# {action:ready/move,dir:up/down,player_id:...}
class ClientHandler(Thread):
    def __init__(self, client, incoming_queue, player_id):
        super().__init__()
        self.player_id = player_id
        self.comm = Communication(client)

        self.client = client
        self.incoming_queue = incoming_queue
        self.outcoming_queue = Queue()
        self.send_thread = Thread(target=self.process)
        self.send_thread.start()

    def run(self):
        try :

            print("RUN STARTED")
            while True:
                print("WAITING FOR DATA")

                action = self.comm.recv_all()

                if action is None:
                    break

                print("RECEIVED:", action)

                package = {
                    "action": "key",
                    "key": action,
                    "player_id": self.player_id
                }

                self.incoming_queue.put({"type":"action","data" : package})
        finally:
            self.incoming_queue.put({
                "type": "disconnect",
                "data": {"player_id": self.player_id}
            })
            self.client.close()

    def process(self):
        while True:
            data = self.outcoming_queue.get()
            self.comm.send(data)
