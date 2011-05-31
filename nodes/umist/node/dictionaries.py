# -*- coding: utf-8 -*-
"""
ExampleNode dictionary definitions. 
"""

# The returnable dictionary is used internally by the node and defines
# all the ways the VAMDC standard keywords (left-hand side) maps to
# the internal database representation queryset (right-hand side)
#
# When writing this, it helps to remember that dictionary is applied
# in a loop to every matching *instance* of the queryset variables
# returned from queryfunc.py. So in the example below, all 'Sources'
# will be looped over by the node software, using the name 'Source'
# (singular). 'Source' will be one single instance of a matching
# database object, from which we extract everything we need (if you
# look at queryfuncs.py, you'll see 'Sources' being assigned)

RETURNABLES = {\
'NodeID':'umist',

'SourceID':'Source.abbr',
#'SourceAuthorName':'Source.author',
#'SourceCategory':'Source.category',
#'SourcePageBegin':'Source.pages',
#'SourcePageEnd':'Source.pages',
#'SourceName':'Source.journal',
'SourceTitle':'Source.title',
'SourceURI':'Source.url',
#'SourceVolume':'Source.volume',
#'SourceYear':'Source.year',

'CollisionThreshold':'CollTrans.tmin'
}

# The restrictable dictionary defines limitations to the search. 
# The left-hand side is standardized, the righ-hand size should
# be defined in Django query-language style, where e.g. a search
# for the Species.atomic field  would be written as species__atomic.

RESTRICTABLES = {\
'MoleculeInchiKey':'reaction__species__vamdc_inchikey',
'MoleculeInchi':'reaction__species__vamdc_inchi',
'MoleculeChemicalName':'reaction__species__names',
}

from vamdctap.caselessdict import CaselessDict
RESTRICTABLES = CaselessDict(RESTRICTABLES)
RETURNABLES = CaselessDict(RETURNABLES)
