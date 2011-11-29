# -*- coding: utf-8 -*-
from django.db.models import Q
from django.conf import settings
import sys

import logging
log=logging.getLogger('vamdc.node.queryfu')

from itertools import chain
from copy import deepcopy

from vamdctap.sqlparse import *

if hasattr(settings,'TRANSLIM'):
    TRANSLIM = settings.TRANSLIM
else: TRANSLIM = 5000

def addStates(transs,species,StateModel):
    nstates=0
    for specie in species:
        subtranss = transs.filter(species=specie)
        sids = subtranss.values_list('upstate_id','lostate_id')
        sids = set(item for s in sids for item in s) # black magic
        nstates += len(sids)
        specie.States = StateModel.objects.filter( pk__in = sids)
    return species, nstates

def getSpeciesWithStates(transs,SpeciesModel,StateModel,addStates):
    log.debug('Entered getSpeciesWithStates(). Add states: %s'%(addStates,))
    spids = transs.values_list('species_id',flat=True).distinct()
    spids = set(spids) # this is not to throw out duplicates but to evaluate the QuerySet,
                       # otherwise it becomes slow due to false optimization.
    species = SpeciesModel.objects.filter(pk__in=spids)
    nspecies = species.count()
    nstates = 0
    if addStates:
        species,ns = addStates(transs,species,StateModel)
        nstates += ns

    return species,nspecies,nstates

def getMethods():
    "Define and map the methods of VALD to xsams equivalents. Store on object for easy access through dictionary"
    class Method(object):
        # OBSTYPE_DICT = {'exp':0, 'obs':1, 'emp':2, 'pred':3, 'calc':4, 'mix':5}
        CATEGORY_DICT = {0:'experiment', 1:'semiempirical', 2:'derived', 3:'theory',4:'semiempirical',5:'compilation'}
        DESC_DICT = {0: "VALD exp - transition between levels with experimentally known energies",
                     1: "VALD obs - transition between levels with experimentally known energies",
                     2: "VALD emp - relativistic Hartree-Fock calculations, normalized to the experimental lifetimes",
                     3: "VALD pred - transitions between predicted energy levels",
                     4: "VALD calc - relativistic Hartree-Fock calculations of lifetimes and transition probabilities",
                     5: "VALD mix - mixture of observation times"}
        def __init__(self, ID):
            self.id = ID
            self.category = self.CATEGORY_DICT[ID]
            self.description = self.DESC_DICT[ID]
    return (Method(0), Method(1), Method(2), Method(3), Method(4), Method(5))
