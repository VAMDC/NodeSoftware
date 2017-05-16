# -*- coding: utf-8 -*-
from requests.utils import CaseInsensitiveDict as CaselessDict
from vamdctap.unitconv import *

from ethylene.node.MyFunctions import *

RESTRICTABLES = CaselessDict({\
'RadTransWavenumber':'wavenumber',
'RadTransWavelength':('wavenumber',invcm2Angstr),
'RadTransProbabilityA':'einstein',
'RadTransProbabilityLineStrength':'intensity',

'MoleculeChemicalName':checkChemicalName,
'Inchi':'isotopeid__inchi',
'InchiKey':'inchikey',
'MoleculeStoichiometricFormula':checkStoichiometricFormula,
'upper.StateEnergy':'upstateid__position',
'lower.StateEnergy':'lowstateid__position',
'StateEnergy':'lowstateid__position',

'EnvironmentTemperature' : checkEnvironmentTemperature,
})

RETURNABLES = CaselessDict({\
'NodeID':'GSMA-C2H4',
'XSAMSVersion':'1.0',

'SourceID':'Source.sourceid',
'SourceAuthorName':'Source.extractRisVal("AU")',
'SourceCategory':'Source.extractRisVal("TY")',
'SourceName':'Source.extractRisVal("JO")',
'SourcePageBegin':'Source.extractRisVal("SP")',
'SourcePageEnd':'Source.extractRisVal("EP")',
'SourceTitle':'Source.extractRisVal("T1")',
'SourceDOI':'Source.extractRisVal("M1")',
'SourceVolume':'Source.extractRisVal("VL")',
'SourceYear':'Source.extractRisVal("PY")',

###################################################################

'RadTransID':'RadTran.transitionid',
'RadTransWavenumber':'RadTran.wavenumber',
'RadTransWavenumberUnit':'1/cm',
'RadTransWavenumberRef':'RadTran.wavenumber_sourceid_id',
'RadTransWavenumberMethod':'RadTran.typeid_id',
'RadTransWavenumberAccuracy':'RadTran.wavenumber_prec',
'RadTransWavenumberAccuracyType':'statistical',

'RadTransUpperStateRef':'RadTran.upstateid_id',
'RadTransLowerStateRef':'RadTran.lowstateid_id',

'RadTransProbabilityA':'RadTran.einstein',
'RadTransProbabilityAUnit':'1/s',

'RadTransProbabilityMultipole':'RadTran.characid.getMultipole()',
'RadTransProbabilityKind':'RadTran.characid.getTransitionKind()',
'RadTransProbabilityLineStrength':'RadTran.intensity',
'RadTransProbabilityLineStrengthUnit':'RadTran.characid.getUnit()',
'RadTransProbabilityLineStrengthRef':'RadTran.intensity_sourceid_id',
'RadTransProbabilityLineStrengthAccuracy':'RadTran.intensity_prec',
'RadTransProbabilityLineStrengthAccuracyType':'statistical',
'RadTransProbabilityLineStrengthAccuracyRelative':'true',

##########################################################################

'MethodCategory':'theory',
'MethodDescription':'Method.name',
'MethodID':'Method.typeid',

'EnvironmentID': '1',
'EnvironmentComment': 'Pressure and NumberDensity are not used in this data base',
'EnvironmentTemperature': '296',
'EnvironmentTemperatureUnit': 'K',

##########################################################################

'MoleculeChemicalName':'Ethylene,Ethene',
'MoleculeCASRegistryNumber':'Molecule.casregnum',
'MoleculeOrdinaryStructuralFormula':'C2H4',
'MoleculeOrdinaryStructuralFormula':'Molecule.formtex',
'MoleculeStoichiometricFormula':'H4C2',
'MoleculeSpeciesID': 'Molecule.isotopeid',
'MoleculeInchi':'Molecule.inchi',
'MoleculeInchiKey':'Molecule.inchikey',

'MoleculeStateID':'MoleculeState.stateid',
'MoleculeStateFullyAssigned':'true',
'MoleculeStateEnergy':'MoleculeState.position',
'MoleculeStateEnergyOrigin':'MoleculeState.isotopeid.eostateid',
'MoleculeStateEnergyUnit':'1/cm',
'MoleculeStateEnergyComment':'MoleculeState.PnPsn()',
'MoleculeStateTotalStatisticalWeight':'MoleculeState.weight',

'MoleculeStateExpansionCoeffStateRef':'MoleculeState.getBSID()',
'MoleculeStateExpansionCoeff':'MoleculeState.getCoef()',

'MoleculeStateQuantumNumbers':'',                       #'MoleculeStateQuantumNumbers':'MoleculeState',
'MoleculeQnCase':'sphcs',
'MoleculeQNJ':'MoleculeState.j',
'MoleculeQNrovibSym':'MoleculeState.symname',
'MoleculeQNrName':'alpha',
'MoleculeQNr':'MoleculeState.alpha',

'MoleculeBasisStates': 'Molecule.BasisStates',
'BasisStateID': 'MoleculeBasisState.sublevid',
'MoleculeBQNviMode':'MoleculeBasisState.getQNviMode()',
'MoleculeBQNvi':'MoleculeBasisState.getQNvi()',
'MoleculeBQNrName':'MoleculeBasisState.getQNrName()',
'MoleculeBQNr':'MoleculeBasisState.getQNr()',
'MoleculeBQNsymName':'MoleculeBasisState.getQNsymName()',
'MoleculeBQNsym':'MoleculeBasisState.getQNsym()',

})
