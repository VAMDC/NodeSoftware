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

'SourceID':'Source.abbr',
#'SourceAuthorName':'Source.author',
#'SourceCategory':'Source.category',
#'SourcePageBegin':'Source.pages',
#'SourcePageEnd':'Source.pages',
#'SourceName':'Source.journal',
'SourceTitle':'Source.full',
'SourceURI':'Source.url',
#'SourceVolume':'Source.volume',
#'SourceYear':'Source.year',

'CollisionThreshold':'CollTran.tmin',
'CollisionThresholdUnit':'K',
'CollisionThresholdComment':'Minimum temperature',
'CollisionProductSpecies':'Product.id',
'CollisionReactantSpecies':'Reactant.id',

# 2011-11-30 KWS Add table data.
# After conversations with C. Hill, we need to use fit parameters.
# DataFunctype -> FitParameters -> (FitArgument, FitParameter, FunctionRef)

'CollisionDataSetRef':'DataSet.Ref',
'CollisionDataSetDescription':'DataSet.Description',

'CollisionTabulatedDataXDataList' : 'TabData.xdata',
'CollisionTabulatedDataXUnits' : 'TabData.xdataunit',
'CollisionTabulatedDataXParameter' : 'undef',
'CollisionTabulatedDataYDataList' : 'TabData.ydata',
'CollisionTabulatedDataYUnits' : 'TabData.ydataunit',
'CollisionTabulatedDataYParameter' : 'undef',

# Range Limits - need Fit Function and new column in DB
# or derivation of which fit function to use from number
# and type of reactants.
#'CollisionTabulatedDataY':'CollTran.tmin',
#'CollisionTabulatedDataYDescription':'Tmin',
#'CollisionTabulatedDataX':'CollTran.tmax',
#'CollisionTabulatedDataXDescription':'Tmax',

#'CollisionTabulatedDataY':'CollTran.alpha',
#'CollisionTabulatedDataYDescription':'alpha',

#'CollisionTabulatedDataY':'CollTran.beta',
#'CollisionTabulatedDataYDescription':'beta',

#'CollisionTabulatedDataY':'CollTran.gamma',
#'CollisionTabulatedDataYDescription':'gamma',



# 2012-02-09 KWS Added collision ID
'CollisionID' : 'CollTran.id',


#    'CollTran.acc, # Need to interpret this and place in the correct keyword
#    'CollTran.clem,
#    'CollTran.dipole,

'AtomSpeciesID':'Atom.id',
'AtomInchi':'Atom.vamdc_inchi',
'AtomInchiKey':'Atom.vamdc_inchikey',

'MoleculeSpeciesID':'Molecule.id',
'MoleculeOrdinaryStructuralFormula':'Molecule.struct_name',

# 2012-01-25 KWS For the new standards we will use the ordinary standard
#                inchikey - not vamdc_inchikey
'MoleculeInChI':'Molecule.inchi',
'MoleculeInChIKey':'Molecule.inchikey',
}

# The restrictable dictionary defines limitations to the search. 
# The left-hand side is standardized, the righ-hand size should
# be defined in Django query-language style, where e.g. a search
# for the Species.atomic field  would be written as species__atomic.

RESTRICTABLES = {\
'MoleculeInChIKey':'reaction__species__inchikey',
'InchiKey':'reaction__species__inchikey',
'MoleculeInChI':'reaction__species__inchi',
'Inchi':'reaction__species__inchi',
'MoleculeChemicalName':'reaction__species__names',
}

