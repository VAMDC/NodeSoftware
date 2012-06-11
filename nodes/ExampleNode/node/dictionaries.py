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
# returned from queryfunc.py. So in the example below, all 'AtomStates'
# will be looped over by the node software, using the name 'AtomState'
# (singular). 'AtomState' will be one single instance of a matching
# database object, from which we extract everything we need by parsing
# the VAMDC_standard LHS of this dictionary to how it maps to our specific
# database on the RHS. So, when looping through all AtomState objects
# matching the given query, the generator will for example know that
# to get the AtomStateEnergy VAMDC value, it will need to look at
# the AtomState.energy, i.e. the "energy" property of the current
# database object being worked on.
#
# (if you look at queryfuncs.py, you'll see 'AtomStates' being
#  assigned)

RETURNABLES = {\
'NodeID':'ExampleNode', # required
############################################################
'MethodID':'Method.id',
'MethodCategory':'Method.category',
############################################################
# Sources are handled by XML method on model.
'AtomStateID':'AtomState.id',
'AtomSymbol':'Atom.name',
'AtomSpeciesID':'Atom.id',
'AtomNuclearCharge':'Atom.atomic',
'AtomIonCharge':'Atom.ion',
'AtomMassNumber':'Atom.massno',
'AtomStateLandeFactor':'AtomState.lande',
'AtomStateLandeFactorUnit':'unitless',
'AtomStateLandeFactorRef':'AtomState.lande_ref_id',
'AtomStateEnergy':'AtomState.energy',
'AtomStateEnergyRef':'AtomState.energy_ref_id',
'AtomStateEnergyUnit':'1/cm',
'AtomStateDescription':'',
'AtomStateLifeTime': 'AtomState.get_best_tau()',
'AtomStateLifeTimeMethod': 'AtomState.get_tau_ref()',
############################################################
'RadTransSpeciesRef':'RadTran.species_id',
'RadTransComment':'Wavelength is for vacuum.',
'RadTransWavelength':'RadTran.vacwave',
'RadTransWavelengthUnit':u'A',
'RadTransWavelengthRef':'RadTran.wave_ref_id',
'RadTransLowerStateRef':'RadTran.lostate.id',
'RadTransUpperStateRef':'RadTran.upstate.id',
'RadTransProbabilityLog10WeightedOscillatorStrength':'RadTran.loggf',
'RadTransProbabilityLog10WeightedOscillatorStrengthUnit':'unitless',
'RadTransProbabilityLog10WeightedOscillatorStrengthRef':'RadTran.loggf_ref_id',
'RadTransProbabilityLog10WeightedOscillatorStrengthMethod':'RadTran.loggf_method',
'RadTransProbabilityLog10WeightedOscillatorStrengthAccuracy':'RadTran.loggf_accur',
############################################################
'RadTransBroadeningNaturalLineshapeParameter':'RadTran.gammarad',
'RadTransBroadeningNaturalLineshapeParameterName':'log(gamma)',
'RadTransBroadeningNaturalLineshapeParameterUnit':'cm3/s',
'RadTransBroadeningNaturalRef':'RadTran.gammarad_ref_id',
############################################################
'RadTransBroadeningPressureLineshapeParameter':'RadTran.gammawaals',
'RadTransBroadeningPressureLineshapeParameterUnit':'["cm3/s","unitless"]',
'RadTransBroadeningPressureLineshapeName':'lorentzian',
'RadTransBroadeningPressureLineshapeParameterName':'["log(gamma)","alpha"]',
'RadTransBroadeningPressureRef':'RadTran.waals_ref_id',
############################################################
'RadTransEffectiveLandeFactor':'RadTran.landeff',
'RadTransEffectiveLandeFactorUnit':'unitless',
'RadTransEffectiveLandeFactorRef':'RadTran.lande_ref_id',
############################################################
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
'AtomSymbol':'species__name',
'AtomNuclearCharge':'species__atomic',
'AtomStateEnergy':'upstate__energy',
'RadTransWavelength':'vacwave',
'RadTransWavenumber':'vavenum',
'RadTransProbabilityLog10WeightedOscillatorStrength':'loggf',
'AtomIonCharge':'species__ion'
}

