#! /usr/bin/env python

import Image
import gtk
import tools

class AnimatedSprite:
    def __init__(self, filename, x, y, lines, columns, fps=10):
        self.x = x
        self.y = y
        self.filename = filename
        image_frames = Image.open(filename)
        frames_pixbuf = self.get_frames(image_frames, lines, columns)
        #self.frames_pixmap, self.frames_mask = [frame_pixbuf.render_pixmap_and_mask() for frame_pixbuf in frames_pixbuf]
        #frame_pixbuf = tools.get_frame_pixbuf(image_frames, (0,0,101,101))
        #self.pixmap, self.mask = frame_pixbuf.render_pixmap_and_mask()
        self.frame_pixmap, self.frame_mask = frames_pixbuf[0].render_pixmap_and_mask()
        
    def get_frames(self, image, lines, columns):        
        frames = []
        frame_width = image.size[0] / columns
        frame_height = image.size[1] / lines
        for j in xrange(lines):
            y = j * frame_height
            for i in xrange(columns):
                x = i * frame_width
                frames.append(
                    tools.get_frame_pixbuf(
                        image,
                        (x, y, x+frame_width, y+frame_height),
                    )
                )
        
        return frames
