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

'SourceID':'Source.id',
'SourceAuthorName':'Source.author',
'SourceCategory':'Source.category',
'SourcePageBegin':'Source.pages',
'SourcePageEnd':'Source.pages',
'SourceName':'Source.journal',
'SourceTitle':'Source.title',
'SourceURI':'Source.url',
'SourceVolume':'Source.volume',
'SourceYear':'Source.year',                                                              

'MethodID':'Method.id',
'MethodCategory':'Method.category',
                           
'FunctionID':'Function.id',
'FunctionName':'Function.name',
'FunctionSourceRef': "",
'FunctionComputerLanguage': "",
'FunctionExpression':"Function.expression",
'FunctionYName':"Function.y",
'FunctionYUnits':"unitless",
'FunctionYDescription':"",
'FunctionYLowerLimit':"0.0",
'FunctionYUpperLimit':"1.0",
'FunctionArgumentName':'FunctionArgument.name',
'FunctionArgumentUnits': "unitless",
'FunctionArgumentDescription': "",
'FunctionArgumentLowerLimit':"FunctionArgument.lower_limit",
'FunctionArgumentUpperLimit':"FunctionArgument.upper_limit",
'FunctionParameterName':"FunctionParameter.name",
'FunctionParameterUnits':"unitless",
'FunctionParameterDescription':"",
'FunctionReferenceFrame':"",
'FunctionDescription':"",
'FunctionSourceCodeURL': ""

}

# The restrictable dictionary defines limitations to the search. 
# The left-hand side is standardized, the righ-hand size should
# be defined in Django query-language style, where e.g. a search
# for the Species.atomic field  would be written as species__atomic.

RESTRICTABLES = {\
'MoleculeInchiKey':'reaction_id__r1_species__vamdc_inchikey',
'MoleculeInchi':'reaction_id__r1_species__vamdc_inchi',
'MoleculeChemicalName':'reaction_id__r1_species__names',
'MoleculeInchiKey':'reaction_id__r2_species__vamdc_inchikey',
'MoleculeInchi':'reaction_id__r2_species__vamdc_inchi',
'MoleculeChemicalName':'reaction_id__r2_species__names',
'MoleculeInchiKey':'reaction_id__r3_species__vamdc_inchikey',
'MoleculeInchi':'reaction_id__r3_species__vamdc_inchi',
'MoleculeChemicalName':'reaction_id__r3_species__names',
'MoleculeInchiKey':'reaction_id__p1_species__vamdc_inchikey',
'MoleculeInchi':'reaction_id__p1_species__vamdc_inchi',
'MoleculeChemicalName':'reaction_id__p1_species__names',
'MoleculeInchiKey':'reaction_id__p2_species__vamdc_inchikey',
'MoleculeInchi':'reaction_id__p2_species__vamdc_inchi',
'MoleculeChemicalName':'reaction_id__p2_species__names',
'MoleculeInchiKey':'reaction_id__p3_species__vamdc_inchikey',
'MoleculeInchi':'reaction_id__p3_species__vamdc_inchi',
'MoleculeChemicalName':'reaction_id__p3_species__names',
'MoleculeInchiKey':'reaction_id__p4_species__vamdc_inchikey',
'MoleculeInchi':'reaction_id__p4_species__vamdc_inchi',
'MoleculeChemicalName':'reaction_id__p4_species__names',
'AtomStateEnergy':'upstate__energy',
'RadTransWavelength':'vacwave',
'RadTransWavenumber':'vavenum',
'RadTransProbabilityLog10WeightedOscillatorStrength':'loggf',
'AtomIonCharge':'species__ion'
}

from vamdctap.caselessdict import CaselessDict
RESTRICTABLES = CaselessDict(RESTRICTABLES)
RETURNABLES = CaselessDict(RETURNABLES)
