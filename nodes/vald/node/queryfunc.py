# -*- coding: utf-8 -*-
from django.db.models import Q
from django.conf import settings
import sys

import logging
log=logging.getLogger('vamdc.node.queryfu')

from dictionaries import *
from itertools import chain
from copy import deepcopy

from models import *
from vamdctap.sqlparse import *

if hasattr(settings,'TRANSLIM'):
    TRANSLIM = settings.TRANSLIM
else: TRANSLIM = 5000

def getRefs(transs):
    llids=set()
    for t in transs.values_list('wave_ref_id','loggf_ref_id','gammarad_ref_id','gammastark_ref_id','waals_ref'):
        llids = llids.union(t)
    lls=LineList.objects.filter(pk__in=llids)
    rids=set()
    for ll in lls:
        rids=rids.union(ll.references.values_list('pk',flat=True))
    return Reference.objects.filter(pk__in=rids)

def getSpeciesWithStates(transs):
    spids = set( transs.values_list('species_id',flat=True) )
    atoms = Species.objects.filter(pk__in=spids,ncomp=1)
    molecules = Species.objects.filter(pk__in=spids,ncomp__gt=1)
    nspecies = atoms.count() + molecules.count()
    nstates = 0
    for species in [atoms,molecules]:
        for specie in species:
            subtranss = transs.filter(species=specie)
            up=subtranss.values_list('upstate_id',flat=True)
            lo=subtranss.values_list('lostate_id',flat=True)
            sids = set(chain(up,lo))
            specie.States = State.objects.filter( pk__in = sids)
            nstates += len(sids)

    return atoms,molecules,nspecies,nstates

def setupResults(sql):
    q = sql2Q(sql)
    transs = Transition.objects.filter(q).order_by('vacwave')
    ntranss=transs.count()
    if TRANSLIM < ntranss and (not sql.requestables or 'radiative' in sql.requestables):
        percentage='%.1f'%(float(TRANSLIM)/ntranss *100)
        newmax=transs = transs[TRANSLIM].vacwave
        transs=Transition.objects.filter(q,Q(vacwave__lt=newmax))
    else: percentage=None
    ntranss=transs.count()
    sources = getRefs(transs)
    atoms,molecules,nspecies,nstates = getSpeciesWithStates(transs)

    if ntranss:
        size_estimate='%.2f'%(ntranss*0.0014 + 0.01)
    else: size_estimate='0.00'

    headerinfo={\
            'TRUNCATED':percentage,
            'COUNT-ATOMS':atoms.count(),
            'COUNT-MOLECULES':molecules.count(),
            'COUNT-STATES':nstates,
            'CoUNT-RADIATIVE':ntranss,
            'APPROX-SIZE':size_estimate,
            }

    return {'RadTrans':transs,
            'Atoms':atoms,
            'Molecules':molecules,
            'Sources':sources,
            'HeaderInfo':headerinfo,
            'Environments':Environments #this is set up statically in models.py
           }
