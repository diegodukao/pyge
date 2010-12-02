#! /usr/bin/python

import sys
import pygame
from scene_builder import SceneBuilder

pygame.init()

builder = SceneBuilder()

screen = builder.create_screen()

bg, bg_rect = builder.create_bg()

sprites = builder.get_sprites()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
    screen.blit(bg, bg_rect)
    
    for sprite in sprites.itervalues():
         screen.blit(sprite.image, sprite.rect)
    
    pygame.display.flip()


