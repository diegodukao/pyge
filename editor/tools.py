#!/usr/bin/python

import gtk
import Image
import StringIO

def get_frame_pixbuf(image, crop_coords):
    frame = image.crop(crop_coords)
    
    return image2pixbuf(frame)

def image2pixbuf(im):  
    file1 = StringIO.StringIO()  
    im.save(file1, "ppm")  
    contents = file1.getvalue()  
    file1.close()  
    loader = gtk.gdk.PixbufLoader("pnm")  
    loader.write(contents, len(contents))  
    pixbuf = loader.get_pixbuf()
    loader.close()
    
    return pixbuf
