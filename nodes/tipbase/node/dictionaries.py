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
'NodeID':'Tipbase',

#'SourceID':'Source.id',
#'SourceAuthorName':'Source.author',
#'SourceCategory':'Source.category',
#'SourcePageBegin':'Source.pages',
#'SourcePageEnd':'Source.pages',
#'SourceName':'Source.journal',
#'SourceTitle':'Source.title',
#'SourceURI':'Source.url',
#'SourceVolume':'Source.volume',
#'SourceYear':'Source.year',                                                              

#'MethodID':'Method.id',
#'MethodCategory':'Method.category',
                           
'AtomStateID':'AtomState.id',

'AtomSymbol':'Atom.atomicion.isotope.chemicalelement.elementsymbol',
'AtomSpeciesID':'Atom.atomicion.id',
'AtomNuclearCharge':'Atom.atomicion.isotope.chemicalelement.nuclearcharge',
'AtomIonCharge':'Atom.atomicion.ioncharge',
'AtomMassNumber':'Atom.atomicion.isotope.massnumber',

#'AtomStateLandeFactor':'AtomState.lande',
#'AtomStateLandeFactorUnit':'unitless',
#'AtomStateLandeFactorRef':'AtomState.lande_ref_id',
'AtomStateEnergy':'AtomState.stateenergy',
'AtomStateEnergyUnit':'AtomState.stateenergyunit.value',
#'AtomStateEnergyRef':'AtomState.energy_ref_id',
#'AtomStateDescription':'',
'AtomStateParity' : 'AtomState.parity.value',
'AtomStateMixingCoeff':'AtomState.Component.mixingcoefficient',
'AtomStateMixingCoeffClass' : 'AtomState.Component.mixingclass.value',
'AtomStateLifeTime': 'AtomState.lifetime',
'AtomStateStatisticalWeight' : 'AtomState.statisticalweight',
'AtomStateStatisticalWeightUnit' : 'AtomState.statisticalweightunit.value',
'AtomStateLifeTimeUnit': 'AtomState.lifetimeunit.value',
'AtomStateIonizationEnergy' : 'AtomState.ionizationenergy',
'AtomStateIonizationEnergyUnit' : 'AtomState.ionizationenergyunit.value',
'AtomStateTotalAngMom' : 'AtomState.totalangularmomentum',
'AtomStateTermLabel' : 'AtomState.Component.termlabel',
'AtomStateTermLSL' : 'AtomState.Component.Lscoupling.l',
'AtomStateTermS' : 'AtomState.Component.Lscoupling.s',
'AtomStateTermLSMultiplicity' : 'AtomState.Component.Lscoupling.multiplicity',
#'AtomStateLifeTimeMethod': 'AtomState.get_tau_ref()',
                                                                         
'CollisionTabulatedDataX' : 'Colltran.x',
'CollisionTabulatedDataY' : 'Colltran.y',
'CollisionDataSetDescription' : 'Colltran.dataSetDescription ',


#'FunctionID':'Function.id',
#'FunctionName':'Function.name',
#'FunctionSourceRef': "",
#'FunctionComputerLanguage': "",
#'FunctionExpression':"Function.expression",
#'FunctionYName':"Function.y",
#'FunctionYUnits':"unitless",
#'FunctionYDescription':"",
#'FunctionYLowerLimit':"0.0",
#'FunctionYUpperLimit':"1.0",
#'FunctionArgumentName':'FunctionArgument.name',
#'FunctionArgumentUnits': "unitless",
#'FunctionArgumentDescription': "",
#'FunctionArgumentLowerLimit':"FunctionArgument.lower_limit",
#'FunctionArgumentUpperLimit':"FunctionArgument.upper_limit",
#'FunctionParameterName':"FunctionParameter.name",
#'FunctionParameterUnits':"unitless",
#'FunctionParameterDescription':"",
#'FunctionReferenceFrame':"",
#'FunctionDescription':"",
#'FunctionSourceCodeURL': ""

}

# The restrictable dictionary defines limitations to the search. 
# The left-hand side is standardized, the righ-hand size should
# be defined in Django query-language style, where e.g. a search
# for the Species.atomic field  would be written as species__atomic.

RESTRICTABLES = {\
'AtomIonCharge' : 'ioncharge',
'AtomNuclearCharge' : 'nuclearcharge',
'AtomSymbol' : 'elementsymbol',
}

