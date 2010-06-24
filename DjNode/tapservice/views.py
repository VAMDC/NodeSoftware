# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext, Context, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q

# Get the node-specific pacakge!
from django.conf import settings
from django.utils.importlib import import_module
NODEPKG=import_module(settings.NODEPKG+'.views')

from time import time
from datetime import date
from string import lower
import gzip
from cStringIO import StringIO
import threading
import os, math, sys
from base64 import b64encode
randStr = lambda n: b64encode(os.urandom(int(math.ceil(0.75*n))))[:n]

# deploying in apache/wsgi does not like plain "print" to stdout
# so use LOG() instead
# at some point we might want to use the "logging" module
def LOG(s):
    print >> sys.stderr, s


# import helper modules that reside in the same directory
from generators import *
from sqlparse import SQL

class TAPQUERY(object):
    def __init__(self,data):
        try:
            self.request=lower(data['REQUEST'])
            self.lang=lower(data['LANG'])
            self.query=data['QUERY']
            self.format=lower(data['FORMAT'])
            self.isvalid=True
        except:
            self.isvalid=False

        if self.isvalid: self.validate()
        if self.isvalid: self.assignQID()
	#if self.isvalid: self.makeQtup()
        if self.isvalid: self.parseSQL()

    def validate(self):
        """
        overwrite this method for
        custom checks, depending on data set
        """

    def parseSQL(self):
        self.parsedSQL=SQL.parseString(self.query)

#    def makeQtup(self):
#        query=self.query%NODEPKG.VAMDC_DICT
#        self.qtup=vamdc2queryset(query)

    def assignQID(self):
        """ make a query-id """
        self.queryid='%s-%s'%(date.today().isoformat(),randStr(8))

    def __str__(self):
        return '%s'%self.query

def sync(request):
    tap=TAPQUERY(request.REQUEST)
    if not tap.isvalid:
        # return http error
        LOG('not valid tap!')
    
    if tap.format == 'xsams': 
        results=NODEPKG.setupResults(tap.parsedSQL)
        generator=Xsams(**results)
        response=HttpResponse(generator,mimetype='text/xml')
        #response['Content-Disposition'] = 'attachment; filename=%s.%s'%(tap.queryid,tap.format)
    
    elif tap.format == 'votable': 
        transs,states,sources=NODEPKG.setupResults(tap)
        generator=votable(transs,states,sources)
        response=HttpResponse(generator,mimetype='text/xml')
        #response['Content-Disposition'] = 'attachment; filename=%s.%s'%(tap.queryid,tap.format)
    
#    elif tap.format == 'embedhtml':
#        transs,states,sources,count=NODEPKG.setupResults(tap,limit=100)
#        generator=embedhtml(transs,count)
#        xml='\n'.join(generator)
#        #open('/tmp/bla.xml','w').write(xml)
#        html=vo2html(E.fromstring(xml))
#        response=HttpResponse(html,mimetype='text/html')

    return response



def async(request):
    c=RequestContext(request,{})
    return render_to_response('node/index.html', c)

def capabilities(request):
    c=RequestContext(request,{})
    return render_to_response('node/index.html', c)

def tables(request):
    c=RequestContext(request,{})
    return render_to_response('node/index.html', c)

def availability(request):
    c=RequestContext(request,{})
    return render_to_response('node/index.html', c)

def index(request):
    c=RequestContext(request,{})
    return render_to_response('node/index.html', c)










#############################################################     
############### LEGACY code below ###########################
#############################################################


class RenderThread(threading.Thread):
    def __init__(self, t,c):
        threading.Thread.__init__(self)
        self.t = t
        self.c = c
    def run(self):
        self.r=self.t.render(self.c)


def RenderXSAMSmulti(format,transs,states,sources):
    # this turned out to be inefficient
    # due to large overhead of python threads
    n=int(transs.count()/3)
    trans1=transs[:n]
    trans2=transs[n:2*n]
    trans3=transs[2*n:]
    t1=loader.get_template('vald/valdxsams_p1.xml')
    t2=loader.get_template('vald/valdxsams_p2.xml')
    th1=RenderThread(t1,Context({'sources':sources,'states':states,}))
    th2=RenderThread(t2,Context({'transitions':trans1}))
    th3=RenderThread(t2,Context({'transitions':trans2}))
    th4=RenderThread(t2,Context({'transitions':trans3}))
    th1.start()
    th2.start()
    th3.start()
    th4.start()
    th1.join()
    th2.join()
    th3.join()
    th4.join()
    rend=th1.r + th2.r + th3.r + th4.r + u'\n</XSAMSData>'
    return rend

def RenderXSAMSsingle(format,transs,states,sources):
    c=Context({'transitions':transs,'sources':sources,'states':states,})
    t=loader.get_template('vald/valdxsams.xml')
    return t.render(c)


def MyRender(format,transs,states,sources):
    if format=='xsams':
        rend=RenderXSAMSsingle(format,transs,states,sources)
    elif format=='csv': 
        t=loader.get_template('vald/valdtable.csv')
        c=Context({'transitions':transs,'sources':sources,'states':states,})
        rend=t.render(c)
    else: 
        rend=''   
    return rend

def renderedResponse(transs,states,sources,tap):
    rendered=MyRender(tap.format,transs,states,sources)
    
    zbuf = StringIO()
    zfile = gzip.GzipFile(mode='wb', compresslevel=6, fileobj=zbuf)
    zfile.write(rendered)
    zfile.close()
    compressed_content = zbuf.getvalue()
    response = HttpResponse(compressed_content,mimetype='application/x-gzip')
    response['Content-Encoding'] = 'gzip'
    response['Content-Length'] = str(len(compressed_content))
    response['Content-Disposition'] = 'attachment; filename=%s.%s.gz'%(tap.queryid,tap.format)
    return response
    


