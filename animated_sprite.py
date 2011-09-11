#! /usr/bin/env python

from pygame import sprite, time

class Animation:
    def __init__(self, sequence_of_frames):
        self.frames = sequence_of_frames

class AnimatedSprite(sprite.Sprite):
    def __init__(self, position, image_frames, lines, columns, fps=10):
        sprite.Sprite.__init__(self)
        self.frames = self.get_frames(image_frames, lines, columns)
        
        self.animation = Animation(xrange(len(self.frames)))
        
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        
        #Track the time the animation was created and the time between
        #updates. That way we can figure out when the image needs to be
        #changed
        self.current_frame = 0
        self.start = time.get_ticks()
        self.last_update = 0
        if fps == 0:
            fps = 1
        self.delay = 1000/fps
        
    def get_frames(self, image, lines, columns):
        image_width, image_height = image.get_size()
        
        frames = []
        frame_width = image_width / columns
        frame_height = image_height / lines
        for j in xrange(lines):
            y = j * frame_height
            for i in xrange(columns):
                x = i * frame_width
                frames.append(image.subsurface((x, y,
                                frame_width, frame_height)))
        
        return frames
        
    
    def update(self):
        '''Update the frame of the animation. It will only occur if the
        time passed since the last update is longer than the delay 
        (1000/fps)'''
        t = time.get_ticks()
        
        if t - self.last_update > self.delay:
            self.change_frame()
            self.last_update = t
        
    def change_frame(self):
        if self.current_frame < (len(self.animation.frames) - 1):
            self.current_frame += 1
        else:
            self.current_frame = 0
        
        self.image = self.frames[self.animation.frames[self.current_frame]]
        
    def create_animation(self, animation_order):
        return Animation(animation_order)
        
    def set_animation(self, animation):
        self.animation = animation
