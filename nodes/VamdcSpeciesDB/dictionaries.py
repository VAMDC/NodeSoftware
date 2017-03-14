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
# returned from queryfunc.py. So in the example below, all 'AtomStates'
# will be looped over by the node software, using the name 'AtomState'
# (singular). 'AtomState' will be one single instance of a matching
# database object, from which we extract everything we need by parsing
# the VAMDC_standard LHS of this dictionary to how it maps to our specific
# database on the RHS. So, when looping through all AtomState objects
# matching the given query, the generator will for example know that
# to get the AtomStateEnergy VAMDC value, it will need to look at
# the AtomState.energy, i.e. the "energy" property of the current
# database object being worked on.
#
# (if you look at queryfuncs.py, you'll see 'AtomStates' being
#  assigned)

RETURNABLES = {\
    'XSAMSVersion':'1.0',
    'NodeID':'VSDB', # required
    ############################################################
    #'MethodID':'Method.id',
    #'MethodCategory':'Method.category',
    ############################################################
    # Sources are handled by XML method on model.
    'AtomInchi':'Atom.inchi',
    'AtomInchiKey':'Atom.inchikey',
    #'AtomVamdcSpeciesID':'Atom.id',
    'AtomSymbol':'Atom.symbol()',
    'AtomSpeciesID':'Atom.id',
    'AtomNuclearCharge':'Atom.nuclear_charge()',
    'AtomIonCharge':'Atom.charge',
    'AtomMassNumber':'Atom.mass_number',
    

    'MoleculeChemicalName':'Molecule.trivial_name()',
    'MoleculeID':'Molecule.id',
    'MoleculeInchi':'Molecule.inchi',
    'MoleculeInchiKey':'Molecule.inchikey',
    'MoleculeVAMDCSpeciesID':'Molecule.id',
    
    'MoleculeMolecularWeight':'Molecule.mass_number',
    'MoleculeSpeciesID':'Molecule.id',
    
    #'MoleculeStructure': 'Molecule',    # we have an XML() method for this
    
    'MoleculeStoichiometricFormula':'Molecule.stoichiometric_formula',
    'MoleculeOrdinaryStructuralFormula':'Molecule.structural_formula()',
    'MoleculeComment': 'Molecule.comment()', #'Molecule.name',
    

}

from vamdctap.unitconv import *
from string import strip
import sys
# Q-objects for always True / False
QTrue = Q(pk=F('pk'))
QFalse = ~QTrue

OPTRANS= { # transfer SQL operators to django-style
    '<':  '__lt',
    '>':  '__gt',
    '=':  '__exact',
    '<=': '__lte',
    '>=': '__gte',
    '!=': '',
    '<>': '',
    'in': '__in',
    'like': '',
}


def stoichiometricformula(r,op,rhs):
    """
    """
    try:
        op = OPTRANS[op]
        #float(rhs)
        rhs = rhs.strip('\'"')
        return Q(**{'stoichiometric_formula'+op:rhs}) & Q(**{'species_type__name__exact':'Molecule'})
    except:
        return Q(pk__isnull=True)


def atommassnumber(r,op,rhs):
    """
    """
    try:
        op = OPTRANS[op]
        #float(rhs)
        return Q(**{'mass_number'+op:rhs}) & Q(**{'species_type__name__exact':'Atom'})
    except:
        return Q(pk__isnull=True)


def atomsymbol(r,op,rhs):
    """
    """
    try:
        op = OPTRANS[op]
        #float(rhs)
        rhs = rhs.strip('\'"')
        return Q(**{'stoichiometric_formula'+op:rhs}) & Q(**{'species_type__name__exact':'Atom'})
    except:
        return Q(pk__isnull=True)


# The restrictable dictionary defines limitations to the search.
# The left-hand side is standardized, the righ-hand size should
# be defined in Django query-language style, where e.g. a search
# for the Species.atomic field  would be written as species__atomic.

RESTRICTABLES = {\
    ##### General ####
    #'AsOfDate':'',
    'InchiKey':'inchikey',
    'VAMDCSpeciesID':'id',
    'IonCharge':'charge',

    ###### Atoms #######
    'AtomSymbol':atomsymbol,
    #'AtomNuclearCharge':'',
    #'AtomIonCharge':''
    #'AtomInchi':'',
    #'AtomInchiKey':'',
    #'AtomMass':'',
    'AtomMassNumber':atommassnumber, #mass_number',
    #'AtomNuclearCharge':'',
    #'AtomNuclearSpin':'',


    ###### Molecules ####
    'MoleculeStoichiometricFormula':stoichiometricformula, #'stoichiometric_formula',
    #'MoleculeChemicalName':'',
    #'MoleculeMolecularWeight':'',

    
}

