#!/usr/bin/python
""" provides some basic chemical functions """

import periodictable
import re

#list of nominal mass of most abundant isotopes
#taken from http://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl
atommasses = {
    'H': 1,
    'D': 2,
    'He': 4,
    'Li': 7,
    'Be': 9,
    'B': 11,
    'C': 12,
    'N': 14,
    'O': 16,
    'F': 19,
    'Ne': 20,
    'Na': 23,
    'Mg': 24,
    'Al': 27,
    'Si': 28,
    'P': 31,
    'S': 32,
    'Cl': 35,
    'Ar': 40,
    'K': 39,
    'Ca': 40,
    'Sc': 45,
    'Ti': 48,
    'V': 51,
    'Cr': 52,
    'Mn': 55,
    'Fe': 56,
    'Co': 59,
    'Ni': 58,
    'Cu': 63,
    'Zn': 64,
    'Ga': 69,
    'Ge': 74,
    'As': 75,
    'Se': 80,
    'Br': 79,
    'Kr': 84,
    'Rb': 85,
    'Sr': 88,
    'Y': 89,
    'Zr': 90,
    'Nb': 93,
    'Mo': 98,
    'Tc': 98,
    'Ru': 102,
    'Rh': 103,
    'Pd': 106,
    'Ag': 107,
    'Cd': 114,
    'In': 115,
    'Sn': 120,
    'Sb': 121,
    'Te': 130,
    'I': 127,
    'Xe': 132,
    'Cs': 133,
    'Ba': 138,
    'La': 139,
    'Ce': 140,
    'Pr': 141,
    'Nd': 142,
    'Pm': 145,
    'Sm': 152,
    'Eu': 153,
    'Gd': 158,
    'Tb': 159,
    'Dy': 162,
    'Ho': 165,
    'Er': 166,
    'Tm': 169,
    'Yb': 174,
    'Lu': 175,
    'Hf': 180,
    'Ta': 181,
    'W': 184,
    'Re': 187,
    'Os': 192,
    'Ir': 193,
    'Pt': 195,
    'Au': 197,
    'Hg': 202,
    'Tl': 205,
    'Pb': 208,
    'Bi': 209,
    'Po': 209,
    'At': 210,
    'Rn': 211,
    'Fr': 223,
    'Ra': 223,
    'Ac': 227,
    'Th': 232,
    'Pa': 231,
    'U': 238,
}

def chemicalformula2exactmass(chemicalformula):
    """ calculate exact mass from chemical formula with periodictable """
    chemformula = periodictable.formula(chemicalformula)
    return chemformula.mass

def chemicalformula2nominalmass(chemicalformula, atommasses = atommasses):
    """ calculate nominal mass from chemical formula using the dictionary atommasses """
    symbolcache = ''
    indexcache = ''

    status = 'none'

    mass = 0

    def calculate(symbolcache, indexcache=''):
        if indexcache == '':
            indexcache = '1'
        return atommasses[symbolcache] * int(indexcache)

    for char in chemicalformula:
        if char.isupper() is True:
            if status == 'digit':
                mass += calculate(symbolcache, indexcache)
                indexcache = ''
                symbolcache = ''
                status = 'none'
            elif status == 'lower':
                mass += calculate(symbolcache, indexcache)
                indexcache = ''
                symbolcache = ''
                status = 'none'
            elif status == 'upper':
                mass += calculate(symbolcache, indexcache)
                indexcache = ''
                symbolcache = ''
                status = 'none'
            symbolcache = char
            status = 'upper'
        elif char.islower() is True:
            symbolcache += char
            status = 'lower'
        elif char.isdigit() is True:
            indexcache += char
            status = 'digit'

    mass += calculate(symbolcache, indexcache)

    return mass

def checkatoms(chemicalformula, atommasses = atommasses):
    """ Checks each atom in a chemical formula for validity (e.g. listing in atommasses) """
    result = 0
    match = re.findall('([A-Z]{1}[a-z]{0,2})', str(chemicalformula))
    for atom in match:
        try:
            mass = atommasses[atom]
        except KeyError:
            result = atom

    return result
