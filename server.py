#!/usr/bin/env python

from SimpleHTTPServer import SimpleHTTPRequestHandler, BaseHTTPServer
from cgi import parse_qs as parse

class MyHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        length= int( self.headers['content-length'] )
        data=self.rfile.read( length )
        data=parse(data)
        self.log_message("""post data is: %s"""%str(data))
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        for key in data.keys():
            self.wfile.write('%s: %s\n'%(key,data[key][0]))
        
    def do_GET(self):
        self.send_response(404)
        

def main():
    try:
        server = BaseHTTPServer.HTTPServer(('', 8080), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()
