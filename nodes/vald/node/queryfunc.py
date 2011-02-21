# -*- coding: utf-8 -*-
from django.db.models import Q
from django.conf import settings
from dictionaries import *
from itertools import chain
from copy import deepcopy

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

def setupResults(sql,limit=10000):
    LOG(sql)
    q=where2q(sql.where,RESTRICTABLES)
    try: q=eval(q)
    except: return {}
    
    transs = Transition.objects.filter(q)
#    transs = Transition.objects.select_related(depth=2).filter(q)
    ntranss=transs.count()

    sources = getRefs(transs)
    nsources = sources.count()
    species,nspecies,nstates = getSpeciesWithStates(transs)

    if limit < ntranss :
        transs = transs[:limit]
        percentage='%.1f'%(float(limit)/ntranss *100)
    else: percentage=None

    
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
