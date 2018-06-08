'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au

'''

from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, uniform
from path import Path



class Hitpoint(object):


    def __init__(self, world=None, scale=30.0, mass=1.0, mode='follow_path'):
        self.world = world
        self.mode = mode

        dir = radians(random() * 360)
        self.pos = Vector2D(world.cx - 50, world.cy / 2)
        self.vel = Vector2D(0,0)
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        self.force = Vector2D()  # current steering force
        self.accel = Vector2D()  # current acceleration due to force
        self.mass = mass

        ### path to follow?
        # self.path = ??
        self.path = Path()
        self.path.create_hitpoint_path()  # <-- Doesn’t exist yet but you’ll create it
        self.waypoint_threshold = 10.0  # <-- Work out a value for this as you test!

        self.ishit = False

        self.max_force = 500.0
        # limits?
        self.max_speed = 50.0
        ## max_force ??


    def collidecircle(self):
        egi.circle(self.pos, 20, False)

    def calculate(self, delta):

        mode = self.mode
        if mode == 'follow_path':
            force = self.follow_path(self.path.current_pt(), 'fast')
        else:
            force = Vector2D()
            self.force = force

        return force

    def update(self, delta):

        force = self.calculate(delta)
        force.truncate(self.max_force)

        self.accel = force / self.mass
        self.vel += self.accel * delta
        # update position
        self.pos += self.vel * delta
        if self.vel.length_sq() > 0.00000001:
            self.heading = self.vel.get_normalised()
            self.side = self.heading.perp()

        self.world.wrap_around(self.pos)


    def render(self, color=None):
        ''' Draw the triangle agent with color'''
        # draw the path if it exists and the mode is follow
        if self.mode == 'follow_path':
            ## ...
            self.path.render()
            pass
        if self.ishit:
            egi.red_pen()
        else:
            egi.blue_pen()
        # draw the ship

        egi.circle(self.pos, 20, True)

        self.ishit = False


    # --------------------------------------------------------------------------


    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return (desired_vel - self.vel)




    def follow_path(self, waypoint_pos, speed):
        if self.path.is_finished():
            return self.arrive(self.path.current_pt(), speed)
        else:
            to_target = self.path.current_pt() - self.pos
            dist = to_target.length()
            if dist < self.waypoint_threshold:
                print("hi there")
                self.path.inc_current_pt()
            return self.seek(self.path.current_pt())

