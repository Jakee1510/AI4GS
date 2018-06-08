'''Autonomous Agent Movement: Seek, Arrive and Flee

Created for COS30002 AI for Games, Lab 05
By Clinton Woodward cwoodward@swin.edu.au

'''
from graphics import egi, KEY
from pyglet import window, clock
from pyglet.gl import *

from vector2d import Vector2D
from world import World
from agent import Agent, AGENT_MODES  # Agent with seek, arrive, flee and pursuit

from Marksman import Marksman
from Hitpoint import Hitpoint
from Bullet import Bullet
from random import randrange

from obstacle import Obstacle

def on_mouse_press(x, y, button, modifiers):
    if button == 1:  # left
        world.target = Vector2D(x, y)
    elif window.mouse.RIGHT:
        world.obstacle.append((Obstacle(world, Vector2D(x, y))))
        if modifiers & KEY.MOD_ALT:
            world.obstacle.clear()



def on_key_press(symbol, modifiers):
    if symbol == KEY.P:
        world.paused = not world.paused

    # Toggle debug force line info on the agent
    elif symbol == KEY._1:
        marksman = world.marksman
        marksman.mode = 'rifle'
        marksman.modespeed = 40
        marksman.shoot()
    elif symbol == KEY._2:
        marksman = world.marksman
        marksman.mode = 'rocket'
        marksman.modespeed = 12
        marksman.shoot()
    elif symbol == KEY._3:
        marksman = world.marksman
        marksman.mode = 'handgun'
        if randrange(0,100) > 50:
            marksman.modespeed = 20
        else:
            marksman.modespeed = 80
        marksman.shoot()
    elif symbol == KEY._4:
        marksman = world.marksman
        marksman.mode = 'grenade'
        if randrange(0, 100) > 50:
            marksman.modespeed = 20
        else:
            marksman.modespeed = 12
        marksman.shoot()



def on_resize(cx, cy):
    world.cx = cx
    world.cy = cy


if __name__ == '__main__':

    # create a pyglet window and set glOptions
    win = window.Window(width=500, height=500, vsync=True, resizable=True)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # needed so that egi knows where to draw
    egi.InitWithPyglet(win)
    # prep the fps display
    fps_display = clock.ClockDisplay()
    # register key and mouse event handlers
    win.push_handlers(on_key_press)
    win.push_handlers(on_mouse_press)
    win.push_handlers(on_resize)

    # create a world for agents
    world = World(500, 500)
    # add one agent
    world.hitpoint = Hitpoint(world)
    world.marksman = Marksman(world)


    # unpause the world ready for movement
    world.paused = False

    while not win.has_exit:
        win.dispatch_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # show nice FPS bottom right (default)
        delta = clock.tick()
        world.update(delta)
        world.render(delta)
        fps_display.draw()
        # swap the double buffer
        win.flip()

