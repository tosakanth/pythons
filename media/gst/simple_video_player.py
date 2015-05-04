##########################################################################
# Before running this file, you need to install gstreamer and python-gst #
# apt-get install python-gst0.10 python-gst0.10-dev                      #
##########################################################################

from os import path

import gobject
import gst
import gtk


gobject.threads_init()

#You could change to wherever of your own 
filename = path.join(path.dirname(path.abspath(__file__)), 'helloworld.ogv')
uri = 'file://' + filename


class Player(object):
    def __init__(self):
        self.window = gtk.Window()
        self.window.connect('destroy', self.quit)
        self.window.set_default_size(800, 450)

        self.drawingarea = gtk.DrawingArea()
        self.window.add(self.drawingarea)

        # Create GStreamer pipeline
        self.pipeline = gst.Pipeline()

        # Create bus to get events from GStreamer pipeline
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message::eos', self.on_eos)
        self.bus.connect('message::error', self.on_error)

        # This is needed to make the video output in our DrawingArea:
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message::element', self.on_sync_message)

        # Create GStreamer elements
        self.playbin = gst.element_factory_make('playbin2')

        # Add playbin2 to the pipeline
        self.pipeline.add(self.playbin)

        # Set properties
        self.playbin.set_property('uri', uri)

    def run(self):
        self.window.show_all()
        # You need to get the XID after window.show_all().  You shouldn't get it
        # in the on_sync_message() handler because threading issues will cause
        # segfaults there. 
        self.xid = self.drawingarea.window.xid
        self.pipeline.set_state(gst.STATE_PLAYING)
        gtk.main()

    def quit(self, window):
        self.pipeline.set_state(gst.STATE_NULL)
        gtk.main_quit()

    def on_sync_message(self, bus, msg):
        if msg.structure.get_name() == 'prepare-xwindow-id':
            print('prepare-xwindow-id')
            msg.src.set_property('force-aspect-ratio', True)
            msg.src.set_xwindow_id(self.xid)

    def on_eos(self, bus, msg):
        print('on_eos(): seeking to start of video')
        self.pipeline.seek_simple(
            gst.FORMAT_TIME,        
            gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_KEY_UNIT,
            0L
        )

    def on_error(self, bus, msg):
        print('on_error():', msg.parse_error())


p = Player()
p.run()
