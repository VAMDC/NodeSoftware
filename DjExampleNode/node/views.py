# -*- coding: utf-8 -*-

# import your models 
#from DjExampleNode.node.models import *

### IMPORTANT NOTE
### Here you must have a function called setupResults()
### which takes Q-objects as generated from the query
### parser. setupResults() should pass these on to your
### models and use them to fetch the corresponding items
### from other models. It should return a DICTIONARY 
### that has as keys some of the following
### Sources
### AtomStates
### MoleStates
### CollTrans
### RadTrans
### Methods
###
### and the values for these keys being the QuerySets.
### this dictionary will be handed into the generator.
###
### Below is an example, inspired by VALD that might help.
### 
### First two helper functions:

# a straight forward example of getting the unique list of
# states that corresponf to a given list of transitions by
# use of the inverse foreign key.
def getVALDstates(transs):
    q1,q2=Q(islowerstate_trans__in=transs),Q(islowerstate_trans__in=transs)
    return State.objects.filter(q1|q2).distinct()
    
# another example that uses a python set to collect reference ids
# that are not stored as foreignkeys in the model
def getVALDsources(transs):
    sids=set([])
    for trans in transs:
        s=set([trans.wave_ref,trans.loggf_ref,trans.lande_ref,trans.gammarad_ref,trans.gammastark_ref,trans.gammawaals_ref])
        sids=sids.union(s)
    return Source.objects.filter(pk__in=sids)


def setupResults(qtup,limit=0):
    # pass the Q-objects to the transition model
    transs = Transition.objects.filter(*qtup)
    
    totalcount=transs.count()
    if limit :
        transs = transs[:limit]

    # call the functions that return 
    sources = getVALDsources(transs)
    states = getVALDstates(transs)

    # return the dictionary as described above
    return {\
	'RadTrans':transs,
	'Sources':sources,
	'AtomStates':states,
	}
