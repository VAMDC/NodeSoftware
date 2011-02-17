# -*- coding: utf-8 -*-
from django.db.models import Q
from django.conf import settings
from dictionaries import *
from itertools import chain

import sys
def LOG(s):
    if settings.DEBUG: print >> sys.stderr, s

from models import *
from vamdctap.sqlparse import *

def getRefs(transs):
    llids=set()
    for t in transs.values_list('wave_ref_id','loggf_ref_id','lande_ref_id','gammarad_ref_id','gammastark_ref_id','waals_ref'):
        llids = llids.union(t)
    lls=LineList.objects.filter(pk__in=llids)
    rids=set()
    for ll in lls:
        rids=rids.union(ll.references.values_list('pk',flat=True))
    return Reference.objects.filter(pk__in=rids)

def getSpeciesWithStates(transs):
    spids = set( transs.values_list('species_id',flat=True) )
    species = Species.objects.filter(pk__in=spids)
    nspecies = species.count()
    nstates = 0
    for specie in species:
        subtranss = transs.filter(species=specie)
        up=subtranss.values_list('upstate_id',flat=True)
        lo=subtranss.values_list('lostate_id',flat=True)
        sids = set(chain(up,lo))
        specie.States = State.objects.filter( pk__in = sids)
        nstates += len(sids)

    return species,nspecies,nstates

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
    #sids=set([])
    #for trans in transs:
    #    s=set([trans.upstate.pk,trans.lostate.pk])
    #    sids=sids.union(s)
    #return State.objects.filter(pk__in=sids)
   
    # solution 4
    up=transs.values_list('upstate_id',flat=True)
    lo=transs.values_list('lostate_id',flat=True)
    sids=set( chain(up,lo) )
    return State.objects.filter(pk__in=sids)


def setupResults(sql,limit=1000):
    LOG(sql)
    q=where2q(sql.where,RESTRICTABLES)
    try: q=eval(q)
    except: return {}
    
    transs = Transition.objects.select_related(depth=2).filter(q)
    ntranss=transs.count()

    if limit < ntranss :
#        transs = transs[:limit]
        percentage='%.1f'%(float(limit)/ntranss *100)
    else: percentage=None

    sources = getRefs(transs)
    nsources = sources.count()
    #states = getVALDstates(transs)
    #nstates = states.count()
    #nspecies = transs.values('species').distinct().count()
    species,nspecies,nstates = getSpeciesWithStates(transs)

    headerinfo=CaselessDict({\
            'Truncated':percentage,
            'COUNT-SOURCES':nsources,
            'COUNT-species':nspecies,
            'count-states':nstates,
            'count-radiative':ntranss
            })
            

    return {'RadTrans':transs,
            'Atoms':species,
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


