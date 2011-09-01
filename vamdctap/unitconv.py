# Note that the fuctions here, if they are to be used from
# the Restrictables dictionary, need to accept and return
# (as list!) two arguments each, the operator and the value.
# The latter also needs to be a string! (stupid in some cases,
# I know, but more robust)

def invertOperator(op):
    if op == '<': return '>'
    elif op == '>': return '<'
    elif op == '<=': return '>='
    elif op == '>=': return '<='

def Hz2Angstr(op, Hz):
    return [invertOperator(op), str(2.99792458E18/float(Hz))]

def eV2Angstr(op, eV):
    return [invertOperator(op), str(3.18264053E-20/float(eV))]

def invcm2Angstr(op, invcm):
    return [invertOperator(op), str(1.0E8/float(invcm))]

#Vald specific but maybe instructive for others.
def valdObstype(op,obstype):
    obstype=obstype.strip().strip('\'"')
    ourMap = {'experiment':'0',
              'theory':'3',
              #'ritz':'None',
              #'recommended':'None',
              #'evaluated':'None',
              'empirical':'2',
              #'scalingLaw':'None',
              #'semiempirical':'None',
              'compilation':'5',
              'derived':'4',
              'observed':'1',}
    if not obstype in ourMap:
        return [op, 'None']
    else:
        return [op, ourMap[obstype]]
