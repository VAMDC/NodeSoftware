from django.db.models import Q
from vamdctap.sqlparse import *
from dictionaries import *
from models import *

def setupResults(sql, LIMIT=1000):
    q=where2q(sql.where,RESTRICTABLES)
    transs = Transition.objects.filter(q)
    ntranss=transs.count()

    if LIMIT < ntranss :
        transs = transs[:LIMIT]
        percentage = '%.1f'%(float(LIMIT)/ntranss *100)
    else: percentage=None

    state_ids = set([])
    for trans in transs:
        s = set([trans.upstate.pk,trans.lostate.pk])
        state_ids = state_ids.union(s)
    states = State.objects.filter(pk__in = state_ids)

    #upper = Q(upstate_set__in = transs)
    #lower = Q(lowstate_set__in = transs)
    #states = State.objects.filter( upper | lower ).distinct()

    nstates = states.count()
    nspecies = transs.values('species').distinct().count()

    headerinfo=CaselessDict({\
            'Truncated':'%s %%'%percentage,
            'COUNT-species':nspecies,
            'count-states':nstates,
            'count-radiative':ntranss
            })


    return {'RadTrans':transs,
            'AtomStates':states,
            'HeaderInfo':headerinfo
           }

