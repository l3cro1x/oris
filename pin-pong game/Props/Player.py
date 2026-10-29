class Player:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.speed = 5
    def update(self, x, y):
        self.x = x
        self.y = y
    def move_up(self):
        self.y -= self.speed
    def move_down(self):
        self.y += self.speed
    def get_pos(self):
        return (self.x, self.y)
