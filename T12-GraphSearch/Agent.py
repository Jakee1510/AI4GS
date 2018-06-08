from graphics import egi
from point2d import Point2D




class Agent(object):
    def __init__(self, x, y, boxes):

        self.pos = Point2D(x, y)
        self.boxes = boxes
        self.path = []
        self.finished = False

    def update(self):
        if len(self.path) > 0:
            src = self.pos
            dest = self.boxes[self.path[0]]._vc

            scale = 0.85
            self.pos.x = (src.x + (dest.x - src.x) * scale)
            self.pos.y = (src.y + (dest.y - src.y) * scale)

            if self.pos.x == dest.x and self.pos.y == dest.y:
                self.path = self.path[1:]

            if len(self.path) == 0:
                self.finished = True


    def render(self):
        egi.blue_pen()
        egi.circle(self.pos, 15)

