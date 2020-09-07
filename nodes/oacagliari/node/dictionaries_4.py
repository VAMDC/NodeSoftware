# -*- coding: utf-8 -*-
"""
OACagliari dictionary definitions. 
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

RETURNABLES = {'AtomMass':'AtomState.stardard_atomic_weight',
'AtomMassNumber':'AtomState.atomic_mass',
'AtomNuclearCharge':'AtomState.atomic_number',
'AtomSymbol':'AtomState.symbol',
#'MethodComment':'Method.',
#'MethodRef':'Method.',
'MoleculeChemicalName':'Molecule.name',
'MoleculeInchi':'Molecule.inchi',
'MoleculeInchiKey':'Molecule.inchikey',
'MoleculeIonCharge':'Molecule.charge',
#'MoleculeMolecularWeight':'Molecule.',
#'MoleculeQnCase':'MoleQNs.',
'MoleculeSpeciesID':'Molecule.species_id',
'MoleculeStateEnergy':'MoleculeState.total_energy',
'MoleculeStateID':'MoleculeState.state_id',
'MoleculeStoichiometricFormula':'Molecule.formula',
'NodeID':'OACagliari',
#'SourceAuthorName':'Source.',
##'SourceCategory':'Source.type.description',
##'SourceID':'Source.bib_id',
##'SourceName':'Source.series.name',
##'SourcePageBegin':'Source.page_begin',
##'SourcePageEnd':'Source.page_end',
##'SourceTitle':'Source.title',
##'SourceURI':'Source.uri',
##'SourceVolume':'Source.volume',
##'SourceYear':'Source.date',
}


RESTRICTABLES = {
'AtomMass':'elements__standard_atomic_weight',
'AtomMassNumber':'elements__atomic_mass',
'AtomNuclearCharge':'elements__atomic_number',
'AtomSymbol':'elements__symbol',
'MoleculeChemicalName':'molecularspecies__name',
'MoleculeInchi':'molecularspecies__inchi',
'MoleculeInchiKey':'molecularspecies__inchikey',
'MoleculeIonCharge':'molecularspecies__charge',
'MoleculeMolecularWeight':'100',
'MoleculeStateEnergy':'electronic_states__total_energy',
'MoleculeStateID':'electronic_states__state_id',
'MoleculeStoichiometricFormula':'molecularspecies__formula',
##'SourceCategory':'reftype__description',
##'SourceYear':'bibliography__date', #only year
}



# Do not edit or remove these three lines
from requests.utils import CaseInsensitiveDict as CaselessDict
RETURNABLES = CaselessDict(RETURNABLES)
RESTRICTABLES = CaselessDict(RESTRICTABLES)

