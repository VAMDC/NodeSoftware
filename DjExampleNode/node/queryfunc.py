# -*- coding: utf-8 -*-

# Get the models
from django.conf import settings
from django.utils.importlib import import_module
MODELS=import_module(settings.NODEPKG+'.models')

from nodelib.sqlparse import where2q
from dictionaries import *

# a straight forward example of getting the unique list of
# states that correspond to a given list of transitions by
# use of the inverse foreign key.
def getVALDstates(transs):
    q1,q2=Q(islowerstate_trans__in=transs),Q(islowerstate_trans__in=transs)
    return State.objects.filter(q1|q2).distinct()
    
# For the Sources we use a python set to collect reference ids
# (which are not stored as foreignkeys in the model). This is faster
# because there are so many Sources which are the same and by getting
# rid of duplicates before asking the DB, we sve time.
def getVALDsources(transs):
    sids=set([])
    for trans in transs:
        s=set([trans.wave_ref,trans.loggf_ref,trans.lande_ref,trans.gammarad_ref,trans.gammastark_ref,trans.gammawaals_ref])
        sids=sids.union(s)
    return Source.objects.filter(pk__in=sids)


def setupResults(sql):
    q=where2q(sql.where,RESTRICTABLES)
    try: q=eval(q)
    except: return {}

    transs = Transition.objects.filter(q)
    
    # use the functions from above  
    sources = getVALDsources(transs)
    states = getVALDstates(transs)

    # return the dictionary as described above
    return {\
	'RadTrans':transs,
	'Sources':sources,
	'AtomStates':states,
	}
