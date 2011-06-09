# -*- coding: utf-8 -*-

import sys
from itertools import chain
from django.conf import settings
from vamdctap.sqlparse import where2q
import dictionaries
from models import States, Transitions
from django.utils.importlib import import_module
from vamdctap.sqlparse import *
from django.db.models import Q
from vamdctap.caselessdict import CaselessDict

def LOG(s):
    "Simple logger function"
    if settings.DEBUG: print >> sys.stderr, s



def getSpeciesWithStates(transs):
    """
    Use the Transition matches to obtain the related Species (only atoms in this example)
    and the states related to each transition. 
    
    We also return some statistics of the result 
    """

    # get the reference ids for the 'species' ForeignKey field 
    # (see getRefs comment for more info)
    spids = set( transs.values_list('species_id',flat=True) )
    # use the reference ids to query the Species database table 
    species = models.Species.objects.filter(pk__in=spids)
    nspecies = species.count() # get some statistics 

    # get all states. Note that when building a queryset like this,
    # (using objects.filter() etc) will usually not hit the database
    # until it's really necessary, making this very efficient. 
    nstates = 0
    for spec in species:
        # get all transitions in linked to this particular species 
        spec_transitions = transs.filter(species=spec)
        # extract reference ids for the states from the transion, combining both
        # upper and lower unique states together
        up = spec_transitions.values_list('upstate_id',flat=True)
        lo = spec_transitions.values_list('lostate_id',flat=True)
        sids = set(chain(up, lo))

        # use the found reference ids to search the State database table 
        # Note that we store a new queryset called 'States' on the species queryset. 
        # This is important and a requirement looked for by the node 
        # software (all RETURNABLES AtomState* will try to loop over this
        # nested queryset). 
        spec.States = models.State.objects.filter( pk__in = sids )    
        nstates += spec.States.count()
    return species, nspecies, nstates

def setupResults(sql, LIMIT=1000):

    # convert the incoming sql to a correct django query syntax object 
    # based on the RESTRICTABLES dictionary in dictionaries.py
    # (where2q is a helper function to do this for us).
    q = where2q(sql.where, dictionaries.RESTRICTABLES)
    try: 
        q = eval(q) # test queryset syntax validity
    except: 
        return {}

    # Find transitions satisfying the criteria.
    transitions = Transitions.objects.filter(q)
    nTransitions = transitions.count()
    LOG("Number of transitions: %d"%nTransitions)

    # Truncate the list of matching transitions.
    # Record the degree of truncation s.t. it can be reported in the output.
    # NB: reporting goes wrong when no transitions are selected.
    if LIMIT < nTransitions :
        transitions = transitions[:LIMIT]
        percentage = '%.1f'%(float(LIMIT)/nTransitions *100)
    else: 
        percentage = None

    # Find states matching the selected transitions and species with those states.
    species, nSpecies, nStates = getSpeciesWithStates(transitions)

    # Create the header with some useful info. The key names here are
    # standardized and shouldn't be changed.
    headerinfo=CaselessDict({\
            'Truncated':percentage,
            'COUNT-SOURCES':nSources,
            'COUNT-species':nSpecies,
            'count-states':nStates,
            'count-radiative':nTransitions
            })

    # return the result dictionary 
    return {'RadTrans':transitions,
            'Atoms': species,
            'Sources': sources,
            'HeaderInfo': headerinfo,
            # 'Methods':methods
            #'Functions':functions
           }
