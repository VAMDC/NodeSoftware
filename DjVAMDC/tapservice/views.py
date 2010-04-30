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

def index(request):
    c=RequestContext(request,{})
    return render_to_response('node/index.html', c)

class TAPQUERY(object):
    def __init__(self,data):
        try:
            self.request=lower(data['REQUEST'])
            self.lang=lower(data['LANG'])
            self.query=lower(data['QUERY'])
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
    sql=sql.lower().replace('(','').replace(')','')
    wheres=sql.split('where')[-1].split('and') # replace this with http://code.google.com/p/python-sqlparse/ later
    qlist=[]
    for w in wheres:
        w=w.split()
        field=w[0]
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
            

class RenderThread(threading.Thread):
    def __init__(self, t,c):
        threading.Thread.__init__(self)
        self.t = t
        self.c = c
    def run(self):
        self.r=self.t.render(self.c)
        

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
