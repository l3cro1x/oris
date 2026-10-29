class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 10
        self.vy = 10
    def update(self,direction=None):
        if direction == "vert":
            self.vy = -self.vy
        elif direction=="horiz":
            self.vx = -self.vx
        else:
            self.x += self.vx
            self.y += self.vy
    def reset(self,side):
        self.x = 195
        self.y = 120
        if side == 1:
            self.vx = -10
            self.vy = -10
        if side == 2:
            self.vx = 10
            self.vy = 10
    def get_pos(self):
        return (self.x, self.y)
    def check(self,pl1,pl2):
        if self.y < 0 or self.y + 10 > 250:
            if self.y < 0:
                self.y = 0
            if self.y +10 > 250:
                self.y = 240
            self.update("vert")
        elif not((pl1.y+ 60 < self.y ) or (pl1.y > self.y + 10)) and self.x-5 < pl1.x +10 and self.vx < 0:
            self.x = pl1.x + 10
            self.update("horiz")
        elif not((pl2.y+ 60 < self.y ) or (pl2.y > self.y+ 10)) and self.x + 5 > pl2.x -10 and self.vx > 0:
            self.x = pl2.x - 10
            self.update("horiz")
        else:
            self.update()