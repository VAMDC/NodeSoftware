# -*- coding: utf-8 -*-

# Lund dictionary

RETURNABLES = {\
'NodeID':'Lund',
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
#'MethodID':'"MOBS"',
#'MethodCategory':'"observed"',
#'MethodDescription':'',
####################################################
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
'AtomStateEnergyUnits':'1/cm',
'AtomStateDescription':'',
'AtomStateHyperfineConstantA': 'AtomState.hfs_a',
'AtomStateHyperfineConstantB': 'AtomState.hfs_b',
'AtomStateLifeTimeCalculated': 'AtomState.tau_calc',
'AtomStateLifeTimeExperimental': 'AtomState.tau_exp',
'AtomStateLifeTimeAccuracy': 'AtomState.tau_accur',
###############################################################
'RadTransSpeciesRef':'RadTran.species_id',
'RadTransComments':'Wavelength is for vacuum.',
'RadTransWavelength':'RadTran.vacwave',
'RadTransWavelengthUnits':u'A',
'RadTransWavelengthExperimentalSourceRef':'RadTran.wave_ref_id',
'RadTransFinalStateRef':'RadTran.lostate.id',
'RadTransInitialStateRef':'RadTran.upstate.id',
'RadTransProbabilityLog10WeightedOscillatorStrength':'RadTran.loggf',
'RadTransProbabilityLog10WeightedOscillatorStrengthSourceRef':'RadTran.loggf_ref_id', 
'RadTransProbabilityLog10WeightedOscillatorStrengthMethodRef':'RadTran.loggf_method',
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

RESTRICTABLES = {\
'AtomSymbol':'species__name',
'AtomNuclearCharge':'species__atomic',
'AtomStateEnergy':'upstate__energy',
'RadTransWavelengthExperimentalValue':'vacwave',
'RadTransWavenumberExperimentalValue':'vavenum',
'RadTransLogGF':'loggf',
'AtomIonCharge':'species__ion',
}



from vamdctap.caselessdict import CaselessDict
RESTRICTABLES = CaselessDict(RESTRICTABLES)
RETURNABLES = CaselessDict(RETURNABLES)
