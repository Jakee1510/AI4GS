
from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange, uniform
from path import Path


class Obstacle(object):

    def __init__(self, world=None, post=Vector2D(0, 0)):

        self.world = world
        self.radius = 30
        self.pos = post


    def render(self):
        egi.blue_pen()
        egi.circle(self.pos, self.radius,  True)


