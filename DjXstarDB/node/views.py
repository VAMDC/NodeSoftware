# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,get_object_or_404
from django.db.models import Q
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

from DjXstarDB.node.models import *

from base64 import b64encode as b64
def enc(s):
    return b64(s).replace('=','')

import sys
def LOG(s):
    print >> sys.stderr, s

RESTRICTABLES = {\
'AtomIonCharge' : 'Ions.charge',
'AtomSymbol' : 'Elements.sym',
'AtomNuclearCharge' : 'Elements.z',
'AtomStateEnergy' : 'Levels.energy'
}
RETURNABLES = {\
'AtomIonCharge' : 'Ions.charge',
'AtomNuclearCharge' : 'Elements.z',
'AtomSymbol' : 'Elements.sym',
'AtomMassNumber' : 'Elements.mass',
'AtomStateEnergy' : 'Levels.energy',
'AtomStateDescription' : 'Levels.label'
}


from DjNode.tapservice.sqlparse import *


def index(request):
    c=RequestContext(request,{})
    return render_to_response('vald/index.html', c)


def getVALDsources(transs):
    sids=set([])
    for trans in transs:
        s=set([trans.wave_ref,trans.loggf_ref,trans.lande_ref,trans.gammarad_ref,trans.gammastark_ref,trans.gammawaals_ref])
        sids=sids.union(s)
    return Source.objects.filter(pk__in=sids)

def getVALDstates(transs):
    #q1,q2=Q(isupperstate_trans__in=transs),Q(islowerstate_trans__in=transs)
    #return State.objects.filter(q1|q2).distinct()
    lostates=State.objects.filter(islowerstate_trans__in=transs)
    histates=State.objects.filter(islowerstate_trans__in=transs)
    states = lostates | histates
    return states.distinct()
    

def setupResults(sql,limit=0):
    LOG(sql)
    q=where2q(sql.where,RESTRICTABLES)
    try: q=eval(q)
    except: return {}
    
    transs = Transition.objects.select_related(depth=2).filter(q)
    
    totalcount=transs.count()
    if limit :
        transs = transs[:limit]

    sources = getVALDsources(transs)
    states = getVALDstates(transs)
    return {'RadTrans':transs,
            'AtomStates':states,
            'Sources':sources,
           }

