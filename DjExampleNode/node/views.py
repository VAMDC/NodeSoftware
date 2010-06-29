# -*- coding: utf-8 -*-

# import your models 
#from DjExampleNode.node.models import *

### IMPORTANT NOTE This file must implement a function called 
### setupResults() which takes the parsed SQL from the query parser. 
### setupResults() must pass the restrictions on to one or several of 
### your models (depending on the database strcture) and also fetch the 
### corresponding items from other models that are needed in the return 
### data. setupResults() must return a DICTIONARY that has as keys some 
### of the following: Sources AtomStates MoleStates CollTrans RadTrans 
### Methods; with the corresponding QuerySets as the values for these 
### keys. This dictionary will be handed into the generator an allow it 
### to fill the XML schema.
###
### Below is an example, inspired by VALD that has a data model like 
### this:
### One for the Sources/References
### One for the Species
### One for the States (points to Species once, and to several 
###   references)
### One for Transitions (points twice to States (upper, lower) and to 
###   several Sources)
###
### In this layout, all restrictions in the query can be passed to
### the Transitions model (using the pointers between models to
### restrict eg. Transition.species.ionization) which facilitates
### things.
###
### Now we can code two helper functions that get the corresponding
### Sources and States to a selection of Transitions:

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



# In order to map the global keywords that come in the query
# to the place in the data model where the corresponding data sits, we 
# use two dictionaries, called RESTRICTABLES and RETURNABLES.


RETURNABLES={\
'SourceID':'Source.id', # field "id" in the queryset "Sources" that setupResults() below provides
'SourceCategory':'journal', # using a constant string works
'AtomStateEnergy':'AtomState.energy', 
'RadTransWavelengthExperimentalValue':'RadTran.vacwave',
}

RESTRICTABLES = {\
'AtomSymbol':'species__name',
'AtomStateEnergy':'upstate__energy',
'RadTransWavelengthExperimentalValue':'vacwave',
}

# import a helper unction that converts the WHERE part of the query into 
# strings that define Q-objects when evaluated which in turn can be 
# passed to a model.
from DjNode.tapservice.sqlparse import where2q

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
