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
#'AtomStateTermLKLSymbol':"",          #TODO
'AtinStateTernKJS2':'Component.s2',

#############################################################
'RadTransID':'RadTran.id',
'RadTransSpeciesRef':'RadTran.species_id',
'RadTransWavelength':'RadTran.waves()',
'RadTransWavelengthUnit':u'A',
'RadTransWavelengthMethod':'RadTran.method_return',
'RadTransWavelengthComment': 'RadTran.wavecomment()',
#'RadTransProcess':"RadTran.transition_type",
'RadTransProcess':"excitation",
'RadTransWavelengthRef':'RadTran.waverefs()',
'RadTransUpperStateRef':'RadTran.upstate_id',
'RadTransLowerStateRef':'RadTran.lostate_id',
#'RadTransProbabilityA':'RadTran.einsteina',
'RadTransProbabilityLog10WeightedOscillatorStrength':'RadTran.loggf',
#'RadTransProbabilityLog10WeightedOscillatorStrengthEval':'RadTran.accur',
'RadTransProbabilityLog10WeightedOscillatorStrengthUnit':'unitless',
'RadTransProbabilityLog10WeightedOscillatorStrengthRef':'RadTran.loggf_ref_id',

'RadTransBroadeningNaturalLineshapeParameter':'RadTran.gammarad',
'RadTransBroadeningNaturalLineshapeParameterName':'log(gamma)',
'RadTransBroadeningNaturalLineshapeParameterUnit':'cm3/s',
'RadTransBroadeningNaturalRef':'RadTran.gammarad_ref_id',
'RadTransBroadeningNaturalEnvironment':'natural',
'RadTransBroadeningNaturalLineshapeName':'lorentzian',
'RadTransBroadeningNaturalComment':"Natural Broadening",

'RadTransBroadeningPressureChargedLineshapeParameter':'RadTran.gammastark',
'RadTransBroadeningPressureChargedLineshapeName':'lorentzian',
'RadTransBroadeningPressureChargedLineshapeParameterName':'log(gamma)',
'RadTransBroadeningPressureChargedLineshapeParameterUnit':'cm3/s',
'RadTransBroadeningPressureChargedRef':'RadTran.gammastark_ref_id',
'RadTransBroadeningPressureChargedEnvironment':'stark',
'RadTransBroadeningPressureChargedComment':"Stark Broadening",
'RadTransBroadeningPressureChargedLineshapeFunction':"stark",

'RadTransBroadeningPressureNeutralLineshapeParameter':'RadTran.getWaals()',
'RadTransBroadeningPressureNeutralLineshapeName':'lorentzian',
'RadTransBroadeningPressureNeutralLineshapeParameterName':'log(gamma)',
'RadTransBroadeningPressureNeutralLineshapeParameterUnit':'cm3/s',
'RadTransBroadeningPressureNeutralLineshapeParameterName':'RadTran.getWaalsName()',  #'log(gamma)',
'RadTransBroadeningPressureNeutralLineshapeParameterUnit':'RadTran.getWaalsUnits()', #'cm3/s',
'RadTransBroadeningPressureNeutralRef':'RadTran.waals_ref_id',
'RadTransBroadeningPressureNeutralEnvironment':'waals',
'RadTransBroadeningPressureNeutralComment':"Van der Waals broadening",
'RadTransBroadeningPressureNeutralLineshapeFunction':"RadTran.getWaalsFunction()",

'RadTransProbabilityOscillatorStrengthAccuracy':'Radtran.accur',
'RadTransProbabilityOscillatorStrengthAccuracyType':'Radtran.getAccurType()',
'RadTransProbabilityOscillatorStrengthAccuracyRelative':'Radtran.getAccurRelative()'
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
'InchiKey':'species__inchi',
'InchiKey':'species__inchikey',
'StateEnergy':bothStates,
'Lower.StateEnergy':'lostate__energy',
'Upper.StateEnergy':'upstate__energy',
'RadTransWavelength':'wavevac',
'RadTransWavenumber':('wavevac',invcm2Angstr),
'RadTransFrequency':('wavevac',Hz2Angstr),
'RadTransEnergy':('wavevac',eV2Angstr),
'RadTransProbabilityLog10WeightedOscillatorStrength':'loggf',
'RadTransBroadeningNatural':'gammarad',
'RadTransBroadeningPressure':'gammastark',
'MethodCategory':('method_restrict',valdObstype),
'RadTransProbabilityA':'einsteina'
}
