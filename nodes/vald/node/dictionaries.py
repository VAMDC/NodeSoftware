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
from math import log10
from django.db.models import Q, F, Value, FloatField, ExpressionWrapper
from django.db.models.functions import Log

# Restrictable functions are called by vamdctap.sqlparse as fu(name, op, *values)
# and return a Q. restriction2Q is imported late because sqlparse imports this module.

def bothStates(field):
    """EITHER upper OR lower state matches"""
    def restrict(r, op, *rhs):
        from vamdctap.sqlparse import restriction2Q
        return restriction2Q([r, op, *rhs], {r: 'upstate__'+field}) \
             | restriction2Q([r, op, *rhs], {r: 'lostate__'+field})
    return restrict

METHOD_MAP = {
    'experiment': 0, 'observed': 1, 'empirical': 2,
    'theory': 3, 'semiempirical': 4, 'compilation': 5,
    'derived': 6, 'ritz': 6
}

def methodCategory(r, op, *rhs):
    """VAMDC method category string to VALD integer code"""
    from vamdctap.sqlparse import restriction2Q
    rhs = [str(METHOD_MAP.get(v.strip('\'"').lower(), v)) for v in rhs]
    return restriction2Q([r, op, *rhs], {r: 'wave_method'})

# stands in for log10(0), below any loggf in VALD
LOGGF_MIN = -99999

def _log10(v):
    v = float(v.strip('\'"'))
    return log10(v) if v > 0 else LOGGF_MIN

def weightedOscStrength(r, op, *rhs):
    """gf restriction applied to loggf"""
    from vamdctap.sqlparse import restriction2Q
    rhs = [v if v in '()' else repr(_log10(v)) for v in rhs]
    return restriction2Q([r, op, *rhs], {r: 'loggf'})

def oscStrength(r, op, *rhs):
    """f restriction applied to loggf, with g of the lower state"""
    from vamdctap.sqlparse import OPTRANS
    if len(rhs) != 1 or op not in ('<', '>', '<=', '>=', '=', '!=', '<>'):
        raise Exception('%s supports only a single value with <, >, <=, >=, =, !='%r)
    loggf = ExpressionWrapper(
        Value(_log10(rhs[0])) + Log(Value(10.0), 2*F('lostate__j') + 1),
        output_field=FloatField())
    if op in ('!=', '<>'):
        return ~Q(loggf=loggf)
    return Q(**{'loggf'+OPTRANS[op]: loggf})

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
'StateEnergy':bothStates('energy'),
'Lower.StateEnergy':'lostate__energy',
'Upper.StateEnergy':'upstate__energy',

# Atomic state properties
'AtomStateLandeFactor':bothStates('lande'),
'Lower.AtomStateLandeFactor':'lostate__lande',
'Upper.AtomStateLandeFactor':'upstate__lande',
'AtomStateParity':bothStates('p'),
'Lower.AtomStateParity':'lostate__p',
'Upper.AtomStateParity':'upstate__p',
'AtomStateTotalAngMom':bothStates('j'),
'Lower.AtomStateTotalAngMom':'lostate__j',
'Upper.AtomStateTotalAngMom':'upstate__j',

# Molecular quantum numbers
'MoleculeQNv':bothStates('v'),
'Lower.MoleculeQNv':'lostate__v',
'Upper.MoleculeQNv':'upstate__v',
'MoleculeQNJ':bothStates('j'),  # J is common to both atoms and molecules
'Lower.MoleculeQNJ':'lostate__j',
'Upper.MoleculeQNJ':'upstate__j',
'MoleculeQNLambda':bothStates('Lambda'),
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
'RadTransProbabilityOscillatorStrength':oscStrength,
'RadTransProbabilityWeightedOscillatorStrength':weightedOscStrength,

# Radiative transitions - broadening
'RadTransBroadeningNatural':'gammarad',
'RadTransBroadeningPressure':'gammastark',
'RadTransBroadeningPressureCharged':'gammastark',
'RadTransBroadeningPressureNeutral':'gammawaals',

# Metadata
'MethodCategory':methodCategory,
}
