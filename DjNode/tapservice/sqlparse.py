
# define a simple SQL grammar
from pyparsing import *

selectStmt = Forward()
selectToken = Keyword("select", caseless=True)
ident = Word( alphas, alphanums ).setName("identifier")
columnName     = delimitedList( ident, ".", combine=True )
columnNameList = Group( delimitedList( columnName ) )
whereExpression = Forward()
and_ = Keyword("and", caseless=True)
or_ = Keyword("or", caseless=True)
in_ = Keyword("in", caseless=True)
E = CaselessLiteral("E")
binop = oneOf("= != < > >= <= eq ne lt le gt ge", caseless=True)
arithSign = Word("+-",exact=1)
realNum = Combine( Optional(arithSign) + ( Word( nums ) + "." + Optional( Word(nums) )  |
                                                         ( "." + Word(nums) ) ) + 
            Optional( E + Optional(arithSign) + Word(nums) ) )
intNum = Combine( Optional(arithSign) + Word( nums ) + 
            Optional( E + Optional("+") + Word(nums) ) )

columnRval = realNum | intNum | quotedString | columnName
whereCondition = Group(
    ( columnName + binop + columnRval ) |
    ( columnName + in_ + "(" + delimitedList( columnRval ) + ")" ) |
    ( columnName + in_ + "(" + selectStmt + ")" ) |
    ( "(" + whereExpression + ")" )
    )
whereExpression << whereCondition + ZeroOrMore( ( and_ | or_ ) + whereExpression ) 

selectStmt      << ( selectToken + Optional(Group(CaselessLiteral('top') + intNum )).setResultsName("top") + 
                   ( oneOf('* ALL', caseless=True) | columnNameList ).setResultsName( "columns" ) + 
                   Optional( CaselessLiteral("where") + whereExpression.setResultsName("where") ) )

SQL=selectStmt

# define Oracle comment format, and ignore them
oracleSqlComment = "--" + restOfLine
SQL.ignore( oracleSqlComment )
