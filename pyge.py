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
        self.background = None
        self.background_path = None
        self.filename = None
        
        # creating the drawing area
        self.area = gtk.DrawingArea()
        self.area.set_size_request(1000, 1000)
        self.pangolayout = self.area.create_pango_layout("")
        
        # adding the drawing area to the viewport
        self.viewport.add(self.area)
        
        # making the connections (??)
        self.area.connect("expose-event", self.area_expose)
        
        self.area.show()
        
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
    
    # Called when the user clicks the 'Insert Backgroud' menu item.
    def on_background_menu_item_activate(self, menuitem, data=None):
        filename = self.get_open_filename()
        
        # If there is already a background, it needs to be destroyed
        if filename:
            if self.background:
                self.background.destroy()
            
            self.background = gtk.Image()
            self.background.set_from_file(filename)
            
            self.viewport.add(self.background)
            self.background.show()
            
            self.background_path = filename
    
    def on_window_destroy(self, widget, data=None):
        gtk.main_quit()
    
    
    def area_expose(self, area, event):
        self.style = self.area.get_style()
        self.gc = self.style.fg_gc[gtk.STATE_NORMAL]
        self.draw_point(10,10)
        self.draw_points(110, 10)
        self.draw_pixmap(215, 0)
        self.draw_line(210, 10)
        self.draw_lines(213, 10)
        return True
    
    def draw_point(self, x, y):
        self.area.window.draw_point(self.gc, x+30, y+30)
        self.pangolayout.set_text("Point")
        self.area.window.draw_layout(self.gc, x+5, y+50, self.pangolayout)
        return

    def draw_points(self, x, y):
        points = [(x+10,y+10), (x+10,y), (x+40,y+30),
                  (x+30,y+10), (x+50,y+10)]
        self.area.window.draw_points(self.gc, points)
        self.pangolayout.set_text("Points")
        self.area.window.draw_layout(self.gc, x+5, y+50, self.pangolayout)
        return

    def draw_line(self, x, y):
        self.area.window.draw_line(self.gc, x+10, y+10, x+20, y+30)
        self.pangolayout.set_text("Line")
        self.area.window.draw_layout(self.gc, x+5, y+50, self.pangolayout)
        return

    def draw_lines(self, x, y):
        points = [(x+10,y+10), (x+10,y), (x+40,y+30),
                  (x+30,y+10), (x+50,y+10)]
        self.area.window.draw_lines(self.gc, points)
        self.pangolayout.set_text("Lines")
        self.area.window.draw_layout(self.gc, x+5, y+50, self.pangolayout)
        return
        
    def draw_pixmap(self, x, y):
        pixbuf=gtk.gdk.pixbuf_new_from_file('/home/diego/Pictures/avatar.png')
        pixmap, mask=pixbuf.render_pixmap_and_mask()
        
        self.area.window.draw_drawable(self.gc, pixmap, 0, 0, x+15, y+25,
                                       -1, -1)
        self.pangolayout.set_text("Pixmap")
        self.area.window.draw_layout(self.gc, x+5, y+80, self.pangolayout)
        return
    
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
            text += "<scene>\n"
            text += "   <background>" + self.background_path
            text += "</background>\n"
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
