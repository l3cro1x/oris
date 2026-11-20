from threading import Thread


class Dispatcher(Thread):
    def __init__(self, incoming_queue, rooms):
        super().__init__()
        self.incoming_queue = incoming_queue
        self.rooms = rooms
        self.clients = dict()
        self.start()

    def add(self, client):
        self.clients[client.id] = client
        print(client.id)

    def run(self):
        while True:
            msg = self.incoming_queue.get()
            print("dispatcher: " + f"{msg.sender_name}")
            match msg.type:
                case ("DIRECT"):
                    sender_id = msg.sender_id
                    recipient_id = msg.recipient
                    recipient = self.clients[recipient_id]
                    sender =  self.clients[sender_id]
                    recipient.outcoming_queue.put(msg)
                    sender.outcoming_queue.put(msg)
                case ("GROUP"):
                    room = self.rooms[msg.room]
                    for client in room:
                        client.outcoming_queue.put(msg)
                case ("CREATE"):
                    pass
                case ("SEARCH"):
                    query = msg.text
                    result = []
                    for client in self.clients.values():
                        if query.lower() in client.name.lower():
                            result.append(f'{client.id},{client.name}')
                    recipient = self.clients[msg.sender_id]
                    recipient.outcoming_queue.put(result)
                    print(result)
