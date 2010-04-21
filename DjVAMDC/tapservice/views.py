from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from DjVAMDC.vald.models import Transition,State,Source,Species

from django.db.models import Q

from time import time
from string import lower

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
    def validate(self):
        """
        overwrite this method for
        custom checks, depending on data set
        """

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

def sync(request):
    tap=TAPQUERY(request.REQUEST)
    if not tap.isvalid:
        # return http error
        pass

    qtup=parseSQL(tap.query)
    
    ts=time()

    transs=Transition.objects.filter(*qtup)
    print '%d transitions set up'%len(transs),time()-ts
    
    lostates=State.objects.filter(islowerstate_trans__in=transs)
    histates=State.objects.filter(islowerstate_trans__in=transs)
    states = lostates | histates
    states = states.distinct()
    print '%d states set up'%len(states),time()-ts
    
    sources=getVALDsources4(transs)
    print '%d sources set up'%len(sources),time()-ts
        

    if tap.format.lower()=='xsams': template='vald/valdxsams.xml'
    elif tap.format.lower()=='csv': template='vald/valdtable.csv'
    else: template='index.html'
    
    c=RequestContext(request,{'transitions':transs,
                              'sources':sources,
                              'states':states,
                              })
    t=loader.get_template(template)
    print 'starting render',time()-ts
    r=t.render(c)
    print 'render ended:',time()-ts
    return HttpResponse(r)
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
