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

RETURNABLES = {\
'NodeID':'umist',
'XSAMSVersion':'1.0',

'SourceID':'Source.id',
'SourceAuthorName':'Source.authorlist',
'SourceCategory':'Source.category',
'SourcePageBegin':'Source.pagebegin',
'SourcePageEnd':'Source.pageend',
'SourceName':'Source.sourcename',
'SourceTitle':'Source.title',
'SourceURI':'Source.url',
'SourceVolume':'Source.volume',
'SourceYear':'Source.year',
'SourceDOI':'Source.doi',
'SourceComments':'Source.comments',

'CollisionUserDefinition':'CollTran.rt.type',
'CollisionThreshold':'CollTran.tmin',
'CollisionThresholdUnit':'K',
'CollisionThresholdComment':'Minimum temperature',
'CollisionProductSpecies':'Product.id',
'CollisionReactantSpecies':'Reactant.id',

'CollisionDataSetRef':'DataSet.Ref',
'CollisionDataSetDescription':'rateCoefficient',
# 2012-10-30 KWS Commented out TabulatedDataSets for the time being
#'CollisionTabulatedDataXDataList' : 'TabData.xdata',
#'CollisionTabulatedDataXUnits' : 'TabData.xdataunit',
#'CollisionTabulatedDataXParameter' : 'undef',
#'CollisionTabulatedDataYDataList' : 'TabData.ydata',
#'CollisionTabulatedDataYUnits' : 'TabData.ydataunit',
#'CollisionTabulatedDataYParameter' : 'undef',

# 2012-10-30 KWS Added functions. Unused features (so far) are left commented out.

'FunctionArgumentLowerLimit':'FunctionArgument.lower_limit',
'FunctionArgumentUpperLimit':'FunctionArgument.upper_limit',
'FunctionArgumentDescription':'FunctionArgument.description',
'FunctionArgumentName':'FunctionArgument.name',
'FunctionArgumentUnits':'FunctionArgument.units',
'FunctionParameterDescription':'FunctionParameter.description',
'FunctionParameterName':'FunctionParameter.name',
'FunctionParameterUnits':'FunctionParameter.units',
#'FunctionSourceRef':'Function.sourceref',

'FunctionComputerLanguage':'Function.computer_language',
'FunctionExpression':'Function.expression',
'FunctionID':'Function.id',
'FunctionName':'Function.name',
'FunctionYName':'Function.y_name',
'FunctionYUnits':'Function.y_units',
#'FunctionYDescription':'',
#'FunctionReferenceFrame':'',
#'FunctionSourceCodeURL':'',
#'FunctionSourceRef':'',
#'FunctionYLowerLimit':'',
#'FunctionYUpperLimit':'',

# 2012-10-23 KWS Added fitfunction data

'CollisionFitDataMethod':'FitData.clem',
'CollisionFitDataAccuracy':'FitData.acc',
'CollisionFitDataFunction' : 'FitData.functionref',
'CollisionFitDataArgumentName' : 'T',
'CollisionFitDataArgumentUnits' : 'K',
'CollisionFitDataArgumentDescription' : 'Argument.description',
'CollisionFitDataArgumentLowerLimit' : 'Argument.tmin',
'CollisionFitDataArgumentUpperLimit' : 'Argument.tmax',

'CollisionFitDataParameter' : 'Parameter.parameter',
'CollisionFitDataParameterName' : 'Parameter.names',
'CollisionFitDataParameterUnit' : 'Parameter.units',

# 2012-10-31 KWS Added Methods

'MethodCategory':'Method.category',
'MethodDescription':'Method.description',
'MethodID':'Method.name',

# 2012-02-09 KWS Added collision ID
'CollisionID' : 'CollTran.id',

#    'CollTran.dipole,

'AtomSpeciesID':'Atom.id',
'AtomInchi':'Atom.inchi',
'AtomInchiKey':'Atom.inchikey',
'AtomNuclearCharge':'Atom.nuclear_charge',
'AtomIonCharge':'Atom.charge',
'AtomSymbol':'Atom.stoic_no_charge',

'MoleculeSpeciesID':'Molecule.id',
'MoleculeInChI':'Molecule.inchi',
'MoleculeInChIKey':'Molecule.inchikey',
'MoleculeOrdinaryStructuralFormula':'Molecule.struct_name',
'MoleculeVAMDCSpeciesID':'Molecule.vamdc_species_id',
'MoleculeMolecularWeight':'Molecule.mass',
'MoleculeStoichiometricFormula':'Molecule.stoic_formula',

'ParticleName':'Particle.comments',
'ParticleSpeciesID':'Particle.id',
'ParticleCharge':'Particle.charge',
'ParticleComment':'Particle.names',

}

# The restrictable dictionary defines limitations to the search. 
# The left-hand side is standardized, the righ-hand size should
# be defined in Django query-language style, where e.g. a search
# for the Species.atomic field  would be written as species__atomic.

RESTRICTABLES = {\
'MoleculeInChIKey':'reaction__species__inchikey',
'InchiKey':'reaction__species__inchikey',
'MoleculeInChI':'reaction__species__inchi',
'MoleculeChemicalName':'reaction__species__names',
'VAMDCSpeciesID':'reaction__species__vamdc_species_id',
'MoleculeStoichiometricFormula':'reaction__species__stoic_formula',
#'MoleculeChemicalName':'',
#'MoleculeOrdinaryStructuralFormula':'',
}

