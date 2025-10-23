# -*- coding: utf-8 -*-

RETURNABLES = {\
'NodeID':'vald',
#############################################################
'MethodID':'Method.id',
'MethodCategory':'Method.category',
'MethodDescription':'Method.description',
#############################################################
'AtomStateID':'AtomState.id',
'AtomSymbol':'Atom.name',
'AtomSpeciesID':'Atom.id',
'AtomInchiKey':'Atom.inchikey',
'AtomInchi':'Atom.inchi',
'AtomNuclearCharge':'Atom.atomic',
'AtomIonCharge':'Atom.ion',
'AtomMassNumber':'Atom.massno',
'AtomStateDescription': 'AtomState.term_desc',
'AtomStateLandeFactor':'AtomState.lande',
'AtomStateLandeFactorUnit':'unitless',
'AtomStateLandeFactorRef':'AtomState.lande_ref_id',
'AtomStateEnergy':'AtomState.energy',
'AtomStateEnergyRef':'AtomState.energy_ref_id',
'AtomStateEnergyUnit':'1/cm',

'AtomStateParity':'AtomState.p',
'AtomStateTotalAngMom':'AtomState.j',

'AtomStateHyperfineConstantA':'AtomState.hfs_a',
'AtomStateHyperfineConstantAAccuracy':'AtomState.hfs_a_error',
'AtomStateHyperfineConstantB':'AtomState.hfs_b',
'AtomStateHyperfineConstantBAccuracy':'AtomState.hfs_b_error',

'AtomStateTermLSL':'Component.l',
'AtomStateTermLSS':'Component.s',
'AtomStateTermMultiplicity':'Component.multiplicity()',
'AtomStateTermLSSeniority':'Component.sn',
#'AtomStateTermJJ':'Component.jj()',
'AtomStateTermJ1J2':'Component.jj()',
'AtomStateTermK':'Component.k',
'AtomStateTermJKJ':'Component.jc',
'AtomStateTermJKS':'Component.s2',
'AtomStateTermLKL':'Component.l',
'AtomStateTermLKK':'Component.k',
#'AtomStateTermLKLSymbol':"",
'AtomStateTermKJS2':'Component.s2',
'AtomStateShellPrincipalQN':'Component.n',

#############################################################
'RadTransID':'RadTran.id',
'RadTransSpeciesRef':'RadTran.species_id',
'RadTransWavelength':'RadTran.get_waves()',
'RadTransWavelengthComment': 'RadTran.get_wave_comments()',
'RadTransWavelengthRef':'RadTran.get_wave_refs()',
'RadTransWavelengthUnit':u'A',
'RadTransWavelengthMethod':'RadTran.method_return',
#'RadTransProcess':"RadTran.transition_type",
'RadTransProcess':"excitation",
'RadTransUpperStateRef':'RadTran.upstate_id',
'RadTransLowerStateRef':'RadTran.lostate_id',
#'RadTransProbabilityA':'RadTran.einsteina',
'RadTransProbabilityLog10WeightedOscillatorStrength':'RadTran.loggf',
#'RadTransProbabilityLog10WeightedOscillatorStrengthEval':'RadTran.accur',
'RadTransProbabilityLog10WeightedOscillatorStrengthUnit':'unitless',
'RadTransProbabilityLog10WeightedOscillatorStrengthRef':'RadTran.loggf_ref_id',

'RadTransBroadeningNaturalLineshapeParameter':'RadTran.gammarad',
'RadTransBroadeningNaturalLineshapeParameterName':'log(gamma)',
'RadTransBroadeningNaturalLineshapeParameterUnit':'1/s',
'RadTransBroadeningNaturalRef':'RadTran.gammarad_ref_id',
'RadTransBroadeningNaturalEnvironment':'natural',
'RadTransBroadeningNaturalLineshapeName':'lorentzian',
'RadTransBroadeningNaturalComment':"Natural Broadening",

'RadTransBroadeningPressureChargedLineshapeParameter':'RadTran.gammastark',
'RadTransBroadeningPressureChargedLineshapeName':'lorentzian',
'RadTransBroadeningPressureChargedLineshapeParameterName':'log(gamma)',
'RadTransBroadeningPressureChargedLineshapeParameterUnit':'1/cm3/s',
'RadTransBroadeningPressureChargedRef':'RadTran.gammastark_ref_id',
'RadTransBroadeningPressureChargedEnvironment':'stark',
'RadTransBroadeningPressureChargedComment':"Stark Broadening",
'RadTransBroadeningPressureChargedLineshapeFunction':"stark",

'RadTransBroadeningPressureNeutralLineshapeParameter':'RadTran.get_waals()',
'RadTransBroadeningPressureNeutralLineshapeName':'lorentzian',
'RadTransBroadeningPressureNeutralLineshapeParameterName':'RadTran.get_waals_name()',  #'log(gamma)',
'RadTransBroadeningPressureNeutralLineshapeParameterUnit':'RadTran.get_waals_units()', #'cm3/s',
'RadTransBroadeningPressureNeutralRef':'RadTran.waals_ref_id',
'RadTransBroadeningPressureNeutralEnvironment':'waals',
'RadTransBroadeningPressureNeutralComment':"Van der Waals broadening",
'RadTransBroadeningPressureNeutralLineshapeFunction':"RadTran.get_waals_function()",

'RadTransProbabilityOscillatorStrengthAccuracy':'Radtran.accur',
'RadTransProbabilityOscillatorStrengthAccuracyType':'Radtran.get_accur_type()',
'RadTransProbabilityOscillatorStrengthAccuracyRelative':'Radtran.get_accur_relative()'
}

# import the converter functions
from vamdctap.unitconv import *

# custom function
from django.db.models import Q

RESTRICTABLES = {\
#'ConstantTest':test_constant_factory('"U"'),
'AtomSymbol':'species__name',
'AtomMassNumber':'species__massno',
'AtomNuclearCharge':'species__atomic',
'IonCharge':'species__ion',
'Inchi':'species__inchi',
'InchiKey':'species__inchikey',
'StateEnergy':bothStates,
'Lower.StateEnergy':'lostate__energy',
'Upper.StateEnergy':'upstate__energy',
'RadTransWavelength':'wave',
'RadTransWavenumber':('wave',invcm2Angstr),
'RadTransFrequency':('wave',Hz2Angstr),
'RadTransEnergy':('wave',eV2Angstr),
'RadTransProbabilityLog10WeightedOscillatorStrength':'loggf',
'RadTransBroadeningNatural':'gammarad',
'RadTransBroadeningPressure':'gammastark',
'MethodCategory':('method_restrict',valdObstype),
'RadTransProbabilityA':'einsteina'
}
