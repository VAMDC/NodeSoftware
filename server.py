#!/usr/bin/env python

from SimpleHTTPServer import SimpleHTTPRequestHandler, BaseHTTPServer
import cgi

class MyHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        print ctype,pdict
        try:
            query=cgi.parse_multipart(self.rfile, pdict)
            print query
        except: print 'nope'
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write('test')
        return

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
