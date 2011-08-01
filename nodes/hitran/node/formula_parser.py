# formula_parser.py
# -*- coding: utf-8 -*-
# Christian Hill
# 12/7/2011

from pyparsing import Word, Group, Optional, OneOrMore, ParseException,\
                      Literal, StringEnd
import elements

caps = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
lowers = caps.lower()
digits = '0123456789'
element = Word(caps, lowers)
integer = Word(digits)
elementRef = Group(element + Optional(integer, default='1'))
chemicalFormula = OneOrMore(elementRef)
plusminus = Literal('+') | Literal('-')
charge = Group(plusminus + Optional(integer, default='1'))
chargedChemicalFormula = Group(chemicalFormula) + Optional(charge)\
                            + StringEnd()

class FormulaError(Exception):
    def __init__(self, error_str):
        self.error_str = error_str
    def __str__(self):
        return self.error_str

def get_stoichiometric_formula(formula):
    """
    Get the stoichiometric formula, in canonical form (increasing
    atomic mass) from a given formula string.
    e.g. 'CH3OH' -> 'H4CO'

    """
 
    elms = {}
    try:
        chargedformulaData = chargedChemicalFormula.parseString(formula)
    except ParseException:
        raise FormulaError("Invalid formula syntax: %s" % formula)
    formulaData = chargedformulaData[0]
    
    # parse the charge part of the formula, if present:
    charge_string = ''
    if len(chargedformulaData) == 2:
        charge_sign, charge_value = chargedformulaData[1]
        charge_string = charge_sign
        if charge_value != '1':
            charge_string += charge_value

    for symbol, stoich in formulaData:
        try:
            element_name = elements.element_names[symbol]
        except KeyError:
            raise FormulaError("Invalid formula: %s. Unknown element symbol"\
                               " %s" % (formula, symbol))
        atomic_number = elements.atomic_numbers[symbol]
        if atomic_number in elms.keys():
            elms[atomic_number] += int(stoich)
        else:
            elms[atomic_number] = int(stoich)
    elm_strs = []
    for atomic_number in sorted(elms.keys()):
        if elms[atomic_number]>1:
            elm_strs.append('%s%d' % (elements.element_symbols[atomic_number],
                                      elms[atomic_number]))
        else:
            elm_strs.append(elements.element_symbols[atomic_number])
    # finally, add on the charge string, e.g. '', '-', '+2', ...
    elm_strs.append(charge_string)
    return ''.join(elm_strs)
