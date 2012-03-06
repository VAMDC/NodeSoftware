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
from nodes.wadis.node import transforms


def dataTypeDict(physicalMagnitudes):
	linearDict = {}
	for physicalMagnitude, values in physicalMagnitudes.items():
		if type(values) is dict:
			if 'Value' in values:
				linearDict[physicalMagnitude] = values['Value']
			else:
				continue
			if 'Unit' in values:
				linearDict[physicalMagnitude + 'Unit'] = values['Unit']
			if 'Ref' in values:
				linearDict[physicalMagnitude + 'Ref'] = values['Ref']
			if 'Comment' in values:
				linearDict[physicalMagnitude + 'Comment'] = values['Comment']
			if 'Method' in values:
				linearDict[physicalMagnitude + 'Method'] = values['Method']
			if 'Accuracy' in values:
				linearDict[physicalMagnitude + 'Accuracy'] = values['Accuracy']
			if 'AccuracyConfidence' in values:
				linearDict[physicalMagnitude + 'AccuracyConfidence'] = values['AccuracyConfidence']
			if 'AccuracyRelative' in values:
				#default="false"
				linearDict[physicalMagnitude + 'AccuracyRelative'] = values['AccuracyRelative']
			if 'AccuracyType' in values:
				#default="arbitrary"
				linearDict[physicalMagnitude + 'AccuracyType'] = values['AccuracyType']
			if 'Eval' in values:
				linearDict[physicalMagnitude + 'Eval'] = values['Eval']
			if 'EvalMethod' in values:
				linearDict[physicalMagnitude + 'EvalMethod'] = values['EvalMethod']
			if 'EvalRecommended' in values:
				linearDict[physicalMagnitude + 'EvalRecommended'] = values['EvalRecommended']
			if 'EvalRef' in values:
				linearDict[physicalMagnitude + 'EvalRef'] = values['EvalRef']
			if 'EvalComment' in values:
				linearDict[physicalMagnitude + 'EvalComment'] = values['EvalComment']
		else:
			linearDict[physicalMagnitude] = values
	return linearDict


RETURNABLES = {#
	#http://www.vamdc.eu/documents/standards/dictionary/returnables.html
	#http://dictionary.vamdc.org/returnables/
	# see return queryfunc.setupResults
	'NodeID': 'wadis',
	}

moleculeReturnables = {#
	# see http://vamdc.org/documents/standards/dataModel/vamdcxsams/speciesMolecules.html
	#'MoleculeCASRegistryNumber' : '',
	#'MoleculeCNPIGroup' : '',
	'MoleculeChemicalName' : 'Molecule.englishName',
	'MoleculeComment' : 'Molecule.plain_name',
	#'MoleculeIUPACName' : '',
	'MoleculeInchi' : 'Molecule.id_inchi',
	'MoleculeInchiKey' : 'Molecule.id_inchi_key',
	'MoleculeIonCharge' : 'Molecule.getCharge()',
	'MoleculeMolecularWeight' : {'Value': 'Molecule.weight', 'Unit': 'amu'},
	#'MoleculeNormalModeDisplacementVectorComment' : '',
	#'MoleculeNormalModeDisplacementVectorMethod' : '',
	#'MoleculeNormalModeDisplacementVectorRef' : '',
	#'MoleculeNormalModeDisplacementVectorSourceRef' : '',
	#'MoleculeNormalModeDisplacementVectorX' : '',
	#'MoleculeNormalModeDisplacementVectorY' : '',
	#'MoleculeNormalModeDisplacementVectorZ' : '',
	#'MoleculeNormalModeElectronicState' : '',
	#'MoleculeNormalModeHarmonicFrequency' : {},
	#'MoleculeNormalModeID' : '',
	#'MoleculeNormalModeIntensity' : {},
	#'MoleculeNormalModeMethod' : '',
	#'MoleculeNormalModePointGroupSymmetry' : '',
	#'MoleculeNormalModeRef' : '',
	#'MoleculeNuclearSpins' : '',
	#'MoleculeNuclearSpinsAtomArray' : '',
	#'MoleculeNuclearSpinsBondArray' : '',
	'MoleculeOrdinaryStructuralFormula' : 'Molecule.getLatexFormula()', #Standard formula describing the chemical complex written in Latex.
	#'MoleculeQNElecStateLabel' : '',
	#'MoleculeQNF' : '',
	#'MoleculeQNF1' : '',
	#'MoleculeQNF1nuclSpin' : '',
	#'MoleculeQNF2' : '',
	#'MoleculeQNF2nuclSpin' : '',
	#'MoleculeQNFj' : '',
	#'MoleculeQNFjj' : '',
	#'MoleculeQNFjnuclSpin' : '',
	#'MoleculeQNFnuclSpin' : '',
	#'MoleculeQNI' : '',
	#'MoleculeQNInuclSpin' : '',
	'MoleculeQNJ' : 'MoleculeState.J',
	#'MoleculeQNK' : '',
	'MoleculeQNKa' : 'MoleculeState.Ka',
	'MoleculeQNKc' : 'MoleculeState.Kc',
	#'MoleculeQNLambda' : '',
	#'MoleculeQNN' : '',
	#'MoleculeQNOmega' : '',
	#'MoleculeQNS' : '',
	#'MoleculeQNSigma' : '',
	#'MoleculeQNSpinComponentLabel' : '',
	#'MoleculeQNasSym' : '',
	#'MoleculeQNelecInv' : '',
	#'MoleculeQNelecRefl' : '',
	#'MoleculeQNkronigParity' : '',
	#'MoleculeQNl' : '',
	#'MoleculeQNl2' : '',
	#'MoleculeQNli' : '',
	#'MoleculeQNliMode' : '',
	#'MoleculeQNparity' : '',
	#'MoleculeQNr' : '',
	#'MoleculeQNrName' : '',
	#'MoleculeQNrotSym' : '',
	#'MoleculeQNrotSymGroup' : '',
	#'MoleculeQNv' : '',
	'MoleculeQNv1' : 'MoleculeState.v1',
	'MoleculeQNv2' : 'MoleculeState.v2',
	'MoleculeQNv3' : 'MoleculeState.v3',
	#'MoleculeQNvi' : '',
	#'MoleculeQNviMode' : '',
	#'MoleculeQNvibInv' : '',
	#'MoleculeQNvibRefl' : '',
	#'MoleculeQNvibSym' : '',
	#'MoleculeQNvibSymGroup' : '',
	'MoleculeQnCase' : 'MoleculeState.case',
	'MoleculeSpeciesID' : 'Molecule.id_inchi_key',
	#'MoleculeStableMolecularProperties' : '',
	#'MoleculeStateDescription' : '',
	'MoleculeStateEnergy' : {'Value': 'MoleculeState.energy', 'Unit': '1/cm', 'Accuracy': 'MoleculeState.energy_delta', 'AccuracyType': 'statistical', 'Method':'MoleculeState.id_energy_ds.getMethod()'},
	'MoleculeStateEnergyOrigin' : 'Zero-point energy',
	'MoleculeStateID' : 'MoleculeState.id',
	#'MoleculeStateLifeTime' : {},
	#'MoleculeStateMixingCoefficient' : '',
	#'MoleculeStateNuclearSpinIsomer' : '',
	#'MoleculeStateNuclearStatisticalWeight' : '',
	#'MoleculeStateParameterMatrix' : '',
	#'MoleculeStateParameterMatrixColRefs' : '',
	#'MoleculeStateParameterMatrixForm' : '',
	#'MoleculeStateParameterMatrixNcols' : '',
	#'MoleculeStateParameterMatrixNrows' : '',
	#'MoleculeStateParameterMatrixRowRefs' : '',
	#'MoleculeStateParameterMatrixUnits' : '',
	#'MoleculeStateParameterMatrixValues' : '',
	#'MoleculeStateParameterValueData' : {},
	#'MoleculeStateParameterVectorDataUnits' : '',
	#'MoleculeStateParameterVectorRef' : '',
	#'MoleculeStateParameterVectorX' : '',
	#'MoleculeStateParameterVectorY' : '',
	#'MoleculeStateParameterVectorZ' : '',
	#'MoleculeStateParameters' : '',
	#'MoleculeStateQuantumNumbers' : '',
	#'MoleculeStateTotalStatisticalWeight' : '',
	'MoleculeStoichiometricFormula' : 'Molecule.getABCFormula()', #An alphabetical suite of the atomic constituents followed by the total number of their occurence.
	#'MoleculeStructure' : '',
	#'MoleculeURLFigure' : '',
}
RETURNABLES.update(moleculeReturnables)

radTransReturnables = {#
	#'RadTransBandCentre' : {},
	#'RadTransBandWidth' : {},
	#'RadTransBroadeningDopplerComment' : '',
	#'RadTransBroadeningDopplerEnvironment' : '',
	#'RadTransBroadeningDopplerLineshapeName' : '',
	#'RadTransBroadeningDopplerLineshapeParameter' : {},
	#'RadTransBroadeningDopplerLineshapeParameterName' : '',
	#'RadTransBroadeningDopplerMethod' : '',
	#'RadTransBroadeningDopplerRef' : '',
	#'RadTransBroadeningInstrumentComment' : '',
	#'RadTransBroadeningInstrumentEnvironment' : '',
	#'RadTransBroadeningInstrumentLineshapeName' : '',
	#'RadTransBroadeningInstrumentLineshapeParameter' : {},
	#'RadTransBroadeningInstrumentLineshapeParameterName' : '',
	#'RadTransBroadeningInstrumentMethod' : '',
	#'RadTransBroadeningInstrumentRef' : '',
	#'RadTransBroadeningNaturalComment' : '',
	#'RadTransBroadeningNaturalEnvironment' : '',
	#'RadTransBroadeningNaturalLineshapeName' : '',
	#'RadTransBroadeningNaturalLineshapeParameter' : {},
	#'RadTransBroadeningNaturalLineshapeParameterName' : '',
	#'RadTransBroadeningNaturalMethod' : '',
	#'RadTransBroadeningNaturalRef' : '',
	#'RadTransBroadeningPressureComment' : '',
	#'RadTransBroadeningPressureEnvironment' : '',
	#'RadTransBroadeningPressureLineshapeName' : '',
	#'RadTransBroadeningPressureLineshapeParameter' : {},
	#'RadTransBroadeningPressureLineshapeParameterName' : '',
	#'RadTransBroadeningPressureMethod' : '',
	#'RadTransBroadeningPressureRef' : '',
	#'RadTransComment' : '',
	#'RadTransEffectiveLandeFactor' : {},
	#'RadTransEnergy' : {},
	#'RadTransFrequency' : {},
	#'RadTransGroup' : '',
	'RadTransID': 'RadTran.id_transition',
	'RadTransLowerStateRef' : 'RadTran.low',
	'RadTransProbabilityA': {'Value': 'RadTran.einstein_coefficient', 'Unit': '1/s', 'Accuracy': 'RadTran.einstein_coefficient_err', 'AccuracyType': 'statistical', 'Method':'RadTran.id_transition_ds.getMethod()'},
	#No cm2molec-1cm-1 or cm-1/(molecule×cm-2) units in XSAMS
	'RadTransProbabilityIdealisedIntensity' : {'Value': 'RadTran.intensity', 'Comment': u'cm-1/(molecule×cm-2)', 'Unit':'undef', 'Accuracy': 'RadTran.intensity_err', 'AccuracyType': 'statistical', 'Method':'RadTran.id_transition_ds.getMethod()'},
	#'RadTransProbabilityKind' : '',
	#'RadTransProbabilityLineStrength' : {},
	#'RadTransProbabilityLog' : {},
	#'RadTransProbabilityOscillatorStrength' : {},
	#'RadTransProbabilityWeightedOscillatorStrength' : {},
	#'RadTransProcess' : '',
	'RadTransRefs' : 'RadTran.id_transition_ds.id_biblio',
	#'RadTransShifting' : '',
	#'RadTransShiftingComment' : '',
	#'RadTransShiftingEnv' : '',
	#'RadTransShiftingMethod' : '',
	#'RadTransShiftingName' : '',
	#'RadTransShiftingParam' : {},
	#'RadTransShiftingParamFitArgumentDescription' : '',
	#'RadTransShiftingParamFitArgumentLowerLimit' : '',
	#'RadTransShiftingParamFitArgumentName' : '',
	#'RadTransShiftingParamFitArgumentUnits' : '',
	#'RadTransShiftingParamFitArgumentUpperLimit' : '',
	#'RadTransShiftingParamFitFunction' : '',
	#'RadTransShiftingParamFitParameter' : {},
	#'RadTransShiftingParamFitParameterName' : '',
	#'RadTransShiftingParamName' : '',
	#'RadTransShiftingRef' : '',
	#'RadTransSpeciesRef' : '',
	'RadTransUpperStateRef' : 'RadTran.up',
	#'RadTransWavelength' : {},
	'RadTransWavenumber': {'Value': 'RadTran.wavenumber', 'Unit': '1/cm', 'Accuracy': 'RadTran.wavenumber_err', 'AccuracyType': 'statistical', 'Method':'RadTran.id_transition_ds.getMethod()'},
	}
RETURNABLES.update(radTransReturnables)

environmentReturnables = {#
	#'EnvironmentComment' : '',
	#'EnvironmentID' : '',
	#'EnvironmentRef' : '',
	#'EnvironmentSpecies' : '',
	#'EnvironmentSpeciesConcentration' : {},
	#'EnvironmentSpeciesMoleFraction' : {},
	#'EnvironmentSpeciesName' : '',
	#'EnvironmentSpeciesPartialPressure' : {},
	#'EnvironmentSpeciesRef' : '',
	#'EnvironmentTemperature' : {},
	#'EnvironmentTotalNumberDensity' : {},
	#'EnvironmentTotalPressure' : {},
}
RETURNABLES.update(environmentReturnables)

functionReturnables = {#
	#'FunctionArgumentDescription' : '',
	#'FunctionArgumentLowerLimit' : '',
	#'FunctionArgumentName' : '',
	#'FunctionArgumentUnits' : '',
	#'FunctionArgumentUpperLimit' : '',
	#'FunctionComputerLanguage' : '',
	#'FunctionDescription' : '',
	#'FunctionExpression' : '',
	#'FunctionID' : '',
	#'FunctionName' : '',
	#'FunctionParameterDescription' : '',
	#'FunctionParameterName' : '',
	#'FunctionParameterUnits' : '',
	#'FunctionReferenceFrame' : '',
	#'FunctionSourceCodeURL' : '',
	#'FunctionSourceRef' : '',
	#'FunctionYDescription' : '',
	#'FunctionYLowerLimit' : '',
	#'FunctionYName' : '',
	#'FunctionYUnits' : '',
	#'FunctionYUpperLimit' : '',
}
RETURNABLES.update(functionReturnables)

methodReturnables = {#
	'MethodCategory' : 'Method.category',
	#'MethodComment' : '',
	'MethodDescription' : 'Method.description',
	'MethodID' : 'Method.id',
	#'MethodRef' : '',
}
RETURNABLES.update(methodReturnables)

sourceReturnables = {#
	#Only these elements is handled the generator
	#Xsams-schema contains another more elements
	'SourceArticleNumber' : 'Source.getArticleNumber()',
	'SourceAuthorName' : 'Source.getAuthorList()',
	'SourceCategory' : 'Source.biblioTypeName',
	'SourceComments' : 'Source.biblioannotation',
	'SourceDOI' : 'Source.bibliodoi',
	'SourceID' : 'Source.biblioid',
	'SourceName' : 'Source.getSourceName()',
	'SourcePageBegin' : 'Source.getPageBegin()',
	'SourcePageEnd' : 'Source.getPageEnd()',
	'SourceTitle' : 'Source.biblioname',
	'SourceURI' : 'Source.bibliourl',
	'SourceVolume' : 'Source.bibliovolume',
	'SourceYear' : 'Source.biblioyear',
}
RETURNABLES.update(sourceReturnables)

RETURNABLES = dataTypeDict(RETURNABLES)

# The restrictable dictionary defines limitations to the search. 
# The left-hand side is standardized, the righ-hand size should
# be defined in Django query-language style, where e.g. a search
# for the Species.atomic field  would be written as species__atomic.

RESTRICTABLES = {#
	#ONLY wadis in transforms.py
	'inner.id_substance': 'id_substance',
	'inner.type': 'id_%s_ds__type',
	#COMMON
	#Samples: 'X':'frequency', 'X':('frequency',eV2MHz), 'X':frequencyFunction
	#http://www.vamdc.eu/documents/standards/dictionary/restrictables.html
	#http://dictionary.vamdc.org/restrictables/
	#'AsOfDate' : '',
	#'AtomMass' : '',
	#'AtomMassNumber' : '',
	#'AtomNuclearCharge' : '',
	#'AtomNuclearSpin' : '',
	#'AtomStateCoupling' : '',
	#'AtomStateHyperfineMomentum' : '',
	#'AtomStateIonizationEnergy' : '',
	#'AtomStateKappa' : '',
	#'AtomStateLandeFactor' : '',
	#'AtomStateMagneticQuantumNumber' : '',
	#'AtomStateParity' : '',
	#'AtomStatePolarizability' : '',
	#'AtomStateQuantumDefect' : '',
	#'AtomStateTotalAngMom' : '',
	#'AtomSymbol' : '',
	#'CollisionCode' : '',
	#'CollisionIAEACode' : '',
	#'EnvironmentSpeciesConcentration' : '',
	#'EnvironmentSpeciesMoleFraction' : '',
	#'EnvironmentSpeciesPartialPressure' : '',
	#'EnvironmentTemperature' : '',
	#'EnvironmentTotalNumberDensity' : '',
	#'EnvironmentTotalPressure' : '',
	#'FunctionID' : '',
	#'FunctionName' : '',
	'Inchi' : transforms.inchi2Id,
	'InchiKey': transforms.inchiKey2Id,
	#'IonCharge' : '',
	'MethodCategory' : transforms.methodCategory2Type,
	#'MoleculeChemicalName' : '', #See VAMDC XSAMS-schema documentation. The ChemicalName element can not be used for search.
	#'MoleculeMolecularWeight' : '',
	#'MoleculeNormalModeHarmonicFrequency' : '',
	#'MoleculeProtonation' : '',
	#'MoleculeQNJ' : '',
	#'MoleculeQNK' : '',
	#'MoleculeQNKa' : '',
	#'MoleculeQNKc' : '',
	#'MoleculeQNv' : '',
	#'MoleculeQNv' : '',
	#'MoleculeQNv' : '',
	#'MoleculeQNv' : '',
	#'MoleculeStateNuclearSpinIsomer' : '',
	#'MoleculeStoichiometricFormula' : '',
	#'NonRadTranEnergy' : '',
	#'NonRadTranProbability' : '',
	#'NonRadTranWidth' : '',
	#'ParticleName' : '',
	#'Pressure' : '',
	#'RadTransBandCentre' : '',
	#'RadTransBandWidth' : '',
	#'RadTransBroadeningDoppler' : '',
	#'RadTransBroadeningInstrument' : '',
	#'RadTransBroadeningNatural' : '',
	#'RadTransBroadeningPressure' : '',
	#'RadTransEffectiveLandeFactor' : '',
	#'RadTransEnergy' : '',
	#'RadTransFrequency' : '',
	'RadTransProbabilityA' : 'einstein_coefficient',
	'RadTransProbabilityIdealisedIntensity' : 'intensity',
	#'RadTransProbabilityLineStrength' : '',
	#'RadTransProbabilityLog' : '',
	#'RadTransProbabilityOscillatorStrength' : '',
	#'RadTransProbabilityWeightedOscillatorStrength' : '',
	#'RadTransWavelength' : '',
	'RadTransWavenumber': 'wavenumber',
	#'SourceCategory' : '',
	#'SourceYear' : '',
	'StateEnergy' : 'energy',
	#'StateLifeTime' : '',
	#'StateStatisticalWeight' : '',
	#'Temperature' : '',
}
