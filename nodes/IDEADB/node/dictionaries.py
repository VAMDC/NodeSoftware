from vamdctap.unitconv import *

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
#'XSAMSVersion' : u'1.0',
'NodeID':'IDEADB',
'MethodCategory':'experiment',
'CollisionCode':'CollTran.process_codes',
'CollisionIAEACode':'CollTran.IAEA_codes',
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
'CollisionTabulatedDataYUnits':'TabData.Yunits',
'CollisionTabulatedDataXUnits':'TabData.Xunits',

'CollisionTabulatedDataYDescription':'Ion Yield',
'CollisionTabulatedDataXDescription':'Energy of the impact electron',

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
'AtomInchiKey':'Atom.inchikey',

'MoleculeSpeciesID':'Molecule.id',
'MoleculeMolecularWeight':'Molecule.mass',
'MoleculeMolecularWeightUnit':'amu',
'MoleculeInchi':'Molecule.inchi',
'MoleculeInchiKey':'Molecule.inchikey',
'MoleculeChemicalName':'Molecule.name',
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
#general stuff
'CollisionCode':('process_code', 'process_code_2'),
'SourceDOI':'source__doi',

#general: has the tuples and searches either in origin_species or in species
'MoleculeChemicalName':'species__name',
'AtomMassNumber':'species__mass',
'MoleculeMolecularWeight':'species__mass',
'AtomSymbol':'species__chemical_formula',
'Inchi':'origin_species__inchi',
'InchiKey':'origin_species__inchikey',
'MoleculeStoichiometricFormula':('origin_species__chemical_formula', 'species__chemical_formula'),
'MoleculeCASRegistryNumber':'species__cas',
'ParticleName':test_constant(['electron']),

#only search for reactants
'reactant0.MoleculeChemicalName':'origin_species__name',
'reactant0.AtomMassNumber':'species__mass',
'reactant0.MoleculeMolecularWeight':'origin_species__mass',
'reactant0.AtomSymbol':'species__chemical_formula',
'reactant0.Inchi':'origin_species__inchi',
'reactant0.InchiKey':'origin_species__inchikey',
'reactant0.MoleculeStoichiometricFormula':'origin_species__chemical_formula',
'reactant0.MoleculeCASRegistryNumber':'origin_species__cas',
'reactant0.ParticleName':test_constant(['electron']),


#only search for reactants
'reactant1.MoleculeChemicalName':'origin_species__name',
'reactant1.AtomMassNumber':'species__mass',
'reactant1.MoleculeMolecularWeight':'origin_species__mass',
'reactant1.AtomSymbol':'species__chemical_formula',
'reactant1.Inchi':'origin_species__inchi',
'reactant1.InchiKey':'origin_species__inchikey',
'reactant1.MoleculeStoichiometricFormula':'origin_species__chemical_formula',
'reactant1.MoleculeCASRegistryNumber':'origin_species__cas',
'reactant1.ParticleName':test_constant(['electron']),

# collider is always an electron:

'collider.ParticleName':test_constant(['electron']),

# target could also be an origin_species
'target.MoleculeChemicalName':'origin_species__name',
'target.AtomMassNumber':'species__mass',
'target.MoleculeMolecularWeight':'origin_species__mass',
'target.AtomSymbol':'species__chemical_formula',
'target.Inchi':'origin_species__inchi',
'target.InchiKey':'origin_species__inchikey',
'target.MoleculeStoichiometricFormula':'origin_species__chemical_formula',
'target.MoleculeCASRegistryNumber':'origin_species__cas',
'target.ParticleName':test_constant(['electron']),


# only search for products
'product0.MoleculeChemicalName':'species__name',
'product0.AtomMassNumber':'species__mass',
'product0.MoleculeMolecularWeight':'species__mass',
'product0.AtomSymbol':'species__chemical_formula',
'product0.Inchi':'species__inchi',
'product0.InchiKey':'species__inchikey',
'product0.MoleculeStoichiometricFormula':'species__chemical_formula',
'product0.MoleculeCASRegistryNumber':'species__cas',

'product1.ParticleName':test_constant(['electron']),
}
