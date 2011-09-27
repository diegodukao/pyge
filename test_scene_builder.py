#! /usr/bin/python

import sys
import pygame
from scene_builder import SceneBuilder

pygame.init()

# Creating the scene with the Scene Builder
builder = SceneBuilder("editor/teste6.pyge")
screen = builder.create_screen()
bg, bg_rect = builder.create_bg()
sprites = builder.get_sprites()
animated_sprites = builder.get_animated_sprites()
animated_sprites["sprite1"].set_animation("idle")

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
    # Drawing the background
    screen.blit(bg, bg_rect)
    
    # Drawing the sprites
    for sprite in sprites.itervalues():
         screen.blit(sprite.image, sprite.rect)
         
    for animated_sprite in animated_sprites.itervalues():
        animated_sprite.update()
        screen.blit(animated_sprite.image, animated_sprite.rect)
    
    # Updating the screen
    pygame.display.flip()
