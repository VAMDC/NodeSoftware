# -*- coding: utf-8 -*-
from vamdctap.caselessdict import CaselessDict
from vamdctap.unitconv import *

from ethylene.node.MyFunctions import *

RESTRICTABLES = CaselessDict({\
'RadTransWavenumber':'wavenumber',
'RadTransWavelength':('wavenumber',invcm2Angstr),
'RadTransProbabilityA':'einstein',
'RadTransProbabilityLineStrength':'intensity',

'MoleculeChemicalName':checkChemicalName,
'Inchi':'isotopeid__inchi',
'InchiKey':'isotopeid__inchikey',
'MoleculeStoichiometricFormula':checkStoichiometricFormula,
})

RETURNABLES = CaselessDict({\
'NodeID':'GSMA-C2H4',

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

'RadTransBroadeningPressureLineshapeParameterName':'SelfBroadening',
'RadTransBroadeningPressureLineshapeParameter':'RadTran.gamma1',
'RadTransBroadeningPressureLineshapeParameterUnit':'1/cm/atm',
'RadTransBroadeningPressureLineshapeParameterRef':'RadTran.gamma1_sourceid_id',
'RadTransBroadeningPressureLineshapeParameterAccuracy':'RadTran.gamma1_prec',

'RadTransUpperStateRef':'RadTran.upstateid_id',
'RadTransLowerStateRef':'RadTran.lowstateid_id',

'RadTransProbabilityA':'RadTran.einstein',
'RadTransProbabilityAUnit':'1/s',

'RadTransProbabilityKind':'RadTran.characid.renameCharacterisation()',
'RadTransProbabilityLineStrength':'RadTran.intensity',
'RadTransProbabilityLineStrengthUnit':'1/cm2/atm',
'RadTransProbabilityLineStrengthRef':'RadTran.intensity_sourceid_id',
'RadTransProbabilityLineStrengthAccuracy':'RadTran.intensity_prec',

##########################################################################

'MethodCategory':'theory',
'MethodDescription':'Method.name',
'MethodID':'Method.typeid',

##########################################################################

'MoleculeChemicalName':'ethylene',
'MoleculeOrdinaryStructuralFormula':'C2H4',
'MoleculeStoichiometricFormula':'H4C2',
'MoleculeSpeciesID': 'Molecule.isotopeid',
'MoleculeInchi':'Molecule.inchi',
'MoleculeInchiKey':'Molecule.inchikey',

'MoleculeStateID':'MoleculeState.stateid',
'MoleculeStateEnergy':'MoleculeState.position',
'MoleculeStateEnergyOrigin':'Zero-point energy',
'MoleculeStateEnergyUnit':'1/cm',
'MoleculeStateEnergyComment':'MoleculeState.PnJcn()',
'MoleculeStateTotalStatisticalWeight':'MoleculeState.weight',

})
