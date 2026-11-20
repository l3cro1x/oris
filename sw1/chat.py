class Chat:
    def __init__(self,name,id):
        self.name = name
        self.id = id
        self.members = set()
    def add_member(self,member):
        self.members.add(member)