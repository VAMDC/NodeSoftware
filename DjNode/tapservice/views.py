from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext, Context, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q

from time import time
from datetime import date
from string import lower
import gzip
from cStringIO import StringIO
import threading
import os, math
from base64 import b64encode
randStr = lambda n: b64encode(os.urandom(int(math.ceil(0.75*n))))[:n]

from DjNode.tapservice.generators import *

def parseSQL(sql):
    wheres=sql.split('where')[1].split('and') # replace this with http://code.google.com/p/python-sqlparse/ later
    qlist=[]
    for w in wheres:
        w=w.split()
        print w
        value=w[-1]
        if 'wavelength' in w: field='vacwave'
        if 'element' in w: field='species__name'
        if '<' in w: op='__lt'
        if '>' in w: op='__gt'
        if '=' in w: op='__iexact'
        if '<=' in w: op='__lte'
        if '>=' in w: op='__gte'
        
        exec('mq=Q(%s="%s")'%(field+op,value))
        qlist.append(mq)
    return tuple(qlist)

def vamdc2queryset(sql):
    sql=sql.replace('(','').replace(')','')
    wheres=sql.split('where')[-1].split('and') # replace this with http://code.google.com/p/python-sqlparse/ later
    qlist=[]
    for w in wheres:
        w=w.split()
        field=w[0].replace('.','__')
        value=w[2]
        if w[1]=='<': op='__lt'
        if w[1]=='>': op='__gt'
        if w[1]=='=': op='__exact'
        if w[1]=='<=': op='__lte'
        if w[1]=='>=': op='__gte'
        qexe='mq=Q(%s="%s")'%(field+op,value)
        print qexe
        exec(qexe)
        qlist.append(mq)
    return tuple(qlist)

from DjVALD.vald.views import setupResults

def index(request):
    c=RequestContext(request,{})
    return render_to_response('node/index.html', c)

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
    def validate(self):
        """
        overwrite this method for
        custom checks, depending on data set
        """

    def assignQID(self):
        """ make a query-id """
        self.queryid='%s-%s'%(date.today().isoformat(),randStr(8))

    def __str__(self):
        return '%s'%self.query


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


#####################################3

def sync(request):
    tap=TAPQUERY(request.REQUEST)
    if not tap.isvalid:
        # return http error
        print 'not valid tap!'
    
    if tap.format == 'xsams': 
        results=setupResults(tap)
        generator=Xsams(**results)
        response=HttpResponse(generator,mimetype='application/xml')
        response['Content-Disposition'] = 'attachment; filename=%s.%s'%(tap.queryid,tap.format)
    
    elif tap.format == 'votable': 
        transs,states,sources=setupResults(tap)
        generator=votable(transs,states,sources)
        response=HttpResponse(generator,mimetype='application/xml')
        response['Content-Disposition'] = 'attachment; filename=%s.%s'%(tap.queryid,tap.format)
    
    elif tap.format == 'embedhtml':
        transs,states,sources,count=setupResults(tap,limit=100)
        generator=embedhtml(transs,count)
        xml='\n'.join(generator)
        #open('/tmp/bla.xml','w').write(xml)
        html=vo2html(E.fromstring(xml))
        response=HttpResponse(html,mimetype='text/html')

    return response







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
    


