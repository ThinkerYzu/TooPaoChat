import os
import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GObject, Gtk

# Create tow pipelines to upload and download streams.
#
# - The first pipe will upload a webcam stream to the server at
#   |host:port|. (UDP)
# - The second pipe will listen at |0.0.0.0:port+1| to receive a stream
#   from server and display it on a window. (UDP)
class GstClient(object):
    def __init__(self, host, port):
        super(GstClient, self).__init__()
        self.host = host
        self.port = port
        self._build_upload()
        self._build_download()
        pass

    def _build_upload(self):
        self.ul_pipe = pipe = Gst.Pipeline.new()
        ef = Gst.ElementFactory

        source = ef.make('v4l2src')
        source.set_property('norm', 45056)
        #source = ef.make('videotestsrc')
        vscale = ef.make('videoscale')
        caps = Gst.Caps.from_string('video/x-raw, width=300, height=200')
        capsfilter = ef.make('capsfilter')
        capsfilter.set_property('caps', caps)
        convert = ef.make('videoconvert')
        vp8enc = ef.make('vp8enc')
        rtpvp8pay = ef.make('rtpvp8pay')
        udpsink = ef.make('udpsink')
        udpsink.set_property('host', self.host)
        udpsink.set_property('port', self.port)

        for comp in (source, vscale, capsfilter, convert, vp8enc, rtpvp8pay, udpsink):
            pipe.add(comp)
            pass

        source.link(vscale)
        vscale.link(capsfilter)
        capsfilter.link(convert)
        convert.link(vp8enc)
        vp8enc.link(rtpvp8pay)
        rtpvp8pay.link(udpsink)

        pipe.set_state(Gst.State.PLAYING)
        pass

    def _build_download(self):
        self.dl_pipe = pipe = Gst.Pipeline.new()
        ef = Gst.ElementFactory
        source = ef.make('udpsrc')
        source.set_property('port', self.port + 1)
        caps = Gst.Caps.from_string('application/x-rtp, payload=96')
        source.set_property('caps', caps)
        rtpvp8depay = ef.make('rtpvp8depay')
        vp8dec = ef.make('vp8dec')
        sink = ef.make('autovideosink')

        for comp in (source, rtpvp8depay, vp8dec, sink):
            pipe.add(comp)
            pass

        source.link(rtpvp8depay)
        rtpvp8depay.link(vp8dec)
        vp8dec.link(sink)

        bus = pipe.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self.on_message)

        pipe.set_state(Gst.State.PLAYING)
        pass

    def on_message(self, pipe, msg):
        if msg.type == 1:
            Gtk.main_quit()
            pass
        pass
    pass

def init():
    GObject.threads_init()
    Gst.init(None)
    pass

def build_client(host, port):
    client = GstClient(host, port)
    return client

def run():
    Gtk.main()
    pass
