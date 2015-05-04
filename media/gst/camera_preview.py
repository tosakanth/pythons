import gobject
import gst
import gtk


gobject.threads_init()


class Webcam(object):
    def __init__(self):
        self.window = gtk.Window()
        self.window.connect('destroy', self.quit)
        self.window.set_default_size(320, 240)

        self.drawingarea = gtk.DrawingArea()
        self.window.add(self.drawingarea)

        # Create GStreamer pipeline
        self.pipeline = gst.Pipeline()

        # Create bus to get events from GStreamer pipeline
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message::error', self.on_error)

        # This is needed to make the video output in our DrawingArea:
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message::element', self.on_sync_message)

        # Create GStreamer elements
        self.src = gst.element_factory_make('v4l2src')
        self.sink = gst.element_factory_make('autovideosink')

        # Add elements to the pipeline
        self.pipeline.add(self.src)
        self.pipeline.add(self.sink)

        self.src.link(self.sink)

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

    def on_error(self, bus, msg):
        print('on_error():', msg.parse_error())


webcam = Webcam()
webcam.run()
