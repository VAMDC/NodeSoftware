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

from vamdctap.caselessdict import CaselessDict
from vamdctap.unitconv import *

import logging
log1=logging.getLogger('vamdc.node.dictionary')

def checkOzone(restrictable,operator,value):
    value = value.strip('\'"')
    if value in ('Ozone','ozone','O3','o3') and operator in ('=','=='):
        log1.debug('Oz keka')   
        return Q(pk=F('pk'))
    else:
        log1.debug('Oz kaka')   
        return ~Q(pk=F('pk'))

def checkO3(restrictable,operator,value):
    value = value.strip('\'"')
    if value in ('O3','o3') and operator in ('=','=='):
        log1.debug('O3 keka')   
        return Q(pk=F('pk'))
    else:
        log1.debug('O3 kaka')   
        return ~Q(pk=F('pk'))

def checkZero(restrictable,operator,value):
    value = value.strip('\'"')
    log1.debug(value)   
    if int(value) == 0 and operator in ('=','==','>=','<='):
        log1.debug('Zero keka')   
        return Q(pk=F('pk'))
    else:
        log1.debug('Zero kaka')   
        return ~Q(pk=F('pk'))

RETURNABLES = CaselessDict({\
'NodeID':'GSMA-SMPO',

'SourceID':'Source.SourceID',
'SourceAuthorName':'Source.authorlist()',
'SourceCategory':'Source.SourceCategory',
'SourcePageBegin':'Source.SourcePageBegin',
'SourcePageEnd':'Source.SourcePageEnd',
'SourceName':'Source.SourceName',
'SourceTitle':'Source.SourceTitle',
'SourceURI':'Source.SourceURI',
'SourceVolume':'Source.SourceVolume',
'SourceYear':'Source.SourceYear',  

###########################################################################                                                            

'MethodID': 'Method.id',
'MethodCategory': 'Method.category',
'MethodDescription': 'Method.description',

'FunctionID': 'Function.id',
'FunctionName': 'Function.name',
'FunctionComputerLanguage': 'Function.clang',
'FunctionExpression': 'Function.expr',
'FunctionDescription': 'Function.descr',
'FunctionYName': 'Function.yname',
'FunctionYUnits': 'Function.yunits',
'FunctionYDescription': 'Function.ydescr',
'FunctionArgumentName': 'FunctionArgument.name',
'FunctionArgumentUnits': 'FunctionArgument.units',
'FunctionArgumentDescription': 'FunctionArgument.descr',
'FunctionArgumentLowerLimit': 'FunctionArgument.low',
'FunctionArgumentUpperLimit': 'FunctionArgument.up',
'FunctionParameterName': 'FunctionParameter.name',
'FunctionParameterUnits': 'FunctionParameter.units',
'FunctionParameterDescription': 'FunctionParameter.descr',

'EnvironmentID': 'Environment.id',
'EnvironmentTemperature': 'Environment.temperature',
'EnvironmentTemperatureUnit': 'K',
'EnvironmentTotalPressure': 'Environment.pressure',
'EnvironmentTotalPressureUnit': 'atm',
'EnvironmentSpeciesName': 'EnvSpecies.name',
'EnvironmentSpeciesMoleFraction': 'EnvSpecies.fraction',
#'EnvironmentSpeciesRef': 'NONE',

###########################################################################                                                            

'RadTransWavenumber':'RadTran.wn',
'RadTransWavenumberUnit':'1/cm',
'RadTransWavenumberRef':'RadTran.ref_wn',
'RadTransWavenumberComment':'',
'RadTransWavenumberMethod':'',
'RadTransWavenumberAccuracy':'RadTran.dwn',
'RadTransWavenumberAccuracyType':'statistical',
'RadTransWavenumberAccuracyRelative':'1',
'RadTransWavenumberAccuracyStatisticalRelative':'RadTran.dwn',

'RadTransEnergy':'RadTran.elow',
'RadTransEnergyUnit':'1/cm',
'RadTransEnergyRef':'RadTran.ref_e',
'RadTransEnergyComment':'Lower state energy',

'RadTransProbabilityLineStrength':'RadTran.s',
'RadTransProbabilityLineStrengthUnit':'1/cm2/atm',
'RadTransProbabilityLineStrengthRef':'RadTran.ref_s',
'RadTransProbabilityLineStrengthMethod':'',
'RadTransProbabilityLineStrengthAccuracy':'RadTran.dint',
'RadTransProbabilityLineStrengthAccuracyType':'statistical',
'RadTransProbabilityLineStrengthAccuracyRelative':'1',
'RadTransProbabilityLineStrengthAccuracyStatisticalRelative':'RadTran.dint',
'RadTransProbabilityA':'RadTran.ae',
'RadTransProbabilityAUnit':'1/s',

#'RadTransBroadeningPressureLineshapeParameterName':'SelfBroadening',
#'RadTransBroadeningPressureLineshapeParameter':'RadTran.hwhms',
#'RadTransBroadeningPressureLineshapeParameterUnit':'1/cm', 
#'RadTransBroadeningPressureLineshapeParameterRef':'',
#'RadTransBroadeningPressureLineshapeParameterComment':'',
#'RadTransBroadeningPressureLineshapeParameterMethod':'',

'RadTransFrequency':'',
'RadTransFrequencyUnit':'',
'RadTransFrequencyRef':'',
'RadTransFrequencyComment':'',

'RadTransFinalStateRef':'RadTran.getStateRefUp()',
'RadTransInitialStateRef':'RadTran.getStateRefLow()',
'RadTransID':'RadTran.getTranId()',

#######################################################################

'MoleculeChemicalName':'Ozone',
'MoleculeStoichiometricFormula':'O3',
'MoleculeOrdinaryStructuralFormula':'Molecule.formula',
'MoleculeSpeciesID':'Molecule.nnn',
'MoleculeInChI':'Molecule.inchi', 
'MoleculeInChIKey':'Molecule.inchikey', 
'MoleculeStateID':'MoleculeState.id',
'MoleculeStateEnergy':'MoleculeState.energy',
'MoleculeStateEnergyOrigin':'Zero-point energy',
'MoleculeStateEnergyUnit':'1/cm',
'MoleculeStateEnergyRef':'',
'MoleculeStateEnergyComment':'',
'MoleculeStateEnergyMethod':'',
#'MoleculeStateEnergyAccuracy':'0.01',
'MoleculeMolecularWeight':'Molecule.mass',
'MoleculeMolecularWeightUnit':'au',
'MoleculeMolecularWeightRef':'Molecule.ref_mass',
'MoleculePartitionFunctionT':'Molecule.pft',
'MoleculePartitionFunction':'Molecule.pfv',
'MoleculeIonCharge':'0',
'MoleculeQnCase':'nltcs',
'MoleculeQNElecStateLabel':'X',
'MoleculeQNv1':'MoleculeState.v1',
'MoleculeQNv2':'MoleculeState.v2',
'MoleculeQNv3':'MoleculeState.v3',
'MoleculeQNJ':'MoleculeState.j',
'MoleculeQNKa':'MoleculeState.ka',
'MoleculeQNKc':'MoleculeState.kc',
'MoleculeNormalModeID':'NormalMode.id',
'MoleculeNormalModePointGroupSymmetry':'NormalMode.sy',
'MoleculeNormalModeHarmonicFrequency':'NormalMode.hf',
'MoleculeNormalModeHarmonicFrequencyUnit':'1/cm',
'MoleculeNormalModeIntensity':''
})

# The restrictable dictionary defines limitations to the search. 
# The left-hand side is standardized, the righ-hand size should
# be defined in Django query-language style, where e.g. a search
# for the Species.atomic field  would be written as species__atomic.

RESTRICTABLES = CaselessDict({\

'RadTransWavenumber':'wn',
'RadTransWavelength':('wn',invcm2Angstr),
'RadTransProbabilityA':'ae',
'RadTransProbabilityLineStrength':'s',

'MoleculeChemicalName':checkOzone,
'MoleculeStoichiometricFormula':checkO3,
'MoleculeInChI':'isotid__inchi', 
'MoleculeInChIKey':'isotid__inchikey',
#'MoleculeInChIKey':'inchikey',
'upper.StateEnergy':'eup',
'lower.StateEnergy':'elow',
'StateEnergy':'elow',
#'IonCharge':checkZero
})

