from httplib import HTTPConnection

import gstclient

# Login to the server and return the port number assigned by the
# server.
def get_login(host, port, name, pwd):
    conn = HTTPConnection(host, port)
    conn.request('GET', '/login/%s/%s' % (name, pwd))
    res = conn.getresponse()
    if res.status != 200:
        return
    data = res.read()
    firstline = data.split('\n')[0]
    name, value = firstline.split('=')
    assert name == 'port'
    return int(value)

if __name__ == '__main__':
    import sys
    assert len(sys.argv) == 5
    host, port, name, pwd = tuple(sys.argv[1:])
    port = get_login(host, port, name, pwd)
    if port:
        print 'Port number is %d' % port
        gstclient.init()
        client = gstclient.build_client(host, port)
        gstclient.run()
    else:
        print 'Error'
        pass
    pass
