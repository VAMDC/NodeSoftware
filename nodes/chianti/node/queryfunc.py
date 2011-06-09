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

def LOG(s):
    "Simple logger function"
    if settings.DEBUG: print >> sys.stderr, s

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

    # Find states matching the selected transitions.
    #print "Gettings states matching the transitions list"
    state_ids = set([])
    for t in transitions:
        state_ids.add(t.chiantiradtransinitialstateindex.pk)
        state_ids.add(t.chiantiradtransfinalstateindex.pk)
    states = States.objects.filter(pk__in = state_ids)
    #print "Finished getting states"
    nStates = states.count()
    
    #print "returning results to generator"

    if percentage == None:
        headerinfo = CaselessDict({\
            'count-states':nStates,
            'count-radiative':nTransitions
            })
    else:
        headerinfo=CaselessDict({\
            'Truncated':'%s %%'%percentage,
            'count-states':nStates,
            'count-radiative':nTransitions
            })


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
    return {\
        'RadTrans':transitions,
	'AtomStates':states,
        'HeaderInfo':headerinfo
	}
