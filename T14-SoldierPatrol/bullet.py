from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians, degrees, asin
from random import random, randrange, uniform
from path import Path


class Bullet(object):


    def __init__(self,world=None, target=None, marksman=None, mode = 'rifle'):
        self.world = world

        self.pos = marksman
        self.targ = target

        self.dir = (self.targ - self.pos).normalise()

        self.mode = mode
        self.speed = 1

        if self.mode == 'rifle':
            self.speed = 30*30

        elif self.mode == 'rocket':
            self.speed = 5 * 30

        elif self.mode == 'handgun':
            self.speed = 30 * 30

        elif self.mode == 'hand_grenade':
            self.speed = 30 * 30
        else:
            self.speed = 0.0


        self.vel = self.dir * self.speed

        self.visible = True


    def update(self,delta):
        self.checkcollision()
        self.pos += self.vel * delta


    def render(self):
        if self.visible:
            egi.green_pen()
            egi.circle(self.pos, 3)



    def checkcollision(self):

        for agent in self.world.enemies:

            to_target = agent.pos - self.pos
            panic_range = 25
            dist = to_target.length()
            if dist < panic_range:
                self.visible = False
                agent.visible = False