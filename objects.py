#! /usr/bin/python

import pygame
from animated_sprite import AnimatedSprite

class Actor(AnimatedSprite):
    def __init__(self, position, image_frames, lines, columns, fps=10):
        AnimatedSprite.__init__(self, position, image_frames, lines, columns, fps=10)
        
        self.jump_speed = 1
        self.jumping = False
        self.gravity = 0.7
        self.max_gravity_speed = 6
        
        self.xspeed = 1
        self.yspeed = 1
        self.xdir = 0
        self.ydir = 0
        self.last_xdir = 0
        self.last_ydir = 0
        
    def update(self):
        super(Actor, self).update()
        self.rect.move_ip(0, self.jump_speed)

