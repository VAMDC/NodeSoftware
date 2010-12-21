# -*- coding: utf-8 -*-
from django.db.models import Q
from django.conf import settings
from dictionaries import *

import sys
def LOG(s):
    if settings.DEBUG: print >> sys.stderr, s

from models import *
from vamdctap.sqlparse import *

def getVALDsources(transs):
    sids=set([])
    for trans in transs:
        s=set([trans.wave_ref,trans.loggf_ref,trans.lande_ref,trans.gammarad_ref,trans.gammastark_ref,trans.waals_ref])
        sids=sids.union(s)
    return Source.objects.filter(pk__in=sids)

def getVALDstates(transs):
    
    #solution 1
    #q1,q2=Q(isupperstate_trans__in=transs),Q(islowerstate_trans__in=transs)
    #return State.objects.filter(q1|q2).distinct()

    # solution 2
    #lostates=State.objects.filter(islowerstate_trans__in=transs)
    #histates=State.objects.filter(isupperstate_trans__in=transs)
    #states = lostates | histates
    #return states.distinct()

    #solution 3, similar to sources
    sids=set([])
    for trans in transs:
        s=set([trans.upstate.pk,trans.lostate.pk])
        sids=sids.union(s)
    return State.objects.filter(pk__in=sids)
   

def setupResults(sql,limit=1000):
    LOG(sql)
    q=where2q(sql.where,RESTRICTABLES)
    try: q=eval(q)
    except: return {}
    
    transs = Transition.objects.select_related(depth=2).filter(q)
    ntranss=transs.count()

    if limit < ntranss :
        transs = transs[:limit]
        percentage='%.1f'%(float(limit)/ntranss *100)
    else: percentage=None

    sources = getVALDsources(transs)
    nsources = sources.count()
    states = getVALDstates(transs)
    nstates = states.count()
    nspecies = transs.values('species').distinct().count()

    # in order to not forget it:
    # write a small function that defines/fixes the
    # string representation of the wavelengths which
    # should have 8 significant dicits, i.e. variable
    # number of decimals.
    # maybe this can be achieved in the model itself.

    headerinfo=CaselessDict({\
            'Truncated':'%s %%'%percentage,
            'COUNT-SOURCES':nsources,
            'COUNT-species':nspecies,
            'count-states':nstates,
            'count-radiative':ntranss
            })
            

    return {'RadTrans':transs,
            'AtomStates':states,
            'Sources':sources,
            'HeaderInfo':headerinfo
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


