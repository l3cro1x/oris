from chat import Chat


class RoomRepository:
    def __init__(self):
        self.rooms = dict()
    def add_room(self,room):
        self.rooms[room.name] = room
    def create_room(self,name,password):
        room = Chat(name,password)
        self.add_room(room)
