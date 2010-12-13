# -*- coding: utf-8 -*-

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

