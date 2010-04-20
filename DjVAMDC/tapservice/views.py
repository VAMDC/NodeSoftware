from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from DjVAMDC.vald.models import Transitions,States,Sources

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
            self.valid=True
        except:
            self.valid=False
        
    def __str__(self):
        return '%s'%self.query

def sync(request):
    if request.POST:
        data = request.POST
    elif request.GET:
        data = request.GET
    else: data = None
    tap=TAPQUERY(data)
    if tap.valid:
        wheres=tap.query.split('WHERE')[1].split('AND') # replace this with http://code.google.com/p/python-sqlparse/ later
        for w in map(lower,wheres):
            if 'wavelength' in w:
                if '<' in w:
                    waveq=Q
        wavebord=85
        transs=Transitions.objects.filter(vacwave__lt=wavebord)
        states=transs.lostate.object.all()
        #states=States.objects.filter(islowerstate_trans__vacwave__lt=wavebord).distinct()
        #sources=Sources.objects.filter(iswaveref_trans__vacwave__lt=wavebord).distinct()
        print time()
        print len(transs),len(states),len(sources)
        print time()
        c=RequestContext(request,{'transitions':transs,
                                  'sources':sources,
                                  'states':states,
                                  })
        t=loader.get_template('vald/valdxsams.xml')
        r=t.render(c)
        print time()
        return HttpResponse(r)
        #return render_to_response('vald/valdxsams.xml', c) # shortcut
    else:
        c=RequestContext(request,{})
        return render_to_response('node/index.html', c)

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
