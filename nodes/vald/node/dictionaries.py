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
'AtomStateDescription': 'AtomState.description()',
'AtomStateConfigurationLabel': 'AtomState.config',
'AtomStateCoreTermLabel': 'AtomState.term',
'AtomStateLandeFactor':'AtomState.lande',
'AtomStateLandeFactorUnit':'unitless',
'AtomStateLandeFactorRef':'AtomState.lande_ref_id',
'AtomStateEnergy':'AtomState.energy',
'AtomStateEnergyRef':'AtomState.energy_ref_id',
'AtomStateEnergyUnit':'1/cm',
'AtomStateEnergyMethod':'AtomState.energy_method',

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
'AtomStateTermJKK':'Component.k',
'AtomStateTermJKJ':'Component.jc',
'AtomStateTermJKS':'Component.s2',
'AtomStateTermLKL':'Component.l',
'AtomStateTermLKK':'Component.k',
'AtomStateTermLKS2':'Component.s2',
#'AtomStateTermLKLSymbol':""',
'AtomStateShellPrincipalQN':'Component.n',

#############################################################
# MOLECULAR KEYWORDS (map to same State model fields)
#############################################################
'MoleculeChemicalName':'Molecule.name',
'MoleculeSpeciesID':'Molecule.id',
'MoleculeInchiKey':'Molecule.inchikey',
'MoleculeInchi':'Molecule.inchi',
'MoleculeStoichiometricFormula':'Molecule.name',
'MoleculeIonCharge':'Molecule.ion',
'MoleculeMassNumber':'Molecule.massno',

'MoleculeStateID':'MoleculeState.id',
'MoleculeStateEnergy':'MoleculeState.energy',
'MoleculeStateEnergyUnit':'1/cm',
'MoleculeStateEnergyOrigin':'MoleculeState.energy_origin()',
'MoleculeStateEnergyRef':'MoleculeState.energy_ref_id',
'MoleculeStateEnergyMethod':'MoleculeState.energy_method',
'MoleculeStateDescription':'MoleculeState.description()',
'MoleculeStateConfigurationLabel':'MoleculeState.config',
'MoleculeQNCase':'MoleculeState.qn_case()',

# Molecular quantum numbers
'MoleculeQNv':'MoleculeState.v',
'MoleculeQNLambda':'MoleculeState.Lambda',
'MoleculeQNSigma':'MoleculeState.Sigma',
'MoleculeQNOmega':'MoleculeState.Omega',
'MoleculeQNN':'MoleculeState.rotN',
'MoleculeQNElecStateLabel':'MoleculeState.elecstate',
'MoleculeQNJ':'MoleculeState.j_fmt()',
'MoleculeQNS':'MoleculeState.s',
'MoleculeQnParity':'MoleculeState.parity_pm()',
'MoleculeQNkronigParity':'MoleculeState.kronig_parity',
'MoleculeQNelecInv':'MoleculeState.elec_inversion',
'MoleculeQNasSym':'MoleculeState.asSym',

#############################################################
'RadTransID':'RadTran.id',
'RadTransSpeciesRef':'RadTran.species_id',
'RadTransWavelength':'RadTran.get_waves()',
'RadTransWavelengthComment': 'RadTran.get_wave_comments()',
'RadTransWavelengthRef':'RadTran.get_wave_refs()',
'RadTransWavelengthUnit':u'A',
'RadTransWavelengthMethod':'RadTran.get_wave_methods()',
#'RadTransProcess':"RadTran.transition_type",
'RadTransProcess':"excitation",
'RadTransUpperStateRef':'RadTran.upstate_id',
'RadTransLowerStateRef':'RadTran.lostate_id',
#'RadTransProbabilityA':'RadTran.einsteina',
'RadTransProbabilityLog10WeightedOscillatorStrength':'RadTran.loggf',
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

# Numerical accuracy (for E, C, P flags with calculated loggf_err)
'RadTransProbabilityLog10WeightedOscillatorStrengthAccuracy':'RadTran.loggf_err',
'RadTransProbabilityLog10WeightedOscillatorStrengthAccuracyType':'RadTran.get_accur_type()',
'RadTransProbabilityLog10WeightedOscillatorStrengthAccuracyRelative':'RadTran.get_accur_relative()',
# Quality evaluation (for N flag letter grades like A, AA+, D-, and other text in accur field)
'RadTransProbabilityLog10WeightedOscillatorStrengthEval':'RadTran.accur',
'RadTransProbabilityLog10WeightedOscillatorStrengthEvalComment':'RadTran.get_accur_comment()'
}

# import the converter functions
from vamdctap.unitconv import *

# custom function
from django.db.models import Q

# Helper functions for restrictables that can query both upper and lower states
def bothStates(qval):
    """Filter transitions where EITHER upper OR lower state matches the energy"""
    return Q(upstate__energy=qval) | Q(lostate__energy=qval)

def bothStates_lande(qval):
    """Filter transitions where EITHER upper OR lower state matches the Lande factor"""
    return Q(upstate__lande=qval) | Q(lostate__lande=qval)

def bothStates_parity(qval):
    """Filter transitions where EITHER upper OR lower state matches the parity"""
    return Q(upstate__p=qval) | Q(lostate__p=qval)

def bothStates_j(qval):
    """Filter transitions where EITHER upper OR lower state matches J"""
    return Q(upstate__j=qval) | Q(lostate__j=qval)

def bothStates_v(qval):
    """Filter transitions where EITHER upper OR lower state matches v (vibrational QN)"""
    return Q(upstate__v=qval) | Q(lostate__v=qval)

def bothStates_Lambda(qval):
    """Filter transitions where EITHER upper OR lower state matches Lambda"""
    return Q(upstate__Lambda=qval) | Q(lostate__Lambda=qval)

def valdObstype(qval):
    """Convert VAMDC method category string to VALD integer code"""
    method_map = {
        'experiment': 0, 'observed': 1, 'empirical': 2,
        'theory': 3, 'semiempirical': 4, 'compilation': 5,
        'derived': 6, 'ritz': 6
    }
    return method_map.get(qval.lower(), qval)

def loggf2osc(loggf_val):
    """Convert log(gf) to oscillator strength: f = 10^(loggf)"""
    return 10**float(loggf_val)

def loggf2wf(loggf_val):
    """Convert log(gf) to weighted oscillator strength: gf = 10^(loggf)"""
    return 10**float(loggf_val)

RESTRICTABLES = {\
#'ConstantTest':test_constant_factory('"U"'),

# Species identification (atoms)
'AtomSymbol':'species__name',
'AtomMassNumber':'species__massno',
'AtomNuclearCharge':'species__atomic',
'IonCharge':'species__ion',
'Inchi':'species__inchi',
'InchiKey':'species__inchikey',

# Species identification (molecules)
'MoleculeChemicalName':'species__name',
'MoleculeStoichiometricFormula':'species__name',
'SpeciesID':'species__id',

# State energy (both atoms and molecules)
'StateEnergy':bothStates,
'Lower.StateEnergy':'lostate__energy',
'Upper.StateEnergy':'upstate__energy',

# Atomic state properties
'AtomStateLandeFactor':bothStates_lande,
'Lower.AtomStateLandeFactor':'lostate__lande',
'Upper.AtomStateLandeFactor':'upstate__lande',
'AtomStateParity':bothStates_parity,
'Lower.AtomStateParity':'lostate__p',
'Upper.AtomStateParity':'upstate__p',
'AtomStateTotalAngMom':bothStates_j,
'Lower.AtomStateTotalAngMom':'lostate__j',
'Upper.AtomStateTotalAngMom':'upstate__j',

# Molecular quantum numbers
'MoleculeQNv':bothStates_v,
'Lower.MoleculeQNv':'lostate__v',
'Upper.MoleculeQNv':'upstate__v',
'MoleculeQNJ':bothStates_j,  # J is common to both atoms and molecules
'Lower.MoleculeQNJ':'lostate__j',
'Upper.MoleculeQNJ':'upstate__j',
'MoleculeQNLambda':bothStates_Lambda,
'Lower.MoleculeQNLambda':'lostate__Lambda',
'Upper.MoleculeQNLambda':'upstate__Lambda',

# Radiative transitions - wavelength/energy
'RadTransWavelength':'wave',
'RadTransWavenumber':('wave',invcm2Angstr),
'RadTransFrequency':('wave',Hz2Angstr),
'RadTransEnergy':('wave',eV2Angstr),

# Radiative transitions - probabilities
'RadTransProbabilityA':'einsteina',
'RadTransProbabilityLog10WeightedOscillatorStrength':'loggf',
'RadTransProbabilityOscillatorStrength':('loggf',loggf2osc),
'RadTransProbabilityWeightedOscillatorStrength':('loggf',loggf2wf),

# Radiative transitions - broadening
'RadTransBroadeningNatural':'gammarad',
'RadTransBroadeningPressure':'gammastark',
'RadTransBroadeningPressureCharged':'gammastark',
'RadTransBroadeningPressureNeutral':'gammawaals',

# Metadata
'MethodCategory':('wave_method',valdObstype),
}
