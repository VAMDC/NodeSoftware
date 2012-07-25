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
'NodeID':'IDEADB',
'MethodCategory':'experiment',
'CollisionCode':'elat',
'CollisionIAEACode':'EDA',
'CollisionID':'CollTran.id',
'CollisionRef':'CollTran.source.id',
'CollisionComment':'CollTran.comment',
'CollisionReactantSpecies':'Reactant.id',
'CollisionProductSpecies':'Product.id',
'CollisionDataSetDescription':'DataSet.description',

'CollisionTabulatedDataProductionDate':'TabData.ProductionDate',
'CollisionTabulatedDataXDataList':'TabData.X.DataList',
'CollisionTabulatedDataXDataListN':'TabData.Xlength',
'CollisionTabulatedDataYDataList':'TabData.Y.DataList',
'CollisionTabulatedDataYDataListN':'TabData.Ylength',
'CollisionTabulatedDataYUnits':'1/s',
'CollisionTabulatedDataXUnits':'TabData.Xunits',

'CollisionTabulatedDataYDescription':'Ion Yield',
'CollisionTabulatedDataXDescription':'Energy of the impact electron',

'CollisionDataSetRef':'DataSet.SourceRef',
'CollisionTabulatedData':'TabData',

#errors
'CollisionTabulatedDataXAccuracyType':'TabData.X.AccuracyType',
'CollisionTabulatedDataXAccuracyRelative':'TabData.X.Relative',
'CollisionTabulatedDataXAccuracyErrorValue':'TabData.X.ErrorValue',

'CollisionTabulatedDataYAccuracyType':'TabData.Y.AccuracyType',
'CollisionTabulatedDataYAccuracyRelative':'TabData.Y.Relative',
'CollisionTabulatedDataYAccuracyErrorList':'TabData.Y.ErrorList',


'AtomInchi':'Atom.inchi',
'AtomMass':'Atom.exactmass',
'AtomMassUnit':'amu',
'AtomMassNumber':'Atom.mass',
'AtomSpeciesID':'Atom.id',
'AtomSymbol':'Atom.chemical_formula',
'AtomNuclearCharge':'Atom.nuclear_charge',
'AtomIonCharge':'Atom.ioncharge',

'MoleculeSpeciesID':'Molecule.id',
'MoleculeMolecularWeight':'Molecule.mass',
'MoleculeMolecularWeightUnit':'amu',
'MoleculeInchi':'Molecule.inchi',
'MoleculeInchiKey':'Molecule.inchikey',
'MoleculeChemicalNameValue':'Molecule.chemical_formula',
'MoleculeStoichiometricFormula':'Molecule.chemical_formula',
'MoleculeCASRegistryNumber':'Molecule.cas',
'MoleculeIonCharge':'Molecule.ioncharge',
'MoleculeOrdinaryStructuralFormula':'Molecule.chemical_formula',

'ParticleName':'Particle.name',
'ParticleSpeciesID':'Particle.speciesid',
'ParticleCharge':'Particle.charge',
'ParticleComment':'Particle.comment',
'ProcessIDType':'Colltran.name',
#SourceArticleNumber
'SourceAuthorName':'Source.author',
#SourceComments
'SourceDOI':'Source.doi',
'SourceID':'Source.id',
'SourceCategory':'Source.type',
'SourcePageBegin':'Source.pagestart',
'SourcePageEnd':'Source.pageend',
'SourceTitle':'Source.title',
'SourceURI':'Source.url',
'SourceVolume':'Source.volume',
'SourceYear':'Source.year',
}

# The restrictable dictionary defines limitations to the search. 
# The left-hand side is standardized, the righ-hand size should
# be defined in Django query-language style, where e.g. a search
# for the Species.atomic field  would be written as species__atomic.

RESTRICTABLES = {\
'MoleculeChemicalName':('species__name','origin_species__name'),
'AtomMassNumber':'species__mass',
'MoleculeMolecularWeight':('species__mass','origin_species__mass'),
'AtomSymbol':'species__chemical_formula',
'Inchi':('species__inchi','origin_species__inchi'),
'InchiKey':('species__inchikey','origin_species__inchikey'),
'MoleculeOrdinaryStructuralFormula':('species__chemical_formula','origin_species__chemical_formula'),
'MoleculeCASRegistryNumber':('species__cas','origin_species__cas'),
}
