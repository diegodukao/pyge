#!/usr/bin/python

import sys
import gtk

class PyGE:
    
    def __init__(self):
        # using GtkBuilder to build the interface from the glade file
        try:
            builder = gtk.Builder()
            builder.add_from_file("ui_pyge.glade")
        except:
            self.error_message("Failed to load UI XML file: ui_pyge.glade")
            sys.exit(1)
            
        # get the widgets which will be referenced in callbacks
        self.window = builder.get_object("window")
        self.viewport = builder.get_object("viewport")
        
        # initializing some variables
        self.drawing_area = None
        self.background_path = None
        self.filename = None
        self.width = None
        self.height = None
        self.sprites = {}
        
        # connect signals
        builder.connect_signals(self)
        
    def main(self):
        self.window.show()
        gtk.main()
    
    # Called when the user clicks the 'Save' menu item.
    def on_save_menu_item_activate(self, menuitem, data=None):
        if self.filename == None:
            filename = self.get_save_filename()
            if filename:
                self.write_file(filename)
    
    # Called when the user clicks the 'Create scene from backgroud' menu item.
    def on_background_menu_item_activate(self, menuitem, data=None):
        filename = self.get_open_filename()
        
        if filename:
            # If a drawing area already exists, it has to be destroyed
            if self.drawing_area:
                self.drawing_area.destroy()
            
            pixbuf = gtk.gdk.pixbuf_new_from_file(filename)
            self.background_pixmap, mask = pixbuf.render_pixmap_and_mask()
            self.width = pixbuf.get_width()
            self.height = pixbuf.get_height()
            
            self.drawing_area = gtk.DrawingArea()
            self.drawing_area.set_size_request(self.width, self.height)
            
            #adding the drawing area to the viewport
            self.viewport.add(self.drawing_area)
            
            #making the connections (??)
            self.drawing_area.connect("expose-event", self.drawing_area_expose)
            
            self.drawing_area.show()
            
            self.background_path = filename
    
    # Called when the user clicks the 'Insert sprite' menu item.
    def on_sprite_menu_item_activate(self, menuitem, data=None):
        filename = self.get_open_filename()
        
        if filename and self.drawing_area:
            pixbuf = gtk.gdk.pixbuf_new_from_file(filename)
            pixmap, mask = pixbuf.render_pixmap_and_mask()
            
            # Adding the image to the dictionary that contains all
            # sprites to be drawn
            image = {'pixmap': pixmap, 'x': 100, 'y': 100, 'filename': filename}
            self.sprites['image1'] = image
            
            
    def on_window_destroy(self, widget, data=None):
        gtk.main_quit()
    
    
    # Updates the drawing area, redrawing the background and sprites
    def drawing_area_expose(self, area, event):
        self.style = self.drawing_area.get_style()
        self.gc = self.style.fg_gc[gtk.STATE_NORMAL]
        self.draw_background()
        self.draw_sprites()
        
        return True
        
    def draw_background(self):
        self.draw_to_drawing_area(self.background_pixmap, 0, 0)
        
        return
    
    def draw_sprites(self):
        if self.sprites:
            for k in self.sprites.keys():
                self.draw_to_drawing_area(self.sprites[k]['pixmap'],
                                          self.sprites[k]['x'],
                                          self.sprites[k]['y'])
    
    def draw_to_drawing_area(self, pixmap, x, y):
        self.drawing_area.window.draw_drawable(self.gc, pixmap,
                                               0, 0, x, y, -1, -1)
    
    # We call get_open_filename() when we want to get a filename to open from the
    # user. It will present the user with a file chooser dialog and return the 
    # filename or None. 
    def get_open_filename(self):
        filename = None
        chooser = gtk.FileChooserDialog("Open File...", self.window,
                                        gtk.FILE_CHOOSER_ACTION_OPEN,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            filename = chooser.get_filename()
        
        chooser.destroy()
        
        return filename
    
    # We call get_save_filename() when we want to get a filename to save from the
    # user. It will present the user with a file chooser dialog and return the 
    # filename or None.
    def get_save_filename(self):
        filename = None
        chooser = gtk.FileChooserDialog("Save File...", self.window,
                                        gtk.FILE_CHOOSER_ACTION_SAVE,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        
        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            filename = chooser.get_filename()
        
        chooser.destroy()
        
        return filename
    
    # writing the xml file describing the scene
    def write_file(self, filename):
        while gtk.events_pending():
            gtk.main_iteration()
        
        try:
            text = "<?xml version='1.0'?>\n"
            text += "<scene width='" + str(self.width)
            text += "' height='" + str(self.height) +"'>\n"
            text += "   <background>" + self.background_path
            text += "</background>\n"
            
            if self.sprites:
                for k in self.sprites.keys():
                    text += "   <sprite x='" + str(self.sprites[k]['x']) + "'"
                    text += " y='" + str(self.sprites[k]['y']) +"'"
                    text += " filename='" + self.sprites[k]['filename'] + "'>"
                    text += k + "</sprite>\n"
            
            text += "</scene>"
            
            if filename:
                file_out = open(filename, "w")
            else:
                file_out = open(self.filename, "w")
            file_out.write(text)
            file_out.close()
            
            if filename:
                self.filename = filename
        except:
            # error writing file, show message to user
            if filename:
                self.error_message("Could not save file: %s" % filename)
            else:
                self.error_message("Could not save file: %s" % self.filename)
    
    # We call error_message() any time we want to display an error message to 
    # the user. It will both show an error dialog and log the error to the 
    # terminal window.
    def error_message(self, message):
    
        # log to terminal window
        print message
        
        # create an error message dialog and display modally to the user
        dialog = gtk.MessageDialog(None,
                                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)
        
        dialog.run()
        dialog.destroy()

if __name__ == "__main__":
    pyge = PyGE()
    pyge.main()
