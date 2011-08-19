
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

