from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians, degrees, asin
from random import random, randrange, uniform
from path import Path


class Target(object):

    def __init__(self, world):
        self.world = world
        self.vel = Vector2D(0,0)
        self.accel = Vector2D(0,0)
        self.pos = Vector2D(self.world.cx / 2, self.world.cy / 2)

    def render(self):
        egi.red_pen()
        egi.cross(self.pos, 10)
