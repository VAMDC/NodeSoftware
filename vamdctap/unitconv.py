# Note that the fuctions here, if they are to be used from
# the Restrictables dictionary, need to accept and return
# (as list!) two arguments each, the operator and the value.
# The latter also needs to be a string! (stupid in some cases,
# I know, but more robust)

import sys
infty = str(sys.float_info.max)

# a decotrator to catch ZeroDivisionError
def catchZeroDivision(fu):
    def catcher(op,val):
        try:
            return fu(op,val)
        except ZeroDivisionError:
            return [invertOperator(op), infty]
        except:
            raise
    return catcher

def invertOperator(op):
    if op == '<': return '>'
    elif op == '>': return '<'
    elif op == '<=': return '>='
    elif op == '>=': return '<='

@catchZeroDivision
def Hz2Angstr(op, Hz):
    return [invertOperator(op), str(2.99792458E18/float(Hz))]

@catchZeroDivision
def eV2Angstr(op, eV):
    return [invertOperator(op), str(3.18264053E-20/float(eV))]

@catchZeroDivision
def invcm2Angstr(op, invcm):
    return [invertOperator(op), str(1.0E8/float(invcm))]

def eV2invcm(op,eV):
    return [op, str(8.06554429E3*float(eV))]

def invcm2eV(op,invcm):
    return [op, str(1.239841930E-4*float(invcm))]

@catchZeroDivision
def Angstr2MHz(op, Angstr):
    return [invertOperator(op), str(2.99792458E12/float(Angstr)) ]

def invcm2MHz(op, invcm):
    return [op, str(29979.2458*float(invcm)) ]

def eV2MHz (op, eV):
    return [op, str(2.417989348E8*float(eV)) ]

def Hz2MHz(op, Hz):
    return [op, str(float(Hz)/1000000.0) ]

# Vald specific but maybe instructive for others.
def valdObstype(op,obstype):
    obstype=obstype.strip().strip('\'"')
    ourMap = {'experiment':'0',
              'semiempirical':'1',
              'derived':'2',
              'theory':'3',
              #'semiempirical':'4',
              'compilation':'5'}
    return [op, ourMap.get(obstype, 'None')]


# Below:
# functions for handling a restrictable manually
# again, this is VALD-specific but may be instructive for other nodes

from django.db.models import Q,F
OPTRANS= { # convert numerical operators to the django-query equivalent
    '<':  '__lt',
    '>':  '__gt',
    '=':  '__exact',
    '<=': '__lte',
    '>=': '__gte'}

def bothStates(r,op,rhs):
    """
        compares two fields with an incoming restrictable, StateEnergy
        in this case which restricts both upper and lower states.
    """
    try:
        op = OPTRANS[op]
        float(rhs)
        return Q(**{'upstate__energy'+op:rhs}) & Q(**{'lostate__energy'+op:rhs})
    except:
        return Q(pk__isnull=True)

def test_constant_factory(const):
    """ returns a function that allows testing
        a restrictable against a constant
    """
    def fu(r,op,rhs):
        try:
            if op not in ('=','=='): raise Exception
            match = eval('%s == %s'%(rhs,const))
            if not match: raise Exception
            return Q(pk=F('pk'))
        except:
            return ~Q(pk=F('pk'))
    return fu
