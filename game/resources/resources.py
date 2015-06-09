# -*- coding: utf-8 -*-

import pyglet

pyglet.resource.path = ["@game.resources.sprites"]
pyglet.resource.reindex()

flapy = pyglet.resource.image("flapy.png")
pipe = pyglet.resource.image("pipe.png")
pipe1 = pyglet.resource.image("pipe1.png")
floor = pyglet.resource.image("floor.png")
