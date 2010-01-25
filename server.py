#!/usr/bin/env python

from SimpleHTTPServer import SimpleHTTPRequestHandler, BaseHTTPServer
from cgi import parse_qs as parse
import json

class MyHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        print self.path
        if self.path=='/query':
            self.answer_query()
        elif self.path=='/registry':
            self.answer_registry()
        else:
            self.e404()

    def e404(self):
        self.send_response(404)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write('Error 404')

    def answer_registry(self):
        """ response for the registry"""
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write('to be implemented')
        
    def answer_query(self):
        length= int( self.headers['content-length'] )
        data=self.rfile.read( length )
        data=parse(data)
        self.log_message("""post data is: %s"""%str(data))
        self.send_response(200)
        self.send_header('Content-type','text/html')
        #self.send_header('Content-type','application/json')
        self.end_headers()
        for key in data.keys():
            self.wfile.write('%s: %s\n'%(key,data[key][0]))
        
    def do_GET(self):
        self.e404()
        

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
