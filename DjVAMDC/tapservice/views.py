from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext, Context, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from DjVAMDC.vald.models import Transition,State,Source,Species

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
            self.request=data['REQUEST']
            self.lang=data['LANG']
            self.query=data['QUERY']
            self.format=data['FORMAT']
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
    wheres=sql.split('WHERE')[1].split('AND') # replace this with http://code.google.com/p/python-sqlparse/ later
    qlist=[]
    for w in map(lower,wheres):
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
            

def getVALDsources1(transs):
    # this is REALLY slow
    waverefs=Q(iswaveref_trans__in=transs)
    landerefs=Q(islanderef_trans__in=transs)
    loggfrefs=Q(isloggfref_trans__in=transs)
    g1refs=Q(isgammaradref_trans__in=transs)
    g2refs=Q(isgammastarkref_trans__in=transs)
    g3refs=Q(isgammawaalsref_trans__in=transs)
    refQ= waverefs | landerefs | loggfrefs | g1refs | g2refs | g3refs
    sources=Source.objects.filter(refQ).distinct()
    return sources

def getVALDsources2(transs):
    waverefs=Q(iswaveref_trans__in=transs)
    landerefs=Q(islanderef_trans__in=transs)
    loggfrefs=Q(isloggfref_trans__in=transs)
    g1refs=Q(isgammaradref_trans__in=transs)
    g2refs=Q(isgammastarkref_trans__in=transs)
    g3refs=Q(isgammawaalsref_trans__in=transs)
    refQs=[waverefs, landerefs, loggfrefs, g1refs, g2refs, g3refs]
    sources=set()
    for q in refQs:
        refs=Source.objects.filter(q)
        for r in refs:
            sources.add(r)
    return sources

def getVALDsources3(transs):
    sids=set([])
    for trans in transs:
        s=set([trans.wave_ref,trans.loggf_ref,trans.lande_ref,trans.gammarad_ref,trans.gammastark_ref,trans.gammawaals_ref])
        sids=sids.union(s)
    return list(sids)

def getVALDsources4(transs):
    sids=set([])
    for trans in transs:
        s=set([trans.wave_ref.id,trans.loggf_ref.id,trans.lande_ref.id,trans.gammarad_ref.id,trans.gammastark_ref.id,trans.gammawaals_ref.id])
        sids=sids.union(s)
    sources=[]
    for sid in sids:
        sources.append(Source.objects.get(pk=sid))
    return sources

def getVALDsources5(transs):
    sids=set([])
    for trans in transs:
        s=set([trans.wave_ref,trans.loggf_ref,trans.lande_ref,trans.gammarad_ref,trans.gammastark_ref,trans.gammawaals_ref])
        sids=sids.union(s)
    sources=[]
    for sid in sids:
        sources.append(Source.objects.get(pk=sid))
    return sources

def getVALDstates1(transs):
    lostates=State.objects.filter(islowerstate_trans__in=transs)
    histates=State.objects.filter(islowerstate_trans__in=transs)
    states = lostates | histates
    return states.distinct()
    

def getVALDstates2(transs):
    sids=set([])
    for trans in transs:
        s=set([trans.lostate,trans.upstate])
        sids=sids.union(s)
    states=[]
    for sid in sids:
        states.append(State.objects.get(pk=sid))
    return states

class RenderThread(threading.Thread):
    def __init__(self, t,c):
        threading.Thread.__init__(self)
        self.t = t
        self.c = c
    def run(self):
        self.r=self.t.render(self.c)
        

def MyRender(format,transs,states,sources):
    if format.lower()=='xsams':
        rend=RenderXSAMSmulti(format,transs,states,sources)
    elif format.lower()=='csv': 
        t=loader.get_template('vald/valdtable.csv')
        c=Context({'transitions':transs,'sources':sources,'states':states,})
        rend=t.render(c)
    else: 
        rend=''   
    return rend


def RenderXSAMSmulti(format,transs,states,sources):
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
    t1=loader.get_template('vald/valdxsams_p1.xml')
    t2=loader.get_template('vald/valdxsams_p2.xml')
    r1=t1.render(c)
    r2=t2.render(c)
    rend=r1+r2+ u'\n</XSAMSData>'
    return rend

def sync(request):
    tap=TAPQUERY(request.REQUEST)
    if not tap.isvalid:
        # return http error
        pass

    qtup=parseSQL(tap.query)
    
    ts=time()

    transs=Transition.objects.filter(*qtup)
    #print '%d transitions set up'%len(transs),time()-ts
    
    states = getVALDstates2(transs)
    #print '%d states set up'%len(states),time()-ts
    
    sources=getVALDsources5(transs)
    #print '%d sources set up'%len(sources),time()-ts
       

    print 'starting rendering',time()-ts
    rendered=MyRender(tap.format,transs,states,sources)
    print 'multi render ended:',time()-ts

    zbuf = StringIO()
    zfile = gzip.GzipFile(mode='wb', compresslevel=6, fileobj=zbuf)
    zfile.write(rendered)
    zfile.close()
    compressed_content = zbuf.getvalue()
    response = HttpResponse(compressed_content,mimetype='application/x-gzip')
    response['Content-Encoding'] = 'gzip'
    response['Content-Length'] = str(len(compressed_content))
    response['Content-Disposition'] = 'attachment; filename=%s%s.gz'%(tap.queryid,tap.format)
    return response
        #return render_to_response('vald/valdxsams.xml', c) # shortcut

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


def compressedview(request):
    zbuf = cStringIO.StringIO()
    zfile = gzip.GzipFile(mode='wb', compresslevel=6, fileobj=zbuf)
    zfile.write(template.render(context).encode('utf-8'))
    zfile.close()
    
    compressed_content = zbuf.getvalue()
    response = HttpResponse(compressed_content)
    response['Content-Encoding'] = 'gzip'
    response['Content-Length'] = str(len(compressed_content))
    return response
