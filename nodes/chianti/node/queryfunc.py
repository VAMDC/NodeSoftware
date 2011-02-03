# -*- coding: utf-8 -*-

from models import States, Transitions
from django.utils.importlib import import_module
from vamdctap.sqlparse import *
from dictionaries import *
from django.db.models import Q

def setupResults(sql, LIMIT=1000):
    #print sql
    # Obtain the query constraints as Django Q objects - a "query set" IIRC
    qString = where2q(sql.where,RESTRICTABLES)
    print qString
    q = eval(qString)

    print Transitions.objects.count();

    # Find transitions satisfying the criteria.
    transitions = Transitions.objects.filter(q)
    nTransitions = transitions.count()
    print nTransitions;

    # Truncate the list of matching transitions.
    # Record the degree of truncation s.t. it can be reported in the output.
    # NB: reporting goes wrong when no transitions are selected.
    if LIMIT < nTransitions :
        transitions = transitions[:LIMIT]
        percentage = '%.1f'%(float(LIMIT)/nTransitions *100)
    else: 
        percentage = None

    # Find states matching the selected transitions.
    print "Gettings states matching the transitions list"
    state_ids = set([])
    for t in transitions:
        state_ids.add(t.chiantiradtransinitialstateindex.pk)
        state_ids.add(t.chiantiradtransfinalstateindex.pk)
    states = States.objects.filter(pk__in = state_ids)
    print "Finished getting states"
    nStates = states.count()
    
    print "returning results to generator"

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


# return the result dictionary 
    return {\
        'RadTrans':transitions,
	'AtomStates':states,
        'HeaderInfo':headerinfo
	}
