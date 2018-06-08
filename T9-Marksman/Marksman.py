from vector2d import Vector2D
from graphics import egi, KEY
from Bullet import Bullet

class Marksman(object):

    def __init__(self, world=None):

        self.world = world
        self.pos = Vector2D(world.cx / 5, world.cy / 2)
        self.bullet = []
        self.target = self.world.hitpoint

        self.modespeed = 1
        self.predictedtarget = Vector2D()


    def update(self, delta):

        self.predictedtarget = self.target.pos + (self.target.vel / self.modespeed * 30) + (self.target.accel) * delta

    def render(self):
        egi.red_pen()
        egi.circle(self.pos, 10, True)

        egi.white_pen()
        #egi.line_by_pos(self.pos, self.world.hitpoint.pos)


    def shoot(self):

        self.world.bullet.append(Bullet(self.world ,self.predictedtarget, self.pos.copy(), self.mode))

