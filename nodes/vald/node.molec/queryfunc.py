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

def addStates(transs,species):
    nstates=0
    for specie in species:
        subtranss = transs.filter(species=specie)
        sids = subtranss.values_list('upstate_id','lostate_id')
        sids = set(item for s in sids for item in s) # black magic
        nstates += len(sids)
        specie.States = State.objects.filter( pk__in = sids)
    return species, nstates

def getSpeciesWithStates(transs,addAtomStates,addMoleStates):
    log.debug('Entered getSpeciesWithStates(). Add states: %s %s'%(addAtomStates,addMoleStates))
    spids = transs.values_list('species_id',flat=True).distinct()
    spids = set(spids) # this is not to throw out duplicates but to evaluate the QuerySet, 
                       # otherwise it becomes slow due to false optimization.
    atoms = Species.objects.filter(pk__in=spids,ncomp=1)
    molecules = Species.objects.filter(pk__in=spids,ncomp__gt=1)
    nspecies = atoms.count() + molecules.count()
    nstates = 0
    if addAtomStates:
        atoms,nas = addStates(transs,atoms)
        nstates += nas
    if addMoleStates:
        molecules,nms = addStates(transs,molecules)
        nstates += nms

    return atoms,molecules,nspecies,nstates

def setupResults(sql):
    q = sql2Q(sql)
    log.debug('Just ran sql2Q(sql); setting up QuerySets now.')
    transs = Transition.objects.filter(q)
    ntranss=transs.count()
    if TRANSLIM < ntranss and (not sql.requestables or 'radiative' in sql.requestables):
        percentage = '%.1f'%(float(TRANSLIM)/ntranss *100)
        transs = transs.order_by('vacwave')
        newmax = transs[TRANSLIM].vacwave
        transs = Transition.objects.filter(q,Q(vacwave__lt=newmax))
        log.debug('Truncated results to %s, i.e %s A.'%(TRANSLIM,newmax))
    else: percentage=None
    ntranss=transs.count()
    log.debug('Transitions QuerySet set up. References next.')
    #refIDs = set( transs.values_list('wave_ref_id','loggf_ref_id','gammarad_ref_id','gammastark_ref_id','waals_ref') )
    #sources = Reference.objects.filter(pk__in=refIDs)
    sources = Reference.objects.all()
    log.debug('Sources QuerySet set up. References next.')

    addAtomStates = (not sql.requestables or 'atomstates' in sql.requestables)
    addMoleStates = (not sql.requestables or 'moleculestates' in sql.requestables)
    atoms,molecules,nspecies,nstates = getSpeciesWithStates(transs,addAtomStates,addMoleStates)

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

    log.debug('Returning from setupResults()')
    return {'RadTrans':transs,
            'Atoms':atoms,
            'Molecules':molecules,
            'Sources':sources,
            'HeaderInfo':headerinfo,
            'Environments':Environments #this is set up statically in models.py
           }

# The old way of getting references via linelists.
#def getRefs(transs):
#    llids=set()
#    for t in transs.values_list('wave_ref_id','loggf_ref_id','gammarad_ref_id','gammastark_ref_id','waals_ref'):
#        llids = llids.union(t)
#    lls=LineList.objects.filter(pk__in=llids)
#    rids=set()
#    for ll in lls:
#        rids=rids.union(ll.references.values_list('pk',flat=True))
#    return Reference.objects.filter(pk__in=rids)


