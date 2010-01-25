#!/usr/bin/env python

from SimpleHTTPServer import SimpleHTTPRequestHandler, BaseHTTPServer
from cgi import parse_qsl as parse
import simplejson as j
from sqlite3 import dbapi2 as sqlite
import string as s

#DBNAME='merged.db'
DBNAME='dummy.db'
conn=sqlite.connect(DBNAME)
curs=conn.cursor()

def runquery(query):
    wher,ord,cols,tab=('',)*4
    for quer in query:
        if quer[0]=='table':
            tab=quer[1]
        elif quer[0]=='where':
            wher=quer[1]
        elif quer[0]=='order':
            ord=quer[1]
        elif quer[0]=='columns':
            if quer[1]=='*':
                print ' star not implemented '
                continue
            cols=quer[1]
            cols=map(s.strip,s.split(cols,','))
        else:
            continue
    if not (tab and cols): return {}

    query='SELECT %s FROM %s'%(s.join(cols,','),tab)
    if wher:
        query+=' WHERE (%s)'%wher
    if ord:
        query+=' ORDER BY (%s)'%ord

    try:
        curs.execute(query+';')
    except sqlite.OperationalError:
        print 'OperationalError: probably an unknown column or table name given'
    data=curs.fetchall()
    ndata=[]
    for dat in data:
        d={}
        for i,col in enumerate(cols):
            d[col]=dat[i]
        ndata.append(d)
    return ndata

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
        quer=self.rfile.read( length )
        quer=parse(quer)
        self.log_message("""post data is: %s"""%str(quer))
        self.send_response(200)
        #self.send_header('Content-type','text/html')
        self.send_header('Content-type','application/json')
        self.end_headers()
        
        j.dump(runquery(quer),self.wfile)
        
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
