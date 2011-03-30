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
'NodeID':'ExampleNode',

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
                                                                         
'RadTransSpeciesRef':'RadTran.species_id',
'RadTransComments':'Wavelength is for vacuum.',
'RadTransWavelength':'RadTran.vacwave',
'RadTransWavelengthUnit':u'A',
'RadTransWavelengthRef':'RadTran.wave_ref_id',
'RadTransWavelengthMethodCategory':'experiment',
'RadTransFinalStateRef':'RadTran.lostate.id',
'RadTransInitialStateRef':'RadTran.upstate.id',
'RadTransProbabilityLog10WeightedOscillatorStrength':'RadTran.loggf',
'RadTransProbabilityLog10WeightedOscillatorStrengthUnit':'unitless',
'RadTransProbabilityLog10WeightedOscillatorStrengthRef':'RadTran.loggf_ref_id',
'RadTransProbabilityLog10WeightedOscillatorStrengthMethod':'RadTran.loggf_method',
'RadTransProbabilityLog10WeightedOscillatorStrengthAccuracy':'RadTran.loggf_accur',

'RadTransBroadeningNaturalLineshapeParameter':'RadTran.gammarad',
'RadTransBroadeningNaturalLineshapeParameterName':'log(gamma)',
'RadTransBroadeningNaturalLineshapeParameterUnit':'cm3/s',
'RadTransBroadeningNaturalRef':'RadTran.gammarad_ref_id',

'RadTransBroadeningStarkLineshapeParameter':'RadTran.gammastark',
'RadTransBroadeningStarkLineshapeName':'lorentzian',
'RadTransBroadeningStarkLineshapeParameterName':'log(gamma)',
'RadTransBroadeningStarkLineshapeParameterUnit':'cm3/s',
'RadTransBroadeningStarkRef':'RadTran.gammastark_ref_id',

'RadTransBroadeningVanDerWaalsLineshapeParameter':'RadTran.gammawaals',
'RadTransBroadeningVanDerWaalsLineshapeParameterUnit':'["cm3/s","unitless"]',

'RadTransBroadeningVanDerWaalsLineshapeName':'lorentzian',
'RadTransBroadeningVanDerWaalsLineshapeParameterName':'["log(gamma)","alpha"]',
'RadTransBroadeningVanDerWaalsRef':'RadTran.waals_ref_id',

'RadTransEffectiveLandeFactor':'RadTran.landeff',
'RadTransEffectiveLandeFactorUnit':'unitless',
'RadTransEffectiveLandeFactorRef':'RadTran.lande_ref_id',
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

from vamdctap.caselessdict import CaselessDict
RESTRICTABLES = CaselessDict(RESTRICTABLES)
RETURNABLES = CaselessDict(RETURNABLES)
