import os
import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GObject, Gtk

class GstRemoteClient(object):
    def __init__(self, server, name, host, port):
        super(GstRemoteClient, self).__init__()
        self.server = server
        self.pipe = server.pipe
        self.vmixer = server.vmixer
        self.output_tee = server.output_tee

        self.name = name
        self.host = host
        self.port = port

        self._build_input()
        self._build_output()
        pass

    def _build_input(self):
        print 'build\n'
        pipe = self.pipe

        ef = Gst.ElementFactory
        self.source = source = ef.make('udpsrc')
        source.set_property('port', self.port)
        source.set_property('reuse', True)
        caps = Gst.Caps.from_string('application/x-rtp, payload=96')
        source.set_property('caps', caps)
        rtpvp8depay = ef.make('rtpvp8depay')
        self.vp8dec = vp8dec = ef.make('vp8dec')

        self.comps = comps = [source, rtpvp8depay, vp8dec]
        for comp in comps:
            pipe.add(comp)
            pass
        for src, dst in zip(comps[:-1], comps[1:]):
            src.link(dst)
            pass
        pass

    def _build_output(self):
        print 'build output\n'
        pipe = self.pipe

        ef = Gst.ElementFactory
        self.udpsink = sink = ef.make('udpsink')
        sink.set_property('host', self.host)
        print self.port + 1
        sink.set_property('port', self.port + 1)

        pipe.add(sink)

        self.comps.append(sink)
        pass

    def do_link(self):
        # Request and set a new pad only when needed, or it may be
        # blocked.
        self.server.request_mixer_pad()

        self.vp8dec.link(self.vmixer)

        tee = self.output_tee
        tee.link(self.udpsink)

        for c in self.comps:
            c.sync_state_with_parent()
            pass
        pass
    pass

class GstServer(object):
    def __init__(self):
        super(GstServer, self).__init__()
        self.clients = {}
        self._build_pipe_core()
        self._num_clients = 0
        pass

    def _build_pipe_core(self):
        self.pipe = pipe = Gst.Pipeline.new()
        ef = Gst.ElementFactory
        self.vmixer = vmixer = ef.make('videomixer')
        vp8enc = ef.make('vp8enc')
        rtpvp8pay = ef.make('rtpvp8pay')
        self.output_tee = tee = ef.make('tee')

        comps = (vmixer, vp8enc, rtpvp8pay, tee)
        for comp in comps:
            pipe.add(comp)
            pass
        for src, dst in zip(comps[:-1], comps[1:]):
            src.link(dst)
            pass
        bus = pipe.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self.on_message)
        pass

    def request_mixer_pad(self):
        pad = self.vmixer.get_request_pad('sink_%d' % (self._num_clients))
        pad.set_property('xpos', 300 * self._num_clients)
        pad.set_property('ypos', 0)
        self._num_clients = self._num_clients + 1
        print pad.name
        return pad

    def add_client(self, name, host, port):
        assert not self.clients.has_key(name)
        client = self.clients[name] = GstRemoteClient(self, name, host, port)

        pipe = self.pipe
        if len(self.clients) == 1:
            client.do_link()
            print 'PLAYING\n'
            pipe.set_state(Gst.State.PLAYING)
        else:
            # Wait all existing udpsrc idle, and safely change the
            # links in the pipeline during the probe callbacks.
            waitings = set(self.clients.values())
            waitings.remove(client)
            for c in self.clients.values():
                if c == client:
                    continue

                pad = c.vp8dec.get_static_pad('src')
                pad.add_probe(Gst.PadProbeType.IDLE, self.on_probe_cb, (client, c, waitings))
                pass
            pass

        return client

    def on_message(self, elm, msg):
        #print msg, msg.type
        pass

    def on_probe_cb(self, pad, info, data):
        newclient, client, waitings = data
        if not waitings:
            return Gst.PadProbeReturn.REMOVE

        waitings.remove(client)
        if waitings:
            return Gst.PadProbeReturn.DROP

        newclient.do_link()
        return Gst.PadProbeReturn.REMOVE
    pass

server = None

def init():
    global server
    GObject.threads_init()
    Gst.init(None)
    server = GstServer()
    pass

def add_client(name, host, port):
    client = server.add_client(name, host, port)
    return client

def run():
    Gtk.main()
    pass
