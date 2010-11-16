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
        
        # connect signals
        builder.connect_signals(self)
        
    def main(self):
        self.window.show()
        gtk.main()
        
    def on_window_destroy(self, widget, data=None):
        gtk.main_quit()

if __name__ == "__main__":
    pyge = PyGE()
    pyge.main()
