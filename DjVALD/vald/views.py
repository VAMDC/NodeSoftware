# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,get_object_or_404
from django.db.models import Q
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

from DjVALD.vald.models import Transition,State,Source,Species

from base64 import b64encode as b64
def enc(s):
    return b64(s).replace('=','')

import sys
def LOG(s):
    print >> sys.stderr, s

#from lxml import etree as E
#vo2html=E.XSLT(E.parse(open(settings.BASEPATH+'DjNode/static/xsl/VOTable2XHTML_mine.xsl')))


RETURNABLES={\
'SourceID':'Source.id',
'SourceAuthorName':'Source.srcdescr',
'SourceCategory':'journal',
'SourcePageBegin':'',
'SourcePageEnd':'',
'SourceName':'',
'SourceTitle':'',
'SourceURI':'',
'SourceVolume':'',
'SourceYear':'2222',
'MethodID':'OBS',
'MethodCategory':'observed',
'MethodDescription':'so far all vald data is marked as observed although that is not necessarily true :)',
'AtomStateID':'AtomState.id',
'AtomSymbol':'AtomState.species.name',
'AtomNuclearCharge':'AtomState.species.atomic',
'AtomConfigurationLabel':'AtomState.charid',
'AtomCompositionComponentTerm':'AtomState.term',
'AtomIonizationEnergy':'AtomState.species.ionen',
'AtomLandeFactor':'AtomState.coupling',
'AtomStateEnergy':'AtomState.energy',
'AtomIonCharge':'AtomState.species.ion',
'AtomMassNumber':'AtomState.species.massno',
'RadTransComments':'Wavelength is for vaccum.',
'RadTransWavelengthExperimentalValue':'RadTran.vacwave',
'RadTransWavelengthExperimentalUnits':'Angstrom',
'RadTransWavelengthExperimentalAccuracy':'RadTran.accur',
'RadTransWavelengthExperimentalSourceRef':'RadTran.wave_ref',
'RadTransFinalStateRef':'RadTran.lostate.id',
'RadTransInitialStateRef':'RadTran.upstate.id',
'RadTransLogGF':'RadTran.loggf',
'RadTransMethodRef':'OBS',
'RadTransProbabilityLog10WeightedOscillatorStrengthSourceRef':'RadTran.loggf_ref',
'RadTransProbabilityLog10WeightedOscillatorStrengthValue':'RadTran.loggf',
}

RESTRICTABLES = {\
'AtomSymbol':'species__name',
'AtomNuclearCharge':'species__atomic',
'AtomStateEnergy':'upstate__energy',
'RadTransWavelengthExperimentalValue':'vacwave',
'RadTransLogGF':'loggf',
'AtomIonCharge':'species__ion',
}

OPTRANS= {\
    '<':  '__lt',
    '>':  '__gt',
    '=':  '__exact',
    '<=': '__lte',
    '>=': '__gte',
    'in': '__in',
}
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
    lostates=State.objects.filter(islowerstate_trans__in=transs).distinct()
    histates=State.objects.filter(islowerstate_trans__in=transs).distinct()
    states = lostates | histates
    return states
    

def singleWhere(w):
    if not RESTRICTABLES.has_key(w[0]): return
    if not OPTRANS.has_key(w[1]): return
    return 'Q(%s=%s)'%(RESTRICTABLES[w[0]] + OPTRANS[w[1]],w[2])

def where2q(ws):
    q=''
    for w in ws:
        if w=='and': q+=' & '
        elif w=='or': q+=' | '
        elif len(w)==3: q+=singleWhere(w)
        elif w[0]=='(' and w[-1]==')':
            q+=sql2q(w[1:-1])
        LOG(q)

    return q

def setupResults(sql,limit=0):
    LOG(sql)
    q=where2q(sql.where)
    try: q=eval(q)
    except: pass
    
    transs = Transition.objects.filter(q)
    
    totalcount=transs.count()
    if limit :
        transs = transs[:limit]

    sources = getVALDsources(transs)
    states = getVALDstates(transs)
    return {'RadTrans':transs,
            'AtomStates':states,
            'Sources':sources,
           }







#############################################################     
############### LEGACY code below ###########################
#############################################################





def getVALDstates2(transs):
    sids=set([])
    for trans in transs:
        sids.add(trans.lostate)
        sids.add(trans.upstate)
        
    states=[]
    sids.remove(None)
    for sid in sids:
        states.append(State.objects.get(pk=sid))
    return states

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
    #resonably fast
    waverefs=Q(iswaveref_trans__in=transs)
    landerefs=Q(islanderef_trans__in=transs)
    loggfrefs=Q(isloggfref_trans__in=transs)
    g1refs=Q(isgammaradref_trans__in=transs)
    g2refs=Q(isgammastarkref_trans__in=transs)
    g3refs=Q(isgammawaalsref_trans__in=transs)
    refQs=[waverefs, landerefs, loggfrefs, g1refs, g2refs, g3refs]
    sources=set()
    for q in refQs:
        refs=Source.objects.filter(q).distinct()
        for r in refs:
            sources.add(r)
    return sources

def getVALDsources3(transs):
    # slower than v2
    sids=set([])
    for trans in transs:
        s=set([trans.wave_ref,trans.loggf_ref,trans.lande_ref,trans.gammarad_ref,trans.gammastark_ref,trans.gammawaals_ref])
        sids=sids.union(s)
    return list(sids)

def getVALDsources4(transs):
    # as slow as v3
    sids=set([])
    for trans in transs:
        s=set([trans.wave_ref.id,trans.loggf_ref.id,trans.lande_ref.id,trans.gammarad_ref.id,trans.gammastark_ref.id,trans.gammawaals_ref.id])
        sids=sids.union(s)
    sources=[]
    for sid in sids:
        sources.append(Source.objects.get(pk=sid))
    return sources


