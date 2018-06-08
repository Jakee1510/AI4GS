'''A 2d world that supports agents with steering behaviour

Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au

'''

from vector2d import Vector2D
from matrix33 import Matrix33
from graphics import egi
from RefuelStation import RefuelStation
from agent import Agent
from bullet import Bullet
from target import Target

class World(object):
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.targett = Target(self)
        self.hunter = None
        self.agent = Agent(self,30, 1, 'seek', False, self.targett)
        self.enemies = []
        self.bullet = []
        self.enemytarget = None
        self.paused = True
        self.show_info = True

        self.refuelst = RefuelStation()

    def update(self, delta):
        if not self.paused:
            self.agent.update(delta)

            for agent in self.enemies:
                agent.update(delta)
                if agent.visible == False:
                    self.enemies.remove(agent)

            for bullet in self.bullet:
                bullet.update(delta)

            self.enemytarget = self.agent



    def render(self):

        self.agent.render()

        for agent in self.enemies:
            agent.render()

        self.targett.render()


        for bullet in self.bullet:
            bullet.render()

        if self.show_info:
            infotext = ', '.join(set(self.agent.mode))
            egi.white_pen()
            egi.text_at_pos(0, 0, infotext)

        self.refuelst.render()



    def add_enemy(self, mode, isenemy, target, color):
        self.enemies.append(Agent(self, 25, 1, mode, isenemy, target, color))


    def wrap_around(self, pos):
        ''' Treat world as a toroidal space. Updates parameter object pos '''
        max_x, max_y = self.cx, self.cy
        if pos.x > max_x:
            pos.x = pos.x - max_x
        elif pos.x < 0:
            pos.x = max_x - pos.x
        if pos.y > max_y:
            pos.y = pos.y - max_y
        elif pos.y < 0:
            pos.y = max_y - pos.y

    def transform_points(self, points, pos, forward, side, scale):
        ''' Transform the given list of points, using the provided position,
            direction and scale, to object world space. '''
        # make a copy of original points (so we don't trash them)
        wld_pts = [pt.copy() for pt in points]
        # create a transformation matrix to perform the operations
        mat = Matrix33()
        # scale,
        mat.scale_update(scale.x, scale.y)
        # rotate
        mat.rotate_by_vectors_update(forward, side)
        # and translate
        mat.translate_update(pos.x, pos.y)
        # now transform all the points (vertices)
        mat.transform_vector2d_list(wld_pts)
        # done
        return wld_pts

    def transform_point(self, point, pos, forward, side):
        ''' Transform the given single point, using the provided position,
        and direction (forward and side unit vectors), to object world space. '''
        # make a copy of the original point (so we don't trash it)
        wld_pt = point.copy()
        # create a transformation matrix to perform the operations
        mat = Matrix33()
        # rotate
        mat.rotate_by_vectors_update(forward, side)
        # and translate
        mat.translate_update(pos.x, pos.y)
        # now transform the point (in place)
        mat.transform_vector2d(wld_pt)
        # done
        return wld_pt
