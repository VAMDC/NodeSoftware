# -*- coding: utf-8 -*-

from django.utils.importlib import import_module
from vamdctap.sqlparse import *
from dictionaries import *
from models import *

# a straight forward example of getting the unique list of
# states that correspond to a given list of transitions by
# use of the inverse foreign key.
#
#def getStates(transs):
#    q1,q2=Q(islowerstate_trans__in=transs),Q(islowerstate_trans__in=transs)
#    return State.objects.filter(q1|q2).distinct()
    
# Sometimes it is better to use a python set to collect reference ids
# (which are not stored as foreignkeys in the model). This is faster
# eg. when  there are many referenced items which are the same. By getting
# rid of duplicates before asking the DB, we save time.
#
#def getSources(transs):
#    sids=set([])
#    for trans in transs:
#        s=set([trans.wave_ref,trans.loggf_ref,trans.lande_ref,trans.gammarad_ref,trans.gammastark_ref,trans.gammawaals_ref])
#        sids=sids.union(s)
#    return Source.objects.filter(pk__in=sids)


#def setupResults(sql):
#    q = where2q(sql.where,RESTRICTABLES)
#    try: q = eval(q)
#    except: return {}
#
#    transs = Transition.objects.filter(q)
#    
#    # use the functions from above  
#    sources = getVALDsources(transs)
#    states = getVALDstates(transs)
#
#    # return the result dictionary 
#    return {\
#	'RadTrans':transs,
#	'Sources':sources,
#	'AtomStates':states,
#	}
