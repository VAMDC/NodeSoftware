#!/usr/bin/env python
"""

simple.py

Very basic proof-of-concept implementation of a webserver that
answers a data query that it gets via a HTTP POST request by handing
it to a SQLite database and sending the data back.

"""

from SimpleHTTPServer import SimpleHTTPRequestHandler, BaseHTTPServer
from cgi import parse_qsl as parse
import simplejson as j
from sqlite3 import dbapi2 as sqlite
import string as s
from sys import argv,exit



class MyHandler(SimpleHTTPRequestHandler):
    """
        The class that gets bound to the webserver
    """
    
    def do_POST(self):
        """
            handle POST requests, pepending on the URL.
        """
        if self.path=='/query':
            self.answer_query()
        elif self.path=='/registry':
            self.answer_registry()
        else:
            self.e404()

    def e404(self):
        """
            a proper 404 reply for unknown requests
        """
        self.send_response(404)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write('Error 404')

    def answer_registry(self):
        """ 
           answer a registry request. not yet implemented.
        """
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write('to be implemented')
        
    def answer_query(self):
        """
            answer data query by parsing the request, 
            handing it to runquery() and sending the
            json-encoded data back.
        """
        length= int( self.headers['content-length'] )
        quer=self.rfile.read( length )
        self.quer=parse(quer)
        self.log_message("""post data is: %s"""%str(self.quer))
        self.send_response(200)
        #self.send_header('Content-type','text/html')
        self.send_header('Content-type','application/json')
        self.end_headers()
        
        j.dump(self.runquery(),self.wfile)
        
    def do_GET(self):
        """
           GET requests are not wanted.
        """
        self.e404()

    def runquery(self):
        """ Takes the list with the parsed request and constructs
            the SQL query from it, then runs it. Returns the data
            together with the column names.
        """
        wher,ord,cols,tab=('',)*4
        for quer in self.quer:
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

        print query
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

        

def run(argv):
    """
        connect to the DB and start the server
    """
    global curs

    if len(argv) > 1:
        DBNAME=argv[1]
    else:
        DBNAME='dummy.db'

    try:
        conn=sqlite.connect(DBNAME)
        curs=conn.cursor()
        print 'bound to %s'%DBNAME
    except:
        print 'Error in opening the database: %s'%argv[1]
        exit(1)

    try:
        server = BaseHTTPServer.HTTPServer(('', 8080), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    run(argv)
