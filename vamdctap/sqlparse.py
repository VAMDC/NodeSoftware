
# define a simple SQL grammar
from pyparsing import *

def setupSQLparser():
    selectStmt = Forward()
    selectToken = Keyword("select", caseless=True)
    ident = Word( alphas, alphanums+'.' ).setName("identifier")
    columnName     = delimitedList( ident, ",", )#combine=True )
    columnNameList = Group( delimitedList( columnName ) )
    whereExpression = Forward()
    and_ = Keyword("and", caseless=True)
    or_ = Keyword("or", caseless=True)
    in_ = Keyword("in", caseless=True)
    not_ = Keyword("not", caseless=True)
    E = CaselessLiteral("E")
    binop = oneOf("= != < > >= <= <> like", caseless=True)
    arithSign = Word("+-",exact=1)
    realNum = Combine( Optional(arithSign) + ( Word( nums ) + "." + Optional( Word(nums) )  |
                                           ( "." + Word(nums) ) ) +
                       Optional( E + Optional(arithSign) + Word(nums) ) )
    intNum = Combine( Optional(arithSign) + Word( nums ) +
                      Optional( E + Optional("+") + Word(nums) ) )

    columnRval = realNum | intNum | quotedString | columnName
    whereCondition = Optional(not_) + Group(
        ( columnName + binop + columnRval ) |
        ( columnName + in_ + "(" + delimitedList( columnRval ) + ")" ) |
        ( "(" + whereExpression + ")" )
        )
    whereExpression << whereCondition + ZeroOrMore( ( and_ | or_ ) + whereExpression )

    selectStmt      << ( selectToken +
                         Optional(CaselessLiteral('count')).setResultsName("count")  +
                         Optional(Group(CaselessLiteral('top') + intNum )).setResultsName("top") +
                         ( oneOf('* ALL', caseless=True) | columnNameList ).setResultsName( "columns" ) +
                         Optional( CaselessLiteral("where") + whereExpression.setResultsName("where") ) )

    # define Oracle comment format, and ignore them
    oracleSqlComment = "--" + restOfLine
    selectStmt.ignore( oracleSqlComment )

    return selectStmt

SQL=setupSQLparser()

############ SQL PARSER FINISHED; SOME HELPER THINGS BELOW

from django.db.models import Q
from django.conf import settings
from django.utils.importlib import import_module
DICTS = import_module(settings.NODEPKG+'.dictionaries')
from caselessdict import CaselessDict
RESTRICTABLES=CaselessDict(DICTS.RESTRICTABLES)

from types import TupleType, FunctionType
from string import strip
import logging
log = logging.getLogger('vamdc.tap.sql')

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

def splitWhere(ws, counter=0):
    logic = []
    rests = {}
    for w in ws:
        if type(w) == str: logic.append(w)
        elif w[1] in OPTRANS:
            logic.append('r%s'%counter)
            rests[str(counter)] = w.asList()
            counter += 1
        else:
            l,r, counter=splitWhere(w, counter)
            logic += l
            rests = dict(rests, **r)

    return logic,rests,counter

def applyRestrictFu(rs,restrictables=RESTRICTABLES):
    log.debug('%s'%rs)
    r, op, foo = rs[0], rs[1], rs[2:]
    if r not in restrictables: return rs
    if isinstance(restrictables[r], FunctionType):
        return restrictables[r]() # this runs the function!

    if not isinstance(restrictables[r], TupleType): return rs
    if len(foo) != 1:
        log.dedug('Applying a function to a Restrictable works only on a single value')
        return rs
    try:
        bla, fu = restrictables[r]
        rs = [r] + fu(op,foo[0])
    except Exception,e:
        log.error('Could not apply function %s to Restrictable %s. Errormsg: %s'%(fu,r,e))

    return rs


def mergeQwithLogic(qdict,logic):
    logic = ' '.join(logic).replace('and','&').replace('not','~').replace('or','|')
    log.debug('Joined logic before inserting Qs: %s'%logic)
    for r in qdict: exec('r%s=qdict[r]'%r)
    try:
        return eval(logic)
    except Exception,e:
        log.error('Eval of logic with Qs failed: %s'%e)


def checkLen1(x):
    if type(x) != list:
        log.error('this should have been a list: %s'%x)
    elif len(x) != 1:
        log.error('this should only have ha one element: %s'%x)
    else:
        return x[0].strip('\'"')

def restriction2Q(rs, restrictables=RESTRICTABLES):
    r, op, foo = rs[0], rs[1], rs[2:]
    if r not in restrictables:
        log.debug('Restrictable "%s" not supported!'%r)
        return Q(False)
    if type(restrictables[r]) == tuple:
        rest_rhs = restrictables[r][0]
    else: rest_rhs = restrictables[r]

    if op=='in':
        if not (foo[0]=='(' and foo[-1]==')'):
            log.error('Values for IN not bracketed: %s'%foo)
        else: foo=foo[1:-1]
        ins = map(strip,foo,('\'"',)*len(foo))
        return Q(**{rest_rhs+'__in':ins})
    if op=='like':
        foo=checkLen1(foo)
        if foo.startswith('%') and foo.endswith('%'): o='__contains'
        elif foo.startswith('%'): o='__endswith'
        elif foo.endswith('%'): o='__startswith'
        else:
            o='__exact'
            log.warning('LIKE operator used without percent signs. Treating as __exact. (Underscore and [] are unsupported)')
        return Q(**{rest_rhs+o:foo.strip('%')})
    if op=='<>' or op=='!=':
        foo = checkLen1(foo)
        if foo.lower() == 'null':
            return Q(**{rest_rhs+'__isnull':False})
        else:
            return ~Q(**{rest_rhs: foo})

    foo = checkLen1(foo)
    return Q(**{rest_rhs+OPTRANS[op]: foo})

def sql2Q(sql):
    if not sql.where:
        return Q()
    log.debug('Starting sql2Q.')
    logic,rs,count = splitWhere(sql.where)
    log.debug('splitWhere() returned: logic: %s\nrs: %s\ncount: %s'%(logic,rs,count))
    qdict = {}
    for i,r in rs.items(): # loop over restrictions
        r = applyRestrictFu(r)
        log.debug('after applyRestrictFu(): %s'%r)
        q = restriction2Q(r)
        log.debug('after restriction2Q(rs): %s'%q)
        qdict[i] = q

    return mergeQwithLogic(qdict,logic)






# OLD HELPER FUNCTIONS BELOW HERE

def singleWhere(w,restrictables):
    if not w[0] in restrictables:
        log.warning('Unsupported Restrictable: %s'%w[0])
        return 'Q(pk=False)'
    if not OPTRANS.has_key(w[1]):
        log.warning('Unsupported operator: %s'%w[1])
        return ''
    value=w[2].strip('\'"')
    qstring = 'Q(%s="%s")'%(restrictables[w[0]] + OPTRANS[w[1]],value)
    return qstring

def where2q(ws,restrictables):
    if not ws:
        return 'Q()'
    q=''
    for w in ws:
        if len(w)>4 and w[1]=='in':
            if not restrictables.has_key(w[0]):
                log.warning('cant find name %s'%w[0]); return ''
            # join the comma-separated list into a single string and strip
            # the parentheses
            w[2] = '"%s"' % ', '.join(w[3:-1])
            qstring="Q(%s__in=(%s))" % (restrictables[w[0]], ', '.join(w[3:-1]))
            q += qstring
            return q
        log.debug('w: %s'%w)
        if w=='and': q+=' & '
        elif w=='or': q+=' | '
        elif w[0]=='(' and w[-1]==')':
            q+=' ( '
            q+=where2q(w[1:-1],restrictables)
            q+=' ) '
        elif len(w)==3: q+=singleWhere(w,restrictables)

    log.debug('q: %s'%q)
    return q
