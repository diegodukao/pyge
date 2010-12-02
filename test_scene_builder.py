#! /usr/bin/python

from scene_builder import SceneBuilder

builder = SceneBuilder()

#screen = builder.create_screen()

bg, bg_rect = builder.create_bg()
print bg
print bg_rect

