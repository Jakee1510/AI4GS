'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au

'''

from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange, uniform
from path import Path

AGENT_MODES = {
    KEY._1: 'seek',
    KEY._2: 'arrive_slow',
    KEY._3: 'arrive_normal',
    KEY._4: 'arrive_fast',
    KEY._5: 'flee',
    KEY._6: 'pursuit',
    KEY._7: 'follow_path',
    KEY._8: 'wander',
    KEY._9: 'neighbourhood',
    KEY._0: 'hide',
}


class Agent(object):
    # NOTE: Class Object (not *instance*) variables!
    DECELERATION_SPEEDS = {
        'slow': 0.9,
        'normal': 0.6,
        'fast': 0.1,
        ### ADD 'normal' and 'fast' speeds here
        # ...
        # ...
    }

    def __init__(self, world=None, scale=30.0, mass=1.0, mode='seek', hunter=False, id=0):
        # keep a reference to the world object
        self.world = world
        self.mode = mode
        # where am i and where am i going? random start pos
        dir = radians(random() * 360)
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        self.force = Vector2D()  # current steering force
        self.accel = Vector2D()  # current acceleration due to force
        self.mass = mass

        # data for drawing this agent
        self.color = 'ORANGE'
        self.vehicle_shape = [
            Point2D(-1.0, 0.6),
            Point2D(1.0, 0.0),
            Point2D(-1.0, -0.6)
        ]

        ### path to follow?
        # self.path = ??
        self.path = Path()
        self.randomise_path()  # <-- Doesn’t exist yet but you’ll create it
        self.waypoint_threshold = 50.0  # <-- Work out a value for this as you test!

        ### wander details
        # self.wander_?? ...
        # NEW WANDER INFO
        # NEW WANDER INFO
        self.wander_target = Vector2D(1, 0)
        self.wander_dist = 1.0 * scale
        self.wander_radius = 1.0 * scale
        self.wander_jitter = 10.0 * scale
        self.bRadius = scale
        # Force and speed limiting code
        self.max_speed = 40.0 * scale
        self.max_force = 500.0
        # limits?
        self.max_speed = 20.0 * scale
        ## max_force ??

        # neighbourhood
        self.tagged = False

        # debug draw info?
        self.show_info = False

        self.hunter = hunter

        if self.hunter == True:
            self.max_speed = 20 * scale
        self.visible = True

    def collidecircle(self):
        egi.circle(self.pos, 20, False)

    def calculate(self, delta):
        # calculate the current steering force
        if self.hunter == True:
            force = self.wander(delta)
            return force
        else:
            mode = self.mode
            if mode == 'seek':
                force = self.seek(self.world.target)
            elif mode == 'arrive_slow':
                force = self.arrive(self.world.target, 'slow')
            elif mode == 'arrive_normal':
                force = self.arrive(self.world.target, 'normal')
            elif mode == 'arrive_fast':
                force = self.arrive(self.world.target, 'fast')
            elif mode == 'flee':
                force = self.flee(self.world.target)
            elif mode == 'pursuit':
                force = self.pursuit(self.world.hunter)
            elif mode == 'wander':
                force = self.wander(delta)
            elif mode == 'follow_path':
                force = self.follow_path(self.path.current_pt(), 'fast')
            elif mode == 'neighbourhood':
                self.get_neighbours(self.world.agents, self.world.radius)
                force = self.wander(delta)
                force += self.alignment(self.world.agents) * self.world.alignment
                force += self.separation(self.world.agents) * self.world.separation
                force += self.cohesion(self.world.agents) * self.world.cohesion
            elif mode == 'hide':
                force = self.hide(self.get_hunters(self.world.agents))
            else:
                force = Vector2D()
            self.force = force
        return force

    def update(self, delta):
        ''' update vehicle position and orientation '''
        # calculate and set self.force to be applied
        ## force = self.calculate()
        force = self.calculate(delta)  # <-- delta needed for wander
        force.truncate(self.max_force)
        ## limit force? <-- for wander
        # ...
        # determin the new accelteration
        self.accel = force / self.mass  # not needed if mass = 1.0
        # new velocity
        self.vel += self.accel * delta
        # check for limits of new velocity
        self.vel.truncate(self.max_speed)
        # update position
        self.pos += self.vel * delta
        # update heading is non-zero velocity (moving)
        if self.vel.length_sq() > 0.00000001:
            self.heading = self.vel.get_normalised()
            self.side = self.heading.perp()
        # treat world as continuous space - wrap new position if needed
        self.world.wrap_around(self.pos)

        if self.mode == 'neighbourhood' and not self.hunter:
            if self.tagged:
                self.color = 'GREEN'
            else:
                self.color = 'ORANGE'

    def render(self, color=None):
        ''' Draw the triangle agent with color'''
        # draw the path if it exists and the mode is follow
        if self.mode == 'follow_path':
            ## ...
            self.path.render()
            pass
        if self.hunter:
            self.color = 'RED'
        # draw the ship

        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                          self.heading, self.side, self.scale)

        # draw it!
        if self.visible:
            egi.closed_shape(pts)

        # draw wander info?
        if self.mode == 'wander' or self.hunter == True:
            wnd_pos = Vector2D(self.wander_dist, 0)
            wld_pos = self.world.transform_point(wnd_pos, self.pos, self.heading, self.side)
            # draw the wander circle
            egi.green_pen()
            egi.circle(wld_pos, self.wander_radius)
            # draw the wander target (little circle on the big circle)
            egi.red_pen()
            wnd_pos = (self.wander_target + Vector2D(self.wander_dist, 0))
            wld_pos = self.world.transform_point(wnd_pos, self.pos, self.heading, self.side)
            egi.circle(wld_pos, 3)
            ## ...
            pass

        # add some handy debug drawing info lines - force and velocity
        if self.show_info:
            s = 0.5  # <-- scaling factor
            # force
            egi.red_pen()
            egi.line_with_arrow(self.pos, self.pos + self.force * s, 5)
            # velocity
            egi.grey_pen()
            egi.line_with_arrow(self.pos, self.pos + self.vel * s, 5)
            # net (desired) change
            egi.white_pen()
            egi.line_with_arrow(self.pos + self.vel * s, self.pos + (self.force + self.vel) * s, 5)
            egi.line_with_arrow(self.pos, self.pos + (self.force + self.vel) * s, 5)

    def speed(self):
        return self.vel.length()

    # --------------------------------------------------------------------------

    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return (desired_vel - self.vel)

    def flee(self, hunter_pos):
        ''' move away from hunter position '''
        desired_vel = (self.pos - hunter_pos).normalise() * self.max_speed
        ## add panic distance (second)
        panic_range = 200
        ## add flee calculations (first)
        to_target = hunter_pos - self.pos
        dist = to_target.length()
        if dist > panic_range:
            return Vector2D()
        return (desired_vel - self.vel)

    def arrive(self, target_pos, speed):
        ''' this behaviour is similar to seek() but it attempts to arrive at
            the target position with a zero velocity'''
        decel_rate = self.DECELERATION_SPEEDS[speed]
        to_target = target_pos - self.pos
        dist = to_target.length()
        if dist > 0:
            # calculate the speed required to reach the target given the
            # desired deceleration rate
            speed = dist / decel_rate
            # make sure the velocity does not exceed the max
            speed = min(speed, self.max_speed)
            # from here proceed just like Seek except we don't need to
            # normalize the to_target vector because we have already gone to the
            # trouble of calculating its length for dist.
            desired_vel = to_target * (speed / dist)
            return (desired_vel - self.vel)
        return Vector2D(0, 0)

    def pursuit(self, evader):
        ''' this behaviour predicts where an agent will be in time T and seeks
            towards that point to intercept it. '''
        ## OPTIONAL EXTRA... pursuit (you'll need something to pursue!)
        return Vector2D()

    def wander(self, delta):
        ''' Random wandering using a projected jitter circle. '''
        wt = self.wander_target
        # this behaviour is dependent on the update rate, so this line must
        # be included when using time independent framerate.
        jitter_tts = self.wander_jitter * delta  # this time slice
        # first, add a small random vector to the target's position
        wt += Vector2D(uniform(-1, 1) * jitter_tts, uniform(-1, 1) * jitter_tts)
        # re-project this new vector back on to a unit circle
        wt.normalise()
        # increase the length of the vector to the same as the radius
        # of the wander circle
        wt *= self.wander_radius
        # move the target into a position WanderDist in front of the agent
        target = wt + Vector2D(self.wander_dist, 0)
        # project the target into world space
        wld_target = self.world.transform_point(target, self.pos, self.heading, self.side)
        # and steer towards it
        return self.seek(wld_target)

    def randomise_path(self):
        cx = self.world.cx  # width
        cy = self.world.cy  # height
        margin = min(cx, cy) * (1 / 6)  # use this for padding in the next line ...
        self.path.create_random_path(2, margin, margin, cx / 2, cy / 2, True)  # you have to figure out the parameters

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

    def get_neighbours(self, bots, radius):
        for bot in bots:
            bot.tagged = False
            dist = Vector2D.distance_sq(self.pos, bot.pos)
            if dist < (radius + bot.bRadius) ** 2:
                bot.tagged = True

    def get_hunters(self, bots):
        for bot in bots:
            if bot.hunter == True:
                return bot

    def alignment(self, group):
        avgHeading = Vector2D()
        avgCount = 0

        for bot in group:
            if self != bot and bot.tagged:
                avgHeading += bot.pos
                avgCount += 1

        if avgCount > 0:
            avgHeading /= float(avgCount)
            avgHeading -= self.heading
        return avgHeading

    def separation(self, group):
        centerMass = Vector2D()
        steeringForce = Vector2D()
        avgCount = 0

        for bot in group:
            if self != bot and self.tagged:
                centerMass += bot.pos
                avgCount += 1

        if avgCount > 0:
            centerMass /= float(avgCount)
            steeringForce += self.flee(centerMass)

        return steeringForce

    def cohesion(self, group):
        centerMass = Vector2D()
        steeringForce = Vector2D()
        avgCount = 0

        for bot in group:
            if self != bot and self.tagged:
                centerMass += bot.pos
                avgCount += 1
        if avgCount > 0:
            centerMass /= float(avgCount)
            steeringForce += self.seek(centerMass)

        return steeringForce

    def GetHidingPosition(self, hunter_pos, obst):
        distFromBoundary = 110
        distAway = obst.radius + distFromBoundary


        toObj = (obst.pos - hunter_pos).normalise()

        return (toObj * distAway) + obst.pos

    def hide(self, hunter):

        DistToClosest = float('inf')
        BestHidingSpot = Vector2D()

        to_target = hunter.pos - self.pos
        panic_range = 60
        dist = to_target.length()
        if dist < panic_range:
            self.visible = False


        for obst in self.world.obstacle:
            hidingSpot = self.GetHidingPosition(hunter.pos, obst)
            hidingDist = Vector2D.distance_sq(hidingSpot, self.pos) #change to self.pos for closest obst search, and change vector to positive
            egi.cross(hidingSpot, 4)
            if hidingDist < DistToClosest:
                DistToClosest = hidingDist
                BestHidingSpot = hidingSpot

        if BestHidingSpot:
            egi.line_by_pos(hunter.pos, BestHidingSpot)
            return self.arrive(BestHidingSpot, 'fast')
        return self.flee(hunter.pos)



