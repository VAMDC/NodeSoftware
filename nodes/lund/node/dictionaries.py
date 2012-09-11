#-*- coding: utf-8 -*-

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
'AtomStateHyperfineConstantA': 'AtomState.hfs_a',
'AtomStateHyperfineConstantAUnit':'unitless',
'AtomStateHyperfineConstantB': 'AtomState.hfs_b',
'AtomStateHyperfineConstantBUnit': 'unitless',
'AtomStateLifeTime': 'AtomState.get_best_tau()',
'AtomStateLifeTimeMethod': 'AtomState.get_tau_ref()',
'AtomStateLifeTimeAccuracy': 'AtomState.tau_accur',                                     
'AtomStateLifeTimeDecay': 'totalRadiative',
                                                                         
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

from vamdctap.unitconv import *

RESTRICTABLES = {\
'AtomSymbol':'species__name',
'AtomNuclearCharge':'species__atomic',
'StateEnergy':bothStates,
'Lower.StateEnergy':'lostate__energy',
'Upper.StateEnergy':'upstate__energy',
'RadTransWavelength':'vacwave',
'RadTransWavenumber':'vavenum',
'RadTransProbabilityLog10WeightedOscillatorStrength':'loggf',
'IonCharge':'species__ion'
}

