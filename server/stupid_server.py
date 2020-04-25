from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import gstserver
import gi
gi.require_version("Gst", "1.0")
from gi.repository import GObject, Gtk

pwds = {
    "user1": "user1_123",
    "user2": "user2_123"
}
ul_ports = {}
client_ip = {}
gst_clients = {}

FIRST_PORT = 8050
for i, name in enumerate(pwds.keys()):
    ul_ports[name] = FIRST_PORT + i * 2
    pass

# This stupid handler assigns every user a fixed port number, that is
# used to upload his video stream.
class ReqHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        args = self.path.split('/')
        args.pop(0)
        cmd = args.pop(0)
        if cmd == 'login':
            self.login(args)
            return
        self.send_response(200, "OK")
        self.ok('HELLO\n')
        pass

    def ok(self, msg):
        self.send_response(200, "OK")
        self.send_header("content-type", "text/plain")
        self.end_headers()
        self.wfile.write(msg)
        pass

    def err(self):
        self.send_response(500, "Error")
        self.send_header("content-type", "text/plain")
        self.end_headers()
        pass

    def change_client_ip(self, name, ip):
        self.log_message('client %s @ %s', name, ip)
        client_ip[name] = ip
        if not gst_clients.has_key(name):
            port = ul_ports[name]
            gst_clients[name] = gstserver.add_client(name, ip, port)
            pass
        pass

    def login(self, args):
        name = args[0]
        pwd = args[1]
        if pwds[name] == pwd:
            self.change_client_ip(name, self.client_address[0])
            port = ul_ports[name]
            self.ok('port=%d' % port)
        else:
            self.err()
            pass
        pass
    pass

def run():
    gstserver.init()

    address = ('', 8001)
    httpd = HTTPServer(address, ReqHandler)

    # Let glib to watch the socket for us.
    #
    # Call HTTPServer to serve one request when there is an incoming
    # connection, and return to main loop of glib immediately.
    def handle_http(*args):
        httpd.handle_request()
        # Add the socket to the watch list repeatly, or it will stop
        # watching it afterward.
        GObject.io_add_watch(httpd.socket.fileno(), GObject.IO_IN, handle_http)
        pass

    GObject.io_add_watch(httpd.socket.fileno(), GObject.IO_IN, handle_http)
    Gtk.main()
    pass

if __name__ == '__main__':
    run()
    pass
