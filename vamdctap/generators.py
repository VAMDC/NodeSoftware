#coding: utf-8 -*-


import sys
import datetime
from xml.sax.saxutils import escape

# Get the node-specific parts
from django.conf import settings
from importlib import import_module
DICTS = import_module(settings.NODEPKG + '.dictionaries')
from caselessdict import CaselessDict
RETURNABLES = CaselessDict(DICTS.RETURNABLES)

# This must always be set.
try:
    NODEID = RETURNABLES['NodeID']
except:
    NODEID = 'PleaseFillTheNodeID'

try:
    XSAMS_VERSION = RETURNABLES['XSAMSVersion']
except:
    XSAMS_VERSION = '1.0'
try:
    SCHEMA_LOCATION = RETURNABLES['SchemaLocation']
except:
    SCHEMA_LOCATION = 'http://vamdc.org/xml/xsams/%s'%XSAMS_VERSION

import logging
log = logging.getLogger('vamdc.tap.generator')

# Helper function to test if an object is a list or tuple
isiterable = lambda obj: hasattr(obj, '__iter__')

def makeiter(obj, n=0):
    """
    Return an iterable of length n, no matter what.
    None as imput should give [], unless n!=0, then [None,None,...]
    """
    if not obj and obj != 0:
        # the empty case
        return [None] * n
    elif not isiterable(obj):
        if n:
            # return single value n times
            return [obj] * n
        else: return [obj]
    else:
        return obj

def makeloop(keyword, G, *args):
    """
    Creates a nested list of lists. All arguments should be valid dictionary
    keywords and will be fed to G. They are expected to return iterables of equal lengths.
    The generator yields a list of current element of each argument-list in order, so one can do e.g.

       for name, unit in makeloop('TabulatedData', G, 'Name', 'Unit'):
          ...
    """
    if not args:
        return []
    Nargs = len(args)
    lis = []
    for arg in args:
        lis.append(makeiter(G("%s%s" % (keyword, arg))))
    try:
        Nlis = lis[0].count()
    except TypeError:
        Nlis = len(lis[0])
    olist = [[] for i in range(Nargs)]
    for i in range(Nlis):
        for k in range(Nargs):
            try:
                olist[k].append(lis[k][i])
            except Exception:
                olist[k].append("")
    return olist

def GetValue(returnable_key, **kwargs):
    """
    the function that gets a value out of the query set, using the global name
    and the node-specific dictionary.
    """
    #log.debug("getvalue, returnable_key : " + returnable_key)
    try:
        #obtain the RHS of the RETURNABLES dictionary
        name = RETURNABLES[returnable_key]
    except Exception, e:
        # The value is not in the dictionary for the node.  This is
        # fine.  Note that this is also used by if-clauses below since
        # the empty string evaluates as False.
        #log.debug(e)
        return ''

    if not name:
        # the key was in the dict, but the value was empty or None.
        return ''

    if not '.' in name:
        # No dot means it is a static string!
        return name

    # strip the prefix
    attribs = name.split('.')[1:]
    attribs.reverse() # to later pop() from the front

    #get the current structure, throw away its name
    bla,obj = kwargs.popitem()

    # Go through the cascade of foreignKeys/attributes to get to the leaf object
    while len(attribs) >1:
        att = attribs.pop()
        obj = getattr(obj,att)

    att = attribs.pop() # this is the last one now, can be either attribute or function

    if att.endswith('()'):
        value = getattr(obj,att[:-2])() # RUN IT!
    else:
        value = getattr(obj,att,name)

    if value == None:
        # the database returned NULL
        return ''
    elif value == 0:
        if isinstance(value, float): return '0.0'
        else: return '0'
    return value

def makeOptionalTag(tagname, keyword, G, extraAttr={}):
    content = G(keyword)

    if not content:
        return ''
    elif isiterable(content):
        s = []
        for c in content:
            s.append( '<%s>%s</%s>'%(tagname,c,tagname) )
        return ''.join(s)
    else:
        extra = "".join([' %s="%s"'% (k, v) for k, v in extraAttr.items()])
        return '<%s%s>%s</%s>'%(tagname, extra, content,tagname)

def makeSourceRefs(refs):
    """
    Create a SourceRef tag entry
    """
    s = []
    if refs:
        if isiterable(refs):
            for ref in refs:
                s.append( '<SourceRef>B%s-%s</SourceRef>' % (NODEID, ref) )
        else: s.append( '<SourceRef>B%s-%s</SourceRef>' % (NODEID, refs) )
    return ''.join(s)

def makePartitionfunc(keyword, G):
    """
    Create the Partionfunction tag element.
    (T and Q can be lists of lists)
    """
    value = G(keyword)
    if not value:
        return ''

    temperature = value
    unit = G(keyword+'Unit')
    partitionfunc = G(keyword+'Q')
    comments = G(keyword+'Comments')
    # Nuclear Spin Isomer Information 
    nsilowrovibsym = G(keyword+'NSILowestRoVibSym')
    nsiname = G(keyword+'NSIName')
    nsisymgroup = G(keyword+'NSISymGroup')
    nsistateref = G(keyword+'NSILowestEnergyStateRef')

    if not isiterable(value[0]):
        Npf = 1
        temperature = [temperature]
        unit = [unit]
        partitionfunc = [partitionfunc]
        comments = [comments]
        # Nuclear Spin Isomer Information 
        nsilowrovibsym = [nsilowrovibsym]
        nsiname = [nsiname]
        nsisymgroup = [nsisymgroup]
        nsistateref = [nsistateref]
    else:
        Npf = len(temperature)
        unit = makeiter(unit,Npf)

    string = ''
    for i in xrange(Npf):
        string += '<PartitionFunction>'
        if len(comments)>i and comments[i]: string += '<Comments>%s</Comments>' % comments[i]
        string += '<T units="%s"><DataList>' % (unit[i] if (len(unit)>i and unit[i]) else 'K')
        string += " ".join(str(temp) for temp in temperature[i])
        string += '</DataList></T>'
        string += '<Q><DataList>'
        string += " ".join(str(q) for q in partitionfunc[i])
        string += '</DataList></Q>'
        if len(nsiname)>i and nsiname[i]:
            string += makePrimaryType("NuclearSpinIsomer", "NuclearSpinIsomer",G,
                                  extraAttr={"lowestEnergyStateRef":'S%s-%s' % (G('NodeID'), nsistateref[i])})
            string += "<Name>%s</Name>" % nsiname[i]
            string += "<LowestRoVibSym group='%s'>%s</LowestRoVibSym>" % (nsisymgroup[i], nsilowrovibsym[i])
            string += "</NuclearSpinIsomer>"

        string += '</PartitionFunction>'
    return string

def makePrimaryType(tagname, keyword, G, extraAttr={}):
    """
    Build the Primary-type base tags. Note that this method does NOT
    close the tag, </tagname> must be added manually by the calling function.

    extraAttr is a dictionary of attributes-value pairs to add to the tag.
    """
    method = G("%sMethod" % keyword)
    comment = G("%sComment" % keyword)
    refs = G(keyword + 'Ref') # Sources

    result = ["<%s" % tagname]
    if method:
        result.append( ' methodRef="M%s-%s"' % (NODEID, method) )
    for k, v in extraAttr.items():
        if v or v==0:
            result.append( ' %s="%s"'% (k, v) )

    result.append( '>' )
    if comment:
        result.append( '<Comments>%s</Comments>' % escape(comment))
    result.append( makeSourceRefs(refs) )

    return ''.join(result)

def makeReferencedTextType(tagname,keyword,G):
    value = G(keyword)
    if value:
        return '%s<Value>%s</Value></%s>'%\
         (makePrimaryType(tagname,keyword,G),
          value,
          tagname)
    else:
        return ''

def makeRepeatedDataType(tagname, keyword, G, extraAttr={}):
    """
    Similar to makeDataType above, but allows the result of G()
    to be iterable and adds the name-attribute. If the
    corresponding refs etc are not iterable, they are replicated
    for each tag.
    """
    value = G(keyword)
    if not value:
        return ''
    
    unit = G(keyword + 'Unit')
    method = G(keyword + 'Method')
    comment = G(keyword + 'Comment')
    acc = G(keyword + 'Accuracy')
    refs = G(keyword + 'Ref')
    name = G(keyword + 'Name')

    # make everything iterable
    value, unit, method, comment, acc, refs, name = [[x] if not isiterable(x) else x  for x in [value, unit, method, comment, acc, refs, name]]

    # if some are shorter than the value list, replicate them
    l = len(value)
    value, unit, method, comment, acc, refs, name = [ x*l if len(x)<l else x for x in [value, unit, method, comment, acc, refs, name]]

    for k, v in extraAttr.items():
        if not isiterable(v): v=[v]*l
        elif len(v)<l: v*=l
        extraAttr[k] = v

    string = ''
    for i, val in enumerate(value):
        string += '<%s' % tagname
        for k, v in extraAttr.items():
            if v[i]: string += ' %s="%s"'%(k,v[i])
        if name[i]:
            string += ' name="%s"' % name[i]
        if method[i]:
            string += ' methodRef="M%s-%s"' % (NODEID, method[i])
        string += '>'
        if comment[i]:
            string += '<Comments>%s</Comments>' % escape('%s' % comment[i])
        string += makeSourceRefs(refs[i])
        string += '<Value units="%s">%s</Value>' % (unit[i] or 'unitless', val)
        string += makeEvaluation( keyword, G, j=i)

        # This is broken, makes empty <Accuracy/>.
        # TODO: Proper solution is to add j-parameter to makeAccuracy(), similar to makeEvalution()
        #if acc[i] is not None:
        #    string += '<Accuracy>%s</Accuracy>' % acc[i]


        string += '</%s>' % tagname
    return string

# an alias for compatibility reasons
makeNamedDataType = makeRepeatedDataType

def makeAccuracy(keyword, G):
    """
    build the elements for accuracy that belong
    to DataType.
    """
    acc = G(keyword + 'Accuracy')
    if acc is None:
        return ''
    acc_list = makeiter(acc)
    nacc = len(acc_list)
    acc_conf = makeiter( G(keyword + 'AccuracyConfidence'), nacc )
    acc_rel = makeiter( G(keyword + 'AccuracyRelative'), nacc )
    acc_typ = makeiter( G(keyword + 'AccuracyType'), nacc )

    result = []
    for i,ac in enumerate( acc_list ):
        result.append('<Accuracy')
        if acc_conf[i]: result.append( ' confidenceInterval="%s"'%acc_conf[i] )
        if acc_typ[i]: result.append( ' type="%s"'%acc_typ[i] )
        if acc_rel[i]: result.append( ' relative="true"')
        result.append( '>%s</Accuracy>'%ac )

    return ''.join(result)

def makeDataSeriesAccuracyType(keyword, G):
    """
    build the elements for accuracy belonging to a data series.
    """
    errlist = makeiter( G(keyword + "AccuracyErrorList") )
    errfile = G(keyword + "AccuracyErrorFile")
    errval = G(keyword + "AccuracyErrorValue")
    if not (errlist or errfile or errval):
        return ''

    errlistN = G(keyword + "AccuracyErrorListN")
    if errlist and not errlistN:
        errlistN = len(errlist)

    string = makePrimaryType("Accuracy", keyword + "Accuracy", G,
                    extraAttr={"type":G(keyword+"AccuracyType"),
                               "relative":G(keyword+"AccuracyRelative")})
    if errlist:
        string += "<ErrorList count='%s'>%s</ErrorList>" % (errlistN, " ".join(str(o) for o in errlist))
    elif errfile:
        string += "<ErrorFile>%s</ErrorFile>" % errfile
    elif errval:
        string += "<ErrorValue>%s</ErrorValue>" % errval
    string += "</Accuracy>"
    return string

def makeEvaluation(keyword, G, j=None):
    """
    build the elements for evaluation that belong
    to DataType.
    """
    evs = G(keyword + 'Eval')
    if not evs:
        return ''

    if j is not None:
        evs=evs[j]

        ev_list = makeiter(evs)
        nevs = len(ev_list)
        try:
            ev_meth = makeiter( G(keyword + 'EvalMethod')[j], nevs )
        except IndexError:
            ev_meth = makeiter( None, nevs)
        try:
            ev_reco = makeiter( G(keyword + 'EvalRecommended')[j], nevs )
        except IndexError:
            ev_reco = makeiter(None, nevs)
        try:
            ev_refs = G(keyword + 'EvalRef')[j]
        except IndexError:
            ev_refs = []
        try:
            ev_comm = G(keyword + 'EvalComment')[j]
        except IndexError:
            ev_comm = []
    else:
        ev_list = makeiter(evs)
        nevs = len(ev_list)
        ev_meth = makeiter( G(keyword + 'EvalMethod'), nevs )
        ev_reco = makeiter( G(keyword + 'EvalRecommended'), nevs )
        ev_refs = G(keyword + 'EvalRef')
        ev_comm = G(keyword + 'EvalComment')

    result = []
    for i,ev in enumerate( makeiter(evs) ):
        result.append('<Evaluation')
        if ev_meth[i]: result.append( ' methodRef="%s"' % ev_meth[i] )
        if ev_reco[i]: result.append( ' recommended="true"' )
        result.append( '>' )
        result.append( makeSourceRefs(ev_refs) )
        if ev_comm: result.append('<Comments>%s</Comments>'%ev_comm)
        result.append('<Quality>%s</Quality></Evaluation>'%ev)

    return ''.join(result)

def makeDataType(tagname, keyword, G, extraAttr={}, extraElem={}):
    """
    This is for treating the case where a keyword corresponds to a
    DataType in the schema which can have units, comment, sources etc.
    The dictionary-suffixes are appended and the values retrieved. If the
    sources is iterable, it is looped over.

    """

    value = G(keyword)
    if not value:
        return ''
    if isiterable(value):
        return makeRepeatedDataType(tagname, keyword, G)
    unit = G(keyword + 'Unit')
    method = G(keyword + 'Method')
    comment = G(keyword + 'Comment')
    refs = G(keyword + 'Ref')

    result = ['<%s' % tagname]
    if method:
        result.append( ' methodRef="M%s-%s"' % (NODEID, method) )
    for k, v in extraAttr.items():
        if not v: continue
        result.append( ' %s="%s"'% (k, v) )
    result.append( '>' )

    if comment:
        result.append( '<Comments>%s</Comments>' % escape(comment))
    result.append( makeSourceRefs(refs) )
    result.append( '<Value units="%s">%s</Value>' % (unit or 'unitless', value) )

    result.append( makeEvaluation( keyword, G) )
    result.append( makeAccuracy( keyword, G) )
    result.append( '</%s>' % tagname )

    for k, v in extraElem.items():
        if not v: continue
        result.append( '<%s>%s</%s>' % (k, v, k) )

    return ''.join(result)

def makeArgumentType(tagname, keyword, G):
    """
    Build ArgumentType

    """
    string = "<%s name='%s' units='%s'>" % (tagname, G("%sName" % keyword), G("%sUnits" % keyword))
    string +=  makeOptionalTag("Description","%sDescription" % keyword, G)
    string +=  makeOptionalTag("LowerLimit","%sLowerLimit" % keyword, G)
    string +=  makeOptionalTag("UpperLimit","%sUpperLimit" % keyword, G)
    string += "</%s>" % tagname
    return string

def makeParameterType(tagname, keyword, G):
    """
    Build ParameterType

    """
    string = "<%s name='%s' units='%s'>" % (tagname, G("%sName" % keyword), G("%sUnits" % keyword))
    string += "<Description>%s</Description>" % G("%sDescription" % keyword)
    string += "</%s>" % tagname
    return string

def checkXML(obj,methodName='XML'):
    """
    If the queryset has an XML method, use that and
    skip the hard-coded implementation.
    """
    if hasattr(obj,methodName):
        #try:
        return True, getattr(obj,methodName, None)() #This calls the method!
        #except Exception as e:
        #    log.warn('XML-method "%s" on %s failed: %s'%(methodName,obj,e))
        #    return False, None
    else:
        return False, None

def SelfSource(tap):
    now = datetime.datetime.now()
    stamp = now.date().isoformat() + '-%s-%s-%s'%(now.hour,now.minute,now.second)
    result = ['<Source sourceID="B%s-%s">'%(NODEID,stamp)]
    result.append("""
    <Comments>
    This Source is a self-reference.
    It represents the database and the query that produced the xml document.
    The sourceID contains a timestamp.
    The full URL is given in the tag UniformResourceIdentifier but you need
    to unescape ampersands and angle brackets to re-use it.
    Query was: %s
    </Comments>""" % escape(tap.query))
    result.append('<Year>%s</Year>'%now.year)
    result.append('<Category>database</Category>')
    result.append('<UniformResourceIdentifier>')
    result.append(escape(tap.fullurl))
    result.append('</UniformResourceIdentifier>')
    result.append('<ProductionDate>%s</ProductionDate>'%now.date().isoformat())
    result.append('<Authors><Author><Name>N.N.</Name></Author></Authors>')
    result.append('</Source>')
    return ''.join(result)

def XsamsSources(Sources, tap):
    """
    Create the Source tag structure (a bibtex entry)
    """

    yield '<Sources>'
    yield SelfSource(tap)

    if not Sources:
        yield '</Sources>'
        return

    for Source in Sources:
        cont, ret = checkXML(Source)
        if cont:
            yield ret
            continue
        G = lambda name: GetValue(name, Source=Source)
        yield '<Source sourceID="B%s-%s"><Authors>\n' % (NODEID, G('SourceID'))
        authornames = makeiter( G('SourceAuthorName') )
        for authorname in authornames:
            if authorname:
                yield '<Author><Name>%s</Name></Author>\n' % authorname

        yield """</Authors>
<Title>%s</Title>
<Category>%s</Category>
<Year>%s</Year>""" % ( G('SourceTitle'), G('SourceCategory'),
                       G('SourceYear') )

        yield makeOptionalTag('SourceName','SourceName',G)
        yield makeOptionalTag('Volume','SourceVolume',G)
        yield makeOptionalTag('PageBegin','SourcePageBegin',G)
        yield makeOptionalTag('PageEnd','SourcePageEnd',G)
        yield makeOptionalTag('ArticleNumber','SourceArticleNumber',G)
        yield makeOptionalTag('UniformResourceIdentifier','SourceURI',G)
        yield makeOptionalTag('DigitalObjectIdentifier','SourceDOI',G)
        yield makeOptionalTag('Comments','SourceComments',G)
        yield '</Source>\n'
    yield '</Sources>\n'

def XsamsEnvironments(Environments):
    if not isiterable(Environments):
        return
    yield '<Environments>'
    for Environment in Environments:
        cont, ret = checkXML(Environment)
        if cont:
            yield ret
            continue

        G = lambda name: GetValue(name, Environment=Environment)
        yield '<Environment envID="E%s-%s">' % (NODEID, G('EnvironmentID'))
        yield makeSourceRefs(G('EnvironmentRef'))
        yield '<Comments>%s</Comments>' % G('EnvironmentComment')
        yield makeDataType('Temperature', 'EnvironmentTemperature', G)
        yield makeDataType('TotalPressure', 'EnvironmentTotalPressure', G)
        yield makeDataType('TotalNumberDensity', 'EnvironmentTotalNumberDensity', G)
        if hasattr(Environment, "Species"):
            yield '<Composition>'
            for EnvSpecies in makeiter(Environment.Species):
                GS = lambda name: GetValue(name, EnvSpecies=EnvSpecies)
                speciesRef = GS('EnvironmentSpeciesRef')
                if speciesRef:
                    yield '<Species name="%s" speciesRef="X%s-%s">' % (GS('EnvironmentSpeciesName'), NODEID, speciesRef)
                else:
                    yield '<Species name="%s">' % (GS('EnvironmentSpeciesName'))
                yield makeDataType('PartialPressure', 'EnvironmentSpeciesPartialPressure', GS)
                yield makeDataType('MoleFraction', 'EnvironmentSpeciesMoleFraction', GS)
                yield makeDataType('Concentration', 'EnvironmentSpeciesConcentration', GS)
                yield '</Species>'
            yield '</Composition>'
        yield '</Environment>\n'
    yield '</Environments>\n'

def parityLabel(parity):
    """
    XSAMS wants this as strings "odd" or "even", not numerical

    """
    try:
        parity = int(parity)
    except Exception:
        return parity

    if parity % 2:
        return 'odd'
    else:
        return 'even'

def makeTermType(tag, keyword, G):
    """
    Construct the Term xsams structure.

    This version is more generic than XsamsTerm function
    and don't enforce LS/JK/LK to be exclusive to one another (as
    dictated by current version of xsams schema)
    """
    string = "<%s>" % tag

    l = G("%sLSL" % keyword)
    lsym = G("%sLSLSymbol" % keyword)
    s = G("%sLSS" % keyword)
    mult = G("%sLSMultiplicity" % keyword)
    senior = G("%sLSSeniority" % keyword)

    if l and s:
        string += "<LS>"
        string += "<L><Value>%s</Value>"% l
        if lsym: string += "<Symbol>%s</Symbol>" % lsym
        string += "</L><S>%s</S>" % s
        if mult: string += "<Multiplicity>%s</Multiplicity>" % mult
        if senior: string += "<Seniority>%s</Seniority>" % senior
        string += "</LS>"

    jj = makeiter(G("%sJJ" % keyword))
    if jj:
        string += "<jj>"
        for j in jj:
            string += "<j>%s</j>" % j
        string += "</jj>"
    j1j2 = makeiter(G("%sJ1J2" % keyword))
    if j1j2:
        string += "<J1J2>"
        for j in j1j2:
            string += "<j>%s</j>" % j
        string += "</J1J2>"
    K = G("%sJKK" % keyword)
    if K:
        string += "<jK>"
        j = G("%sJKJ" % keyword)
        if j:
            string += "<j>%s</j>" % j
        S2 = G("%sJKS" % keyword)
        if S2:
            string += "<S2>%s</S2>" % S2
        string += "<K>%s</K>" % K
        string += "</jK>"
    l = G("%sLKL" % keyword)
    k = G("%sLKK" % keyword)
    if l and k:
        string += "<LK>"
        string += "<L><Value>%s</Value><Symbol>%s</Symbol></L>" % (l, G("%sLKLSymbol" % keyword))
        string += "<K>%s</K>" % k
        string += "<S2>%s</S2>" % G("%sLKS2" % keyword)
        string += "</LK>"
    tlabel = G("%sLabel" % keyword)
    if tlabel:
        string += "<TermLabel>%s</TermLabel>" % tlabel
    string += "</%s>" % tag
    return string

def makeShellType(tag, keyword, G):
    """
    Creates the Atom shell type.
    """
    sid = G("%sID" % keyword)
    string = "<%s" % tag
    if sid:
        string += ' shellid"=%s-%s"' % (NODEID, sid)
    string += ">"
    string += "<PrincipalQuantumNumber>%s</PrincipalQuantumNumber>" % G("%sPrincipalQN" % keyword)

    string += "<OrbitalAngularMomentum>"
    string += "<Value>%s</Value>" % G("%sOrbitalAngMom" % keyword)
    symb = G("%sOrbitalAngMomSymbol" % keyword)
    if symb:
        string += "<Symbol>%s</Symbol>" % symb
    string += "</OrbitalAngularMomentum>"
    string += "<NumberOfElectrons>%s</NumberOfElectrons>" % G("%sNumberOfElectrons" % keyword)
    parity = G("%sParity" % keyword)
    if (parity):
      string += "<Parity>%s</Parity>" % parity
    kappa = G("%sKappa" % keyword)
    if kappa:
      string += "<Kappa>%s</Kappa>" % kappa
    totalAngularMomentum = G("%sTotalAngularMomentum" % keyword)
    if totalAngularMomentum:
      string += "<TotalAngularMomentum>%s</TotalAngularMomentum>" % totalAngularMomentum
    shellterm = makeTermType("ShellTerm", "%sTerm" % keyword, G)
    if shellterm != "<%s></%s>" % (tag, tag): # shellterm is optional, so don't accept an empty tag
        string += shellterm
    string += "</%s>" % tag
    return string


def makeAtomStateComponents(AtomState):
    """
    This constructs the Atomic Component structure.

    Atom - the current Atom queryset
    """
    if not hasattr(AtomState,'Components'):
        return ''

    string = ""
    for Component in makeiter(AtomState.Components):
        G = lambda name: GetValue(name, Component=Component)

        string += "<Component>"

        if hasattr(Component, "SuperShells"):
            string += "<SuperConfiguration>"
            for SuperShell in makeiter(Component.SuperShells):
                GA = lambda name: GetValue(name, SuperShell=SuperShell)
                string += "<SuperShell>"
                string += "<PrincipalQuantumNumber>%s</PrincipalQuantumNumber>" % GA("AtomStateSuperShellPrincipalQN")
                string += "<NumberOfElectrons>%s</NumberOfElectrons>" % GA("AtomStateSuperShellNumberOfElectrons")
                string += "</SuperShell>"
            string += "</SuperConfiguration>"

        string += "<Configuration>"
        string += "<AtomicCore>"
        ecore = G("AtomStateElementCore")
        if ecore:
            string += "<ElementCore>%s</ElementCore>" % ecore
        conf = G("AtomStateConfiguration")
        if conf:
            # TODO: The format of the Configuration tab is not yet
            # finalized in XSAMS!
            string += "<Configuration>%s</Configuration>" % conf
        string += makeTermType("Term", "AtomStateCoreTerm", G)
        tangmom = G("AtomStateCoreTotalAngMom")
        if tangmom:
            string += "<TotalAngularMomentum>%s</TotalAngularMomentum>" % tangmom
        string += "</AtomicCore>"

        if hasattr(Component, "Shells"):
            string += "<Shells>"
            for AtomShell in makeiter(Component.Shells):
                GS = lambda name: GetValue(name, AtomShell=AtomShell)
                string += makeShellType("Shell", "AtomStateShell", GS)

            if hasattr(Component, "ShellPair"):
                for AtomShellPair in makeiter(Component.ShellPairs):
                    GS = lambda name: GetValue(name, AtomShellPair=AtomShellPair)
                    string += '<ShellPair shellPairID="%s-%s">' % (NODEID, GS("AtomStateShellPairID"))
                    string += makeShellType("Shell1", "AtomStateShellPairShell1", GS)
                    string += makeShellType("Shell2", "AtomStateShellPairShell2", GS)
                    string += makeTermType("ShellPairTerm", "AtomStateShellPairTerm", GS)
                string += "</ShellPair>"

            string += "</Shells>"

        clabel = G("AtomStateConfigurationLabel")
        if clabel:
            string += "<ConfigurationLabel>%s</ConfigurationLabel>" % clabel
        string += "</Configuration>"

        string += makeTermType("Term", "AtomStateTerm", G)
        mixCoe = G("AtomStateMixingCoeff")
        if mixCoe:
            string += '<MixingCoefficient mixingClass="%s">%s</MixingCoefficient>' % (G("AtomStateMixingCoeffClass"), mixCoe)
        coms = G("AtomStateComponentComment")
        if coms:
            string += "<Comments>%s</Comments>" % coms

        string += "</Component>"

    return string

def XsamsAtoms(Atoms):
    """
    Generator (yield) for the main block of XSAMS for the atoms, with an inner
    loop for the states. The QuerySet that comes in needs to have a nested
    QuerySet called States attached to each entry in Atoms.

    """

    if not Atoms: return
    yield '<Atoms>'
    for Atom in makeiter(Atoms):
        cont, ret = checkXML(Atom)
        if cont:
            yield ret
            continue

        G = lambda name: GetValue(name, Atom=Atom)
        yield """<Atom>
<ChemicalElement>
<NuclearCharge>%s</NuclearCharge>
<ElementSymbol>%s</ElementSymbol>
</ChemicalElement><Isotope>""" % (G('AtomNuclearCharge'), G('AtomSymbol'))

        amn = G('AtomMassNumber') #this is mandatory if <IsotopeParameters> is to be filled at all
        if amn:
            yield '<IsotopeParameters><MassNumber>%s</MassNumber>%s' \
                    % (G('AtomMassNumber'), makeDataType('Mass', 'AtomMass', G))
            yield makeOptionalTag('NuclearSpin','AtomNuclearSpin',G)
            yield '</IsotopeParameters>'

        yield '<Ion speciesID="X%s-%s"><IonCharge>%s</IonCharge>' \
                % (NODEID, G('AtomSpeciesID'), G('AtomIonCharge'))
        yield makeOptionalTag('IsoelectronicSequence','AtomIsoelectronicSequence',G)
        if not hasattr(Atom,'States'):
            Atom.States = []
        for AtomState in Atom.States:
            cont, ret = checkXML(AtomState)

            if cont:
                yield ret
                continue
            G = lambda name: GetValue(name, AtomState=AtomState)
#            yield '<AtomicState stateID="S%s-%s">'% (G('NodeID'), G('AtomStateID'))
            yield makePrimaryType("AtomicState", "AtomicState", G,
                                  extraAttr={"stateID":'S%s-%s' % (G('NodeID'), G('AtomStateID')),
                                             "auxillary":G("AtomStateAuxillary")})

            yield makeSourceRefs(G('AtomStateRef'))
            yield makeOptionalTag('Description','AtomStateDescription',G)
            yield '<AtomicNumericalData>'
            yield makeDataType('StateEnergy', 'AtomStateEnergy', G)
            yield makeDataType('IonizationEnergy', 'AtomStateIonizationEnergy', G)
            yield makeDataType('LandeFactor', 'AtomStateLandeFactor', G)
            yield makeDataType('QuantumDefect', 'AtomStateQuantumDefect', G)
            yield makeRepeatedDataType('LifeTime', 'AtomStateLifeTime', G, extraAttr={"decay":G("AtomStateLifeTimeDecay")})
            yield makeDataType('Polarizability', 'AtomStatePolarizability', G)
            statweig = G('AtomStateStatisticalWeight')
            if statweig:
                yield '<StatisticalWeight>%s</StatisticalWeight>' % statweig
            yield makeDataType('HyperfineConstantA', 'AtomStateHyperfineConstantA', G)
            yield makeDataType('HyperfineConstantB', 'AtomStateHyperfineConstantB', G)
            yield '</AtomicNumericalData><AtomicQuantumNumbers>'

            p, j, k, hfm, mqn = G('AtomStateParity'), G('AtomStateTotalAngMom'), \
                                G('AtomStateKappa'), G('AtomStateHyperfineMomentum'), \
                                G('AtomStateMagneticQuantumNumber')

            if p:
                yield '<Parity>%s</Parity>' % parityLabel(p)
            if j:
                yield '<TotalAngularMomentum>%s</TotalAngularMomentum>' % j
            if k:
                yield '<Kappa>%s</Kappa>' % k
            if hfm:
                yield '<HyperfineMomentum>%s</HyperfineMomentum>' % hfm
            if mqn:
                yield '<MagneticQuantumNumber>%s</MagneticQuantumNumber>' % mqn
            yield '</AtomicQuantumNumbers>'

            cont, ret = checkXML(AtomState,'CompositionXML')
            if cont:
                yield ret
            else:
                if hasattr(AtomState, "Components"):
                    yield makePrimaryType("AtomicComposition", "AtomicStateComposition", G)
                    yield makeAtomStateComponents(AtomState)
                    yield '</AtomicComposition>'

            yield '</AtomicState>'
        G = lambda name: GetValue(name, Atom=Atom) # reset G() to Atoms, not AtomStates
        yield '<InChI>%s</InChI>' % G('AtomInchi')
        yield '<InChIKey>%s</InChIKey>' % G('AtomInchiKey')
  #        yield '<VAMDCSpeciesID>%s</VAMDCSpeciesID>' % G('AtomVAMDCSpeciesID')
        yield """</Ion>
</Isotope>
</Atom>"""
    yield '</Atoms>'

# ATOMS END
#
# MOLECULES START
def makeNormalMode(G):

    elstate = G('MoleculeNormalModeElectronicState')
    pointgr = G('MoleculeNormalModePointGroupSymmetry')
    id = G('MoleculeNormalModeID')
    extraAttr = {}
    if elstate: extraAttr['electronicStateRef'] = "S%s-%s" % (NODEID, elstate)
    if pointgr: extraAttr['pointGroupSymmetry'] = pointgr
    if id: extraAttr['id'] = "V%s-%s" % (NODEID, id)
    result = [ makePrimaryType('NormalMode', 'MoleculeNormalMode', G, extraAttr=extraAttr) ]
    result.append( makeDataType('HarmonicFrequency','MoleculeNormalModeHarmonicFrequency',G) )
    result.append( makeDataType('Intensity','MoleculeNormalModeIntensity',G) )

    vsrefs = G('MoleculeNormalModeDisplacementVectorRef')
    unit = G('MoleculeNormalModeDisplacementVectorsUnit')
    x3s = G('MoleculeNormalModeDisplacementVectorX3')
    y3s = G('MoleculeNormalModeDisplacementVectorY3')
    z3s = G('MoleculeNormalModeDisplacementVectorZ3')
    extraAttr = {}
    if unit: extraAttr['units'] = unit
    vsrefs, x3s, y3s, z3s = \
        map(makeiter, [vsrefs, x3s, y3s, z3s])

    if len(x3s)>0:
        result.append( makePrimaryType('DisplacementVectors','MoleculeNormalModeDisplacementVectors',G, extraAttr=extraAttr) ) # TODO-should this be VectorS or Vector?

        for i,x3 in enumerate(x3s):
            result.append('<Vector')
            try: result.append(' ref="%s"'%vsrefs[i])
            except: pass
            try: result.append(' x3="%s"'%x3)
            except: pass
            try: result.append(' y3="%s"'%y3s[i])
            except: pass
            try: result.append(' z3="%s"'%z3s[i])
            except: pass
            result.append('></Vector>')

        result.append('</DisplacementVectors>')

    result.append('</NormalMode>')
    return ''.join(result)

def XsamsMCSBuild(Molecule):
    """
    Generator for the MolecularChemicalSpecies
    """
    G = lambda name: GetValue(name, Molecule=Molecule)
    yield '<MolecularChemicalSpecies>\n'
    yield makeReferencedTextType('OrdinaryStructuralFormula','MoleculeOrdinaryStructuralFormula',G)
    yield '<StoichiometricFormula>%s</StoichiometricFormula>\n'\
            % G("MoleculeStoichiometricFormula")
    yield makeOptionalTag('IonCharge', 'MoleculeIonCharge', G)
    yield makeReferencedTextType('ChemicalName','MoleculeChemicalName',G)
    yield makeReferencedTextType('IUPACName','MoleculeIUPACName',G)
    yield makeOptionalTag('URLFigure','MoleculeURLFigure',G)
    yield makeOptionalTag('InChI','MoleculeInChI',G)
    yield '<InChIKey>%s</InChIKey>\n' % G("MoleculeInChIKey")
    yield makeReferencedTextType('CASRegistryNumber','MoleculeCASRegistryNumber',G)
    yield makeOptionalTag('CNPIGroup','MoleculeCNPIGroup',G)
    yield '<VAMDCSpeciesID>%s</VAMDCSpeciesID>\n' % G("MoleculeVAMDCSpeciesID")

    yield makePartitionfunc("MoleculePartitionFunction", G)

    cont, ret = checkXML(G("MoleculeStructure"), 'CML')
    if cont:
        yield '<MoleculeStructure>\n'
        yield ret
        yield '</MoleculeStructure>\n'

    cont, ret = checkXML(G('NormalModes'))
    if cont:
        yield '<NormalModes>\n'
        yield ret
        yield '</NormalModes>\n'
    elif hasattr(Molecule, 'NormalModes'):
        NMlist = [makeNormalMode(lambda name: GetValue(name, NormalMode=NormalMode)) \
                    for NormalMode in Molecule.NormalModes]
        NMstring = '\n'.join(NMlist)
        if NMstring:
            yield '<NormalModes>\n%s</NormalModes>\n'%NMstring

    yield '<StableMolecularProperties>\n%s</StableMolecularProperties>\n' % makeDataType('MolecularWeight', 'MoleculeMolecularWeight', G)
    if G("MoleculeComment"):
        yield '<Comment>%s</Comment>\n' % escape(G("MoleculeComment"))
    yield '</MolecularChemicalSpecies>\n'

def makeCaseQNs(G):
    """
    Build the Case tag with the QNs

    Note: order of QNs matters in xsams.
    """
    case = G('MoleculeQNCase')
    if not case: return ''

    result = [
        '<Case xsi:type="case:Case" caseID="%s" xmlns:case="http://vamdc.org/xml/xsams/%s/cases/%s">' % (case, XSAMS_VERSION, case),
        '<case:QNs>',
        makeOptionalTag('case:ElecStateLabel', 'MoleculeQNElecStateLabel', G)]
    elecSym, elecSymGroup = G("MoleculeQNelecSym"), G("MoleculeQNelecSymGroup")
    if elecSym:
        if elecSymGroup:
            result.append('<case:elecSym group="%s">%s</case:elecSym>' % (elecSymGroup, elecSym))
        else:
            result.append('<case:elecSym>%s</case:elecSym>' % elecSym)

    result.extend([
            makeOptionalTag('case:elecInv', 'MoleculeQNelecInv', G),
            makeOptionalTag('case:elecRefl', 'MoleculeQNelecRefl', G),
            makeOptionalTag('case:Lambda', 'MoleculeQNLambda', G),
            makeOptionalTag('case:Sigma', 'MoleculeQNSigma', G),
            makeOptionalTag('case:Omega', 'MoleculeQNOmega', G),
            makeOptionalTag('case:S', 'MoleculeQNS', G)])
    result.extend(['<case:vi mode="%s">%s</case:vi>' %
                   (makeiter(G("MoleculeQNviMode"))[i],val)
                   for i, val in enumerate(makeiter(G("MoleculeQNvi")))])
    result.extend(['<case:li mode="%s">%s</case:li>' %
                   (makeiter(G("MoleculeQNliMode"))[i],val)
                   for i, val in enumerate(makeiter(G("MoleculeQNli")))])
    result.extend([
            makeOptionalTag('case:v', 'MoleculeQNv', G),
            makeOptionalTag('case:l', 'MoleculeQNl', G),
            makeOptionalTag('case:vibInv', 'MoleculeQNvibInv', G),
            makeOptionalTag('case:vibRefl', 'MoleculeQNvibRefl', G)])
    vibSym, vibSymGroup = G("MoleculeQNvibSym"), G("MoleculeQNvibSymGroup")
    if vibSym:
        if vibSymGroup:
            result.append('<case:vibSym group="%s">%s</case:vibSym>' % (vibSymGroup,vibSym))
        else:
            result.append('<case:vibSym>%s</case:vibSym>' % vibSym)
    result.extend([
            makeOptionalTag('case:v1', 'MoleculeQNv1', G),
            makeOptionalTag('case:v2', 'MoleculeQNv2', G),
            makeOptionalTag('case:l2', 'MoleculeQNl2', G),
            makeOptionalTag('case:v3', 'MoleculeQNv3', G),
            makeOptionalTag('case:J', 'MoleculeQNJ', G),
            makeOptionalTag('case:K', 'MoleculeQNK', G),
            makeOptionalTag('case:N', 'MoleculeQNN', G),
            makeOptionalTag('case:Ka', 'MoleculeQNKa', G),
            makeOptionalTag('case:Kc', 'MoleculeQNKc', G)])
    rotSym, rotSymGroup = G("MoleculeQNrotSym"), G("MoleculeQNrotSymGroup")
    if rotSym:
        if rotSymGroup:
            result.append('<case:rotSym group="%s">%s</case:rotSym>' % (rotSymGroup,rotSym))
        else:
            result.append('<case:rotSym>%s</case:rotSym>' % rotSym)
    rovibSym, rovibSymGroup = G("MoleculeQNrovibSym"), G("MoleculeQNrovibSymGroup")
    if rovibSym:
        if rovibSymGroup:
            result.append('<case:rovibSym group="%s">%s</case:rovibSym>' % (rovibSymGroup,rovibSym))
        else:
            result.append('<case:rovibSym>%s</case:rovibSym>' % rovibSym)
    result.extend([
            makeOptionalTag('case:I', 'MoleculeQNI', G, extraAttr={"nuclearSpinRef":G("MoleculeQNInuclSpin")}),
            makeOptionalTag('case:SpinComponentLabel', 'MoleculeQNSpinComponentLabel', G)])
    result.extend(['<case:Fj j="%s" nuclearSpinRef="%s">%s</case:Fj>' %
                   (makeiter(G("MoleculeQNFjj"))[i], makeiter(G("MoleculeQNFjnuclSpin"))[i], val)
                   for i, val in enumerate(makeiter(G("MoleculeQNFj")))])
    result.extend([
            makeOptionalTag('case:F1', 'MoleculeQNF1', G, extraAttr={"nuclearSpinRef":G("MoleculeQNF1nuclSpin")}),
            makeOptionalTag('case:F2', 'MoleculeQNF2', G, extraAttr={"nuclearSpinRef":G("MoleculeQNF2nuclSpin")}),
            makeOptionalTag('case:F', 'MoleculeQNF', G, extraAttr={"nuclearSpinRef":G("MoleculeQNFnuclSpin")})])
    result.extend(['<case:r name="%s">%s</case:r>'%(makeiter(G("MoleculeQNrName"))[i],val)
                   for i,val in enumerate(makeiter(G("MoleculeQNr")))])
    result.extend([
            makeOptionalTag('case:parity', 'MoleculeQNparity', G),
            makeOptionalTag('case:kronigParity', 'MoleculeQNkronigParity', G),
            makeOptionalTag('case:asSym', 'MoleculeQNasSym', G),
            "</case:QNs>",
            "</Case>"])
    return "".join(result)

def makeCaseBSQNs(G):
    """
    Build the Case tag with the BasisState QNs

    Note: order of QNs matters in xsams.
    """
    case = G('MoleculeQNCase')
    if not case: return ''

    result = [
        '<Case xsi:type="case:Case" caseID="%s" xmlns:case="http://vamdc.org/xml/xsams/%s/cases/%s">' % (case, XSAMS_VERSION, case),
        '<case:QNs>']

    result.extend(['<case:vi mode="%s">%s</case:vi>' %
                   (makeiter(G("MoleculeBQNviMode"))[i],val)
                   for i, val in enumerate(makeiter(G("MoleculeBQNvi")))])
    result.extend(['<case:li mode="%s">%s</case:li>' %
                   (makeiter(G("MoleculeBQNliMode"))[i],val)
                   for i, val in enumerate(makeiter(G("MoleculeBQNli")))])
    result.extend(['<case:r name="%s">%s</case:r>'%(makeiter(G("MoleculeBQNrName"))[i],val)
                   for i,val in enumerate(makeiter(G("MoleculeBQNr")))])
    result.extend(['<case:sym name="%s">%s</case:sym>'%(makeiter(G("MoleculeBQNsymName"))[i],val)
                   for i,val in enumerate(makeiter(G("MoleculeBQNsym")))])
    result.extend([
            "</case:QNs>",
            "</Case>\n"])
    return "".join(result)

def XsamsMSBuild(MoleculeState):
    """
    Generator for MolecularState tag
    """
    G = lambda name: GetValue(name, MoleculeState=MoleculeState)
    yield makePrimaryType("MolecularState", "MoleculeState", G,
            extraAttr={"stateID":'S%s-%s' % (G('NodeID'), G('MoleculeStateID')),
                       "fullyAssigned":G("MoleculeStateFullyAssigned"),"auxillary":G("MoleculeStateAuxillary")})
    yield makeOptionalTag("Description","MoleculeStateDescription",G)

    yield '  <MolecularStateCharacterisation>'
    yield makeDataType('StateEnergy', 'MoleculeStateEnergy', G,
                extraAttr={'energyOrigin':'S%s-%s' % (G('NodeID'), G('MoleculeStateEnergyOrigin'))})
    yield makeOptionalTag("TotalStatisticalWeight", "MoleculeStateTotalStatisticalWeight", G)
    yield makeOptionalTag("NuclearStatisticalWeight", "MoleculeStateNuclearStatisticalWeight", G)
#    yield makeOptionalTag("NuclearSpinIsomer", "MoleculeStateNuclearSpinIsomer", G)
    if G("MoleculeStateNSIName"):
        yield makePrimaryType("NuclearSpinIsomer", "NuclearSpinIsomer",G,
                              extraAttr={"lowestEnergyStateRef":'S%s-%s' % (G('NodeID'), G('MoleculeStateNSILowestEnergyStateRef'))})
        yield "<Name>%s</Name>" % G("MoleculeStateNSIName")
        yield "<LowestRoVibSym group='%s'>%s</LowestRoVibSym>" % (G('MoleculeStateNSISymGroup'), G('MoleculeStateNSILowestRoVibSym'))
        yield "</NuclearSpinIsomer>"

    if G("MoleculeStateLifeTime"):
        # note: currently only supporting 0..1 lifetimes (xsams dictates 0..3)
        # the decay attr is a string, either: 'total', 'totalRadiative' or 'totalNonRadiative'
        yield makeDataType('LifeTime','MoleculeStateLifeTime', G, extraAttrs={'decay':G('MoleculeStateLifeTimeDecay')})
    if hasattr(MoleculeState, "Parameters"):
        for Parameter in makeiter(MoleculeState.Parameters):
            cont, ret = checkXML(Parameter)
            if cont:
                yield ret
                continue
            GP = lambda name: GetValue(name, Parameter=Parameter)
            yield makePrimaryType("Parameters","MoleculeStateParameters", GP)
            if GP("MoleculeStateParametersValueData"):
                yield makeDataType("ValueData", "MoleculeStateParametersValueData", GP)
            if GP("MoleculeStateParametersVectorData"):
                yield makePrimaryType("VectorData", "MoleculeStateParametersVectorData", GP, extraAttr={"units":GP("MoleculeStateParametersVectorUnits")})
                if hasattr(Parameter, "Vector"):
                    for VectorValue in makeiter(Parameter.Vector):
                        GPV = lambda name: GetValue(name, VectorValue)
                        yield makePrimaryType("Vector", "MoleculeStateParameterVector", GPV,
                                              extraAttr={"ref":GPV("MoleculeStateParameterVectorRef"),
                                                         "x3":GPV("MoleculeStateParameterVectorX3"),
                                                         "y3":GPV("MoleculeStateParameterVectorY3"),
                                                         "z3":GPV("MoleculeStateParameterVectorZ3")})
                        yield "</Vector>"
                yield "</VectorData>"
            if GP("MoleculeStateParametersMatrixData"):
                yield makePrimaryType("MatrixData", "MoleculeStateParametersMatrixData", GP,
                                      extraAttr={"units":GP("MoleculeStateParametersMatrixUnits"),
                                                 "nrows":GPV("MoleculeStateParametersMatrixNrows"),
                                                 "ncols":GP("MoleculeStateParametersMatrixNcols"),
                                                 "form":GP("MoleculeStateParametersMatrixForm"),
                                                 "values":GP("MoleculeStateParametersMatrixValues")})
                yield "<RowRefs>%s</RowRefs>" % GP("MoleculeStateParametersMatrixDataRowRefs") # space-separated list of strings
                yield "<ColRefs>%s</ColRefs>" % GP("MoleculeStateParametersMatrixDataColRefs") # space-separated list of strings
                yield "<Matrix>%s</Matrix>" % GP("MoleculeStateParametersMatrixDataMatrix") # space-separated list of strings
                yield "</MatrixData>"
            yield "</Parameters>"
    yield '  </MolecularStateCharacterisation>\n'
    yield makeOptionalTag("Parity", "MoleculeStateParity", G)

    cont, ret = checkXML(G("MoleculeStateQuantumNumbers"))
    if cont:
        yield ret
    else:
        yield makeCaseQNs(G)

    # commented out at the moment, need to confer on names to use, and rework makeCaseQNs(). /SR
    if hasattr(MoleculeState, "Expansions"):
        for Expansion in makeiter(MoleculeState.Expansions):
            cont, ret = checkXML(Expansion)
            if cont:
                yield ret
                continue
            GE = lambda name: GetValue(name, Expansion=Expansion)
            yield makePrimaryType("StateExpansion", "MoleculeStateExpansion", GE)
            for i,val in enumerate(makeiter(G("MoleculeStateExpansionCoeff"))):
               #yield "<Coeff stateRef=S%s-B%s>%s</Coeff>" % (G('NODEID'),makeiter(G("MoleculeStateExpansionCoeffStateRef"))[i],val)
                yield '<Coeff basisStateRef="SB%s-%s">%s</Coeff>' % (G('NODEID'),makeiter(G("MoleculeStateExpansionCoeffStateRef"))[i],val)
            yield "</StateExpansion>"

    yield '</MolecularState>'

def XsamsBSBuild(MoleculeBasisState):
    G = lambda name: GetValue(name, MoleculeBasisState=MoleculeBasisState)
    cont, ret = checkXML(MoleculeBasisState)
    if cont:
        yield ret
    else:
        yield makePrimaryType("BasisState", "MoleculeBasisState", G,
            extraAttr={"basisStateID":'SB%s-%s' % (G('NodeID'),
                                                   G('MoleculeBasisStateID')),})
        cont, ret = checkXML(G("BasisStateQuantumNumbers"))
        if cont:
            yield ret
        else:
            yield makeCaseBSQNs(G)
        yield '</BasisState>'

def XsamsMolecules(Molecules):
    """
    Generator for Molecules tag
    """
    if not Molecules: return
    yield '<Molecules>\n'
    for Molecule in makeiter(Molecules):
        cont, ret = checkXML(Molecule)
        if cont:
            yield ret
            continue
        G = lambda name: GetValue(name, Molecule=Molecule)
        yield '<Molecule speciesID="X%s-%s">\n' % (NODEID,
                                                   G("MoleculeSpeciesID"))

        # write the MolecularChemicalSpecies description:
        for MCS in XsamsMCSBuild(Molecule):
            yield MCS

        if hasattr(Molecule, 'BasisStates'):
            yield makePrimaryType('BasisStates', 'MoleculeBasisStates', G)
            for MoleculeBasisState in Molecule.BasisStates:
                for BS in XsamsBSBuild(MoleculeBasisState):
                    yield BS
            yield '</BasisStates>\n'

        if not hasattr(Molecule,'States'):
            Molecule.States = []
        for MoleculeState in Molecule.States:
            for MS in XsamsMSBuild(MoleculeState):
                yield MS
        yield '</Molecule>\n'
    yield '</Molecules>\n'


def XsamsSolids(Solids):
    """
    Generator for Solids tag
    """
    if not Solids:
        return
    yield "<Solids>"
    for Solid in makeiter(Solids):
        cont, ret = checkXML(Solid)
        if cont:
            yield ret
            continue
        G = lambda name: GetValue(name, Solid=Solid)
        yield makePrimaryType("Solid", "Solid", G, extraAttr={"speciesID":"S%s-%s" % (NODEID, G("SolidSpeciesID"))})
        if hasattr(Solid, "Layers"):
            for Layer in makeiter(Solid.Layers):
                GL = lambda name: GetValue(name, Layer=Layer)
                yield "<Layer>"
                yield "<MaterialName>%s</MaterialName>" % GL("SolidLayerName")
                if hasattr(Solid, "Components"):
                    makePrimaryType("MaterialComposition", "SolidLayerComponent")
                    for Component in makeiter(Layer.Components):
                        GLC = lambda name: GetValue(name, Component=Component)
                        yield "<ChemicalElement>"
                        yield "<NuclearCharge>%s</NuclearCharge>" % GLC("SolidLayerComponentNuclearCharge")
                        yield "<ElementSymbol>%s</ElementSymbol>" % GLC("SolidLayerComponentElementSymbol")
                        yield "</ChemicalElement>"
                        yield "<StochiometricValue>%s</StochiometricValue>" % GLC("SolidLayerComponentStochiometricValue")
                        yield "<Percentage>%s</Percentage>" % GLC("SolidLayerComponentPercentage")
                    yield "</MaterialComposition>"
                makeDataType("MaterialThickness", "SolidLayerThickness", GL)
                yield "<MaterialTopology>%s</MaterialThickness>" % GL("SolidLayerTopology")
                makeDataType("MaterialTemperature", "SolidLayerTemperature", GL)
                yield "<Comments>%s</Comments>" % GL("SolidLayerComment")
                yield "</Layer>"
        yield "</Solid>"
    yield "</Solids>"

def XsamsParticles(Particles):
    """
    Generator for Particles tag.
    """
    if not Particles:
        return
    yield "<Particles>"
    for Particle in makeiter(Particles):
        cont, ret = checkXML(Particle)
        if cont:
            yield ret
            continue
        G = lambda name: GetValue(name, Particle=Particle)
        yield makePrimaryType("Particle", "Particle", G,
         extraAttr={'speciesID':"X%s-%s"%(G('NodeID'), G('ParticleSpeciesID')),
                    'name':"%s"%G('ParticleName')})
        yield "<ParticleProperties>"
        charge = G("ParticleCharge")
        if charge :
            yield "<ParticleCharge>%s</ParticleCharge>" % charge
        yield makeDataType("ParticleMass", "ParticleMass", G)
        spin = G("ParticleSpin")
        if spin:
            yield "<ParticleSpin>%s</ParticleSpin>" % spin
        polarization = G("ParticlePolarization")
        if polarization  :
            yield "<ParticlePolarization>%s</ParticlePolarization>" % polarization
        yield "</ParticleProperties>"
        yield "</Particle>"
    yield "</Particles>"

###############
# END SPECIES
# BEGIN PROCESSES
#################

def makeBroadeningType(G, name='Natural'):
    """
    Create the Broadening tag
    """
    lsparams = makeNamedDataType('LineshapeParameter','RadTransBroadening%sLineshapeParameter' % name, G)
    if not lsparams:
        return ''

    env = G('RadTransBroadening%sEnvironment' % name)
    meth = G('RadTransBroadening%sMethod' % name)
    comm = G('RadTransBroadening%sComment' % name)
    realname = name.lower()
    if realname.startswith('pressure') and not (realname=='pressure'):
        realname=realname.replace('pressure','pressure-')
    s = '<Broadening name="%s"' % realname
    if meth:
        s += ' methodRef="M%s-%s"' % (NODEID, meth)
    if env:
        s += ' envRef="E%s-%s"' % (NODEID, env)
    s += '>'
    if comm:
        s +='<Comments>%s</Comments>' % comm
    s += makeSourceRefs(G('RadTransBroadening%sRef' % name))

    # in principle we should loop over lineshapes but
    # lets not do so unless somebody actually has several lineshapes
    # per broadening type             RadTransBroadening%sLineshapeName
    funcref = G("RadTransBroadening%sLineshapeFunction" % name) or None
    if funcref:
        s += '<Lineshape name="%s" functionRef="F%s-%s">' % (G('RadTransBroadening%sLineshapeName' % name), NODEID, funcref)
    else:
        s += '<Lineshape name="%s">' % G('RadTransBroadening%sLineshapeName' % name)
    s += lsparams
    s += '</Lineshape>'
    s += '</Broadening>'
    return s

def XsamsRadTranBroadening(G):
    """
    helper function for line broadening, called from RadTrans

    allowed names are:
     Pressure - collisional broadenings
     PressureNeutral - collisional, neutral perturbers (e.g. vad der Waals)
     PressureCharged - collisional between charged(ionized) perturbers (e.g. Stark)
     Doppler - doppler broadening
     Instrument - instrument-specific broadening
     Natural - for line broadening caused by finite lifetime of initial and final states.
               Usually, Lorentzian line profile should be used.

     Each broadening object can also optionally hold an iterable property "Broadening" for
     subclassing.
    """
    s=[]
    broadenings = ('Natural', 'Instrument', 'Doppler', 'Pressure', 'PressureNeutral', 'PressureCharged')
    for broadening in broadenings :
        if hasattr(G('RadTransBroadening'+broadening), "Broadenings"):
            for Broadening in  makeiter(G('RadTransBroadening'+broadening).Broadenings):
                GB = lambda name: GetValue(name, Broadening=Broadening)
                s.append( makeBroadeningType(GB, name=broadening) )
        else:
            s.append( makeBroadeningType(G, name=broadening) )
    return ''.join(s)



def XsamsRadTranShifting(RadTran):
    """
    Shifting type
    """
    string = ""
    if hasattr(RadTran, "Shiftings"):
        for Shifting in makeiter(RadTran.Shiftings):
            G = lambda name: GetValue(name, Shifting=Shifting)
            dic = {}
            nam = G("RadTransShiftingName")
            eref = G("RadTransShiftingEnv")
            if nam:
                dic["name"] = nam
            if eref:
                dic["envRef"] = "E%s-%s"  % (NODEID, eref)
            string += makePrimaryType("Shifting", "RadTransShifting", G, extraAttr=dic)
            if hasattr(Shifting, "ShiftingParams"):
                for ShiftingParam in Shifting.ShiftingParams:
                    GS = lambda name: GetValue(name, ShiftingParam=ShiftingParam)
                    string += makePrimaryType("ShiftingParameter", "RadTransShiftingParam", GS, extraAttr={"name":GS("RadTransShiftingParamName")})
                    val = GS("RadTransShiftingParamUnit")
                    if val:
                        string += "<Value units='%s'>%s</Value>" % (val, GS("RadTransShiftingParam" ))
                    string += makeAccuracy('RadTransShiftingParam', GS)


                    if hasattr(ShiftingParam, "Fit"):
                        for Fit in makeiter(ShiftingParam.Fits):
                            GSF = lambda name: GetValue(name, Fit=Fit)
                            string += "<FitParameters functionRef='F%s-%s'>" % (NODEID, GSF("RadTransShiftingParamFitFunction"))

                            # hard-code to avoid yet anoter named loop variable
                            for name, units, desc, llim, ulim in makeloop("RadTransShiftingParamFitArgument", GSF, "Name", "Units", "Description", "LowerLimit", "UpperLimit"):
                                string += "<FitArgument name='%s' units='%s'>" % (name, units)
                                string += "<Description>%s</Description>" % desc
                                string += "<LowerLimit>%s</LowerLimit>" % llim
                                string += "<UpperLimit>%s</UpperLimit>" % ulim
                                string += "</FitArgument>"
                                return string

                            if hasattr(Fit, "Parameters"):
                                for Parameter in makeiter(Fit.Parameters):
                                    GSFP = lambda name: GetValue(name, Parameter=Parameter)
                                    string += makeNamedDataType("FitParameter", "RadTransShiftingParamFitParameter", GSFP)
                            string += "</FitParameters>"

                    string += "</ShiftingParameter>"

            string += "</Shifting>"

    return string

def XsamsRadTrans(RadTrans):
    """
    Generator for the XSAMS radiative transitions.
    """
    if not isiterable(RadTrans):
        return

    for RadTran in RadTrans:
        cont, ret = checkXML(RadTran)
        if cont:
            yield ret
            continue

        G = lambda name: GetValue(name, RadTran=RadTran)
        group = G('RadTransGroup')
        proc = G('RadTransProcess')
        attrs=''
        if group: attrs += ' groupLabel="%s"'%group
        if proc: attrs += ' process="%s"'%proc
        yield '<RadiativeTransition id="P%s-R%s"%s>'%(NODEID,G('RadTransID'),attrs)
        yield makeOptionalTag('Comments','RadTransComment',G)
        yield makeSourceRefs(G('RadTransRefs'))
        yield '<EnergyWavelength>'
        yield makeDataType('Wavenumber', 'RadTransWavenumber', G)
        yield makeDataType('Wavelength', 'RadTransWavelength', G,
                extraAttr={'envRef':G('RadTransWavelengthEnv'),
                    'vacuum':G('RadTransWavelengthVacuum')},
                extraElem={'AirToVacuum':G('RadTransWavelengthAirToVac')})
        yield makeDataType('Frequency', 'RadTransFrequency', G)
        yield makeDataType('Energy', 'RadTransEnergy', G)
        yield '</EnergyWavelength>'

        upper = G('RadTransUpperStateRef')
        if upper:
            yield '<UpperStateRef>S%s-%s</UpperStateRef>\n' % (NODEID, upper)
        lower = G('RadTransLowerStateRef')
        if lower:
            yield '<LowerStateRef>S%s-%s</LowerStateRef>\n' % (NODEID, lower)
        species = G('RadTransSpeciesRef')
        if species:
            yield '<SpeciesRef>X%s-%s</SpeciesRef>\n' % (NODEID, species)

        yield '<Probability>'
        yield makeDataType('TransitionProbabilityA', 'RadTransProbabilityA', G)
        yield makeDataType('OscillatorStrength', 'RadTransProbabilityOscillatorStrength', G)
        yield makeDataType('LineStrength', 'RadTransProbabilityLineStrength', G)
        yield makeDataType('WeightedOscillatorStrength', 'RadTransProbabilityWeightedOscillatorStrength', G)
        yield makeDataType('Log10WeightedOscillatorStrength', 'RadTransProbabilityLog10WeightedOscillatorStrength', G)
        yield makeDataType('IdealisedIntensity', 'RadTransProbabilityIdealisedIntensity', G)
        yield makeOptionalTag('Multipole','RadTransProbabilityMultipole',G)
        yield makeOptionalTag('TransitionKind','RadTransProbabilityKind',G)
        yield makeDataType('EffectiveLandeFactor', 'RadTransEffectiveLandeFactor', G)
        yield '</Probability>\n'

        yield "<ProcessClass>"
        yield makeOptionalTag('UserDefinition', 'RadTransUserDefinition',G)
        yield makeOptionalTag('Code','RadTransCode',G)
        yield makeOptionalTag('IAEACode','RadTransIAEACode',G)
        yield "</ProcessClass>"

        if hasattr(RadTran, 'XML_Broadening'):
            yield RadTran.XML_Broadening()
        else:
            yield XsamsRadTranBroadening(G)
        if hasattr(RadTran, 'XML_Shifting'):
            yield RadTran.XML_Shifting()
        else:
            yield XsamsRadTranShifting(RadTran)
        yield '</RadiativeTransition>\n'

def makeDataSeriesType(tagname, keyword, G):
    """
    Creates the dataseries type
    """
    result=[]
    dic = {}
    xpara = G("%sParameter" % keyword)
    if xpara:
        dic["parameter"] = "%sParameter" % keyword
    xunits = G("%sUnit" % keyword)
    if xunits:
        dic["units"] = xunits
    xid = G("%sID" % keyword)
    if xid:
        dic["id"] = "%s-%s" % (NODEID, xid)
    result.append(makePrimaryType("%s" % tagname, "%s" % keyword, G, extraAttr=dic))

    dlist = makeiter(G("%s" % keyword))
    if dlist:
        result.append("<DataList count='%s'>%s</DataList>" % (G("%sN" % keyword), " ".join(str(d) for d in dlist)))

    csec = G("%sLinearA0" % keyword) and G("%sLinearA1" % keyword)
    if csec:
        dic = {"initial":G("%sLinearInitial" % keyword), "increment":G("%sLinearIncrement" % keyword)}
        nx = G("%sLinearCount" % keyword)
        if nx:
            dic["count"] = nx
        xunits = G("%sLinearUnits" % keyword)
        if xunits:
            dic["units"] = xunits
        result.append(makePrimaryType("LinearSequence", "%sLinear" % keyword, G, extraAttr=dic))
        result.append("</LinearSequence>")
    dfile = G("%sDataFile" % keyword)
    if dfile:
        result.append("<DataFile>%s</DataFile>" % dfile)
    elist = makeiter(G("%sErrorList" % keyword))
    if elist:
        result.append("<ErrorList n='%s' units='%s'>%s</ErrorList>" % (G("%sErrorListN" % keyword), G("%sErrorListUnits" % keyword), " ".join(str(e) for e in elist)))
    err = G("%sError" % keyword)
    if err:
        result.append("<Error>%s</Error>" % err)

    result.append("</%s>" % tagname)
    return ''.join(result)


def XsamsRadCross(RadCross):
    """
    for the Radiative/CrossSection part

    querysets and nested querysets:

    RadCros
      RadCros.BandAssignments
        BandAssignment.Modes
          Mode.DeltaVs

    loop varaibles:

    RadCros
      RadCrosBandAssignment
        RadCrosBandAssigmentMode
          RadCrosBandAssignmentModeDeltaV
    """

    if not isiterable(RadCross):
        return

    for RadCros in RadCross:
        cont, ret = checkXML(RadCros)
        if cont:
            yield ret
            continue

        # create header

        G = lambda name: GetValue(name, RadCros=RadCros)
        dic = {'id':"P%s-CS%s" % (NODEID, G("CrossSectionID")) }

        envRef = G("CrossSectionEnvironment")
        if envRef:
            dic["envRef"] = "E%s-%s" % (NODEID, envRef)
        group = G("CrossSectionGroup")
        if group:
            dic["groupLabel"] = "%s" % group

        yield makePrimaryType("AbsorptionCrossSection", "CrossSection", G, extraAttr=dic)
        yield "<Description>%s</Description>" % G("CrossSectionDescription")

        yield makeDataSeriesType("X", "CrossSectionX", G)
        yield makeDataSeriesType("Y", "CrossSectionY", G)

        species = G("CrossSectionSpecies")
        state = G("CrossSectionState")
        if species or state:
            yield "<Species>"
            if species:
                yield "<SpeciesRef>X%s-%s</SpeciesRef>" % (NODEID, species)
            if state:
                yield "<StateRef>S%s-%s</StateRef>" % (NODEID, state)
            yield "</Species>"

        # Note - XSAMS dictates a list of BandAssignments here; but this is probably unlikely to
        # be used; so for simplicity we only assume one band assignment here.

        yield makePrimaryType("BandAssignment", "CrossSectionBand", G, extraAttr={"name":G("CrossSectionBandName")})

        yield makeDataType("BandCentre", "CrossSectionBandCentre", G)
        yield makeDataType("BandWidth", "CrossSectionBandWidth", G)

        if hasattr(RadCros, "Modes"):
            for BandMode in RadCros.BandModes:

                cont, ret = checkXML(BandMode)
                if cont:
                    yield ret
                    continue

                GM = lambda name: GetValue(name, BandMode=BandMode)
                yield makePrimaryType("Modes", "CrossSectionBandMode", GM, extraAttr={"name":GM("CrossSectionBandModeName")})

                for deltav, modeid in makeloop("CrossSectionBandMode", GM, "DeltaV", "DeltaVModeID"):
                    if modeid:
                        yield "<DeltaV modeID=V%s-%s>%s</DeltaV>" % (deltav, NODEID, modeid)
                    else:
                        yield "<DeltaV>%s</DeltaV>" % deltav
                yield "</Modes>"
        yield "</BandAssignment>"
        yield "</AbsorptionCrossSection>"


def XsamsCollTrans(CollTrans):
    """
    Collisional transitions.
    QuerySets and nested querysets:
    # CollTran
    #  CollTran.Reactants
    #  CollTran.IntermediateStates
    #  CollTran.Products
    #  CollTran.DataSets
    #    DataSet.FitData
    #      FitData.Arguments
    #      FitData.Parameters
    #    DataSet.TabulatedData

    Matching loop variables to use:
    # CollTran
    #  CollTranReactant
    #  CollTranIntermediateState
    #  CollTranProduct
    #  CollTranDataSet
    #    CollTranFitData
    #      CollTranFitDataArgument
    #      CollTranFitDataParameter
    #    CollTranTabulatedData
    """

    if not isiterable(CollTrans):
        return
    yield "<Collisions>"
    for CollTran in CollTrans:

        cont, ret = checkXML(CollTran)
        if cont:
            yield ret
            continue

        # create header
        G = lambda name: GetValue(name, CollTran=CollTran)
        dic = {'id':"P%s-C%s" % (NODEID, G("CollisionID")) }
        group = G("CollisionGroup")
        if group:
            dic["groupLabel"] = "%s" % group
        yield makePrimaryType("CollisionalTransition", "Collision", G, extraAttr=dic)

        yield "<ProcessClass>"
        yield makeOptionalTag('UserDefinition', 'CollisionUserDefinition',G)
        yield makeOptionalTag('Code','CollisionCode',G)
        yield makeOptionalTag('IAEACode','CollisionIAEACode',G)
        yield "</ProcessClass>"

        if hasattr(CollTran, "Reactants"):
            for Reactant in CollTran.Reactants:

                cont, ret = checkXML(Reactant)
                if cont:
                    yield ret
                    continue

                GR = lambda name: GetValue(name, Reactant=Reactant)
                yield "<Reactant>"
                species = GR("CollisionReactantSpecies")
                if species:
                    yield "<SpeciesRef>X%s-%s</SpeciesRef>" % (NODEID, species)
                state = GR("CollisionReactantState")
                if state:
                    yield "<StateRef>S%s-%s</StateRef>" % (NODEID, state)
                yield "</Reactant>"

        if hasattr(CollTran, "IntermediateStates"):
            for IntermdiateState in CollTran.IntermediateStates:

                cont, ret = checkXML(IntermdiateState)
                if cont:
                    yield ret
                    continue

                GI = lambda name: GetValue(name, IntermdiateState=IntermdiateState)
                yield "<IntermediateState>"
                species = GI("CollisionIntermediateSpecies")
                if species:
                    yield "<SpeciesRef>X%s-%s</SpeciesRef>" % (NODEID, species)
                state = GI("CollisionIntermediateState")
                if state:
                    yield "<StateRef>S%s-%s</StateRef>" % (NODEID, state)
                yield "</IntermediateState>"

        if hasattr(CollTran, "Products"):
            for Product in CollTran.Products:

                cont, ret = checkXML(Product)
                if cont:
                    yield ret
                    continue

                GP = lambda name: GetValue(name, Product=Product)
                yield "<Product>"
                species = GP("CollisionProductSpecies")
                if species:
                    yield "<SpeciesRef>X%s-%s</SpeciesRef>" % (NODEID, species)
                state = GP("CollisionProductState")
                if state:
                    yield "<StateRef>S%s-%s</StateRef>" % (NODEID, state)
                species = GP("CollisionProductSpecies")
                yield "</Product>"

        yield makeDataType("Threshold", "CollisionThreshold", G)
        yield makeDataType("BranchingRatio", "CollisionBranchingRatio", G)

        if hasattr(CollTran, "DataSets"):
            yield "<DataSets>"
            for DataSet in CollTran.DataSets:
                cont, ret = checkXML(DataSet)
                if cont:
                    yield ret
                    continue

                GD = lambda name: GetValue(name, DataSet=DataSet)

                yield makePrimaryType("DataSet", "CollisionDataSet", GD, extraAttr={"dataDescription":GD("CollisionDataSetDescription")})

                # Fit data
                if hasattr(DataSet, "FitData"):
                    for FitData in DataSet.FitData:

                            cont, ret = checkXML(FitData)
                            if cont:
                                yield ret
                                continue

                            GDF = lambda name: GetValue(name, FitData=FitData)

                            yield makePrimaryType("FitData", "CollisionFitData", GDF)

                            fref = GDF("CollisionFitDataFunction")
                            if fref:
                                yield "<FitParameters functionRef='F%s-%s'>" % (NODEID, fref)
                            else:
                                yield "<FitParameters>"

                            if hasattr(FitData, "Arguments"):
                                for Argument in FitData.Arguments:

                                    cont, ret = checkXML(Argument)
                                    if cont:
                                        yield ret
                                        continue

                                    GDFA = lambda name: GetValue(name, Argument=Argument)
                                    yield "<FitArgument name='%s' units='%s'>" % (GDFA("CollisionFitDataArgumentName"), GDFA("CollisionFitDataArgumentUnits"))
                                    desc = GDFA("CollisionFitDataArgumentDescription")
                                    if desc:
                                        yield "<Description>%s</Description>" % desc
                                    lowlim = GDFA("CollisionFitDataArgumentLowerLimit")
                                    if lowlim:
                                        yield "<LowerLimit>%s</LowerLimit>" % lowlim
                                    hilim = GDFA("CollisionFitDataArgumentUpperLimit")
                                    if hilim:
                                        yield "<UpperLimit>%s</UpperLimit>" % hilim
                                    yield "</FitArgument>"
                            if hasattr(FitData, "Parameters"):
                                for Parameter in FitData.Parameters:

                                    cont, ret = checkXML(Parameter)
                                    if cont:
                                        yield ret
                                        continue

                                    GDFP = lambda name: GetValue(name, Parameter=Parameter)
                                    yield makeNamedDataType("FitParameter", "CollisionFitDataParameter", GDFP)
                                yield "</FitParameters>"

                                accur = GDF("CollisionFitDataAccuracy")
                                if accur:
                                    yield "<FitAccuracy>%s</FitAccuracy>" % accur
                                physun = GDF("CollisionFitDataPhysicalUncertainty")
                                if physun:
                                    yield "<PhysicalUncertainty>%s</PhysicalUncertainty>" % physun
                                pdate = GDF("CollisionFitDataProductionDate")
                                if pdate:
                                    yield "<ProductionDate>%s</ProductionDate>" % pdate
                                yield "</FitData>"

                # Tabulated data
                if hasattr(DataSet, "TabData"):
                    for TabData in DataSet.TabData:
                        cont, ret = checkXML(TabData)
                        if cont:
                            yield ret
                            continue

                        GDT = lambda name: GetValue(name, TabData=TabData)

                        yield makePrimaryType("TabulatedData", "CollisionTabulatedData", GDT)

                        yield "<Description>%s</Description>" % GDT("CollisionTabulatedDataDescription")

                        # handle X components
                        yield makePrimaryType("X", "CollisionTabulatedDataX", GDT, extraAttr={"parameter": GDT("CollisionTabulatedDataXParameter"),
                                                                                              "units": GDT("CollisionTabulatedDataXUnits")})
                        yield "<Description>%s</Description>" % GDT("CollisionTabulatedDataXDescription")

                        if GDT("CollisionTabulatedDataXDataList"):
                            yield "<DataList count='%s'>%s</DataList>" % (GDT("CollisionTabulatedDataXDataListN"), " ".join(makeiter(GDT("CollisionTabulatedDataXDataList"))))
                        elif GDT("CollisionTabulatedDataXLinearSequence"):
                            yield "<LinearSequence count='%s' initial='%s' increment='%s'/>" % (GDT("CollisionTabulatedDataXLinearSequenceN"),
                                                                                                GDT("CollisionTabulatedDataXLinearSequenceInitial"),
                                                                                                GDT("CollisionTabulatedDataXLinearSequenceIncrement"))
                        elif GDT("CollisionTabulatedDataXDataFile"):
                            yield "<DataFile>%s</DataFile>" % GDT("CollisionTabulatedDataXDataFile")
                        yield makeDataSeriesAccuracyType("CollisionTabulatedDataX", GDT)
                        yield "</X>"

                        # handle Y components
                        yield makePrimaryType("Y", "CollisionTabulatedDataY", GDT, extraAttr={"parameter": GDT("CollisionTabulatedDataYParameter"),
                                                                                              "units": GDT("CollisionTabulatedDataYUnits")})
                        yield "<Description>%s</Description>" % GDT("CollisionTabulatedDataYDescription")

                        if GDT("CollisionTabulatedDataYDataList"):
                            yield "<DataList count='%s'>%s</DataList>" % (GDT("CollisionTabulatedDataYDataListN"), " ".join(makeiter(GDT("CollisionTabulatedDataYDataList"))))
                        elif GDT("CollisionTabulatedDataYLinearSequence"):
                            yield "<LinearSequence count='%s' initial='%s' increment='%s'/>" % (GDT("CollisionTabulatedDataYLinearSequenceN"),
                                                                                                GDT("CollisionTabulatedDataYLinearSequenceInitial"),
                                                                                                GDT("CollisionTabulatedDataYLinearSequenceIncrement"))
                        elif GDT("CollisionTabulatedDataYDataFile"):
                            yield "<DataFile>%s</DataFile>" % GDT("CollisionTabulatedDataYDataFile")

                        yield makeDataSeriesAccuracyType("CollisionTabulatedDataY", GDT)
                        yield "</Y>"


                        tabref = GDT("CollisionTabulatedDataReferenceFrame")
                        if tabref:
                            yield "<ReferenceFrame>%s</ReferenceFrame>" % tabref
                        physun = GDT("CollisionTabulatedDataPhysicalUncertainty")
                        if physun:
                            yield "<PhysicalUncertainty>%s</PhysicalUncertainty>" % physun
                        pdate = GDT("CollisionTabulatedDataProductionDate")
                        if pdate:
                            yield "<ProductionDate>%s</ProductionDate>" % pdate

                        yield "</TabulatedData>"

                yield "</DataSet>"
            yield "</DataSets>"
        yield "</CollisionalTransition>"
    yield '</Collisions>'

def XsamsNonRadTrans(NonRadTrans):
    """
    non-radiative transitions
    """
    if not isiterable(NonRadTrans):
        return

    yield "<NonRadiative>"
    for NonRadTran in NonRadTrans:

        cont, ret = checkXML(NonRadTran)
        if cont:
            yield ret
            continue

        G = lambda name: GetValue(name, NonRadTran=NonRadTran)
        dic = {'id':"%s-%s" % (NODEID, G("NonRadTranID")) }
        group = G("NonRadTranGroup")
        if group:
            dic["groupLabel"] = "%s" % group
        proc = G("NonRadTranProcess")
        if proc:
            dic["process"] = "%s" % proc
        yield makePrimaryType("NonRadiativeTransition", "NonRadTran", G, extraAttr=dic)

        yield "<InitialStateRef>S%s-%s</InitialStateRef>" % (NODEID, G("NonRadTranInitialState"))
        fstate = G("NonRadTranFinalState")
        if fstate:
            yield "<FinalStateRef>S%s-%s</FinalStateRef>" % (NODEID, fstate)
        fspec = G("NonRadTranSpecies")
        if fspec:
            yield "<SpeciesRef>X%s-%s</SpeciesRef>" % (NODEID, fspec)
        yield makeDataType("Probability", "NonRadTranProbability", G)
        yield makeDataType("NonRadiativeWidth", "NonRadTranWidth", G)
        yield makeDataType("TransitionEnergy", "NonRadTranEnergy", G)
        typ = G("NonRadTranType")
        if typ:
            yield "<Type>%s</Type>" % typ

        yield "</NonRadiativeTransition>"

    yield "</NonRadiative>"

def XsamsFunctions(Functions):
    """
    Generator for the Functions tag
    """
    if not isiterable(Functions):
        return
    yield '<Functions>\n'
    for Function in Functions:

        cont, ret = checkXML(Function)
        if cont:
            yield ret
            continue

        G = lambda name: GetValue(name, Function=Function)
        yield makePrimaryType("Function", "Function", G, extraAttr={"functionID":"F%s-%s" % (NODEID, G("FunctionID"))})

        yield "<Name>%s</Name>" % G("FunctionName")
        yield '<Expression computerLanguage="%s">%s</Expression>\n' % (G("FunctionComputerLanguage"), G("FunctionExpression"))
        yield '<Y name="%s" units="%s">' % (G("FunctionYName"), G("FunctionYUnits"))
        desc = G("FunctionYDescription")
        if desc:
            yield "<Description>%s</Description>" % desc
        lowlim = G("FunctionYLowerLimit")
        if lowlim:
            yield "<LowerLimit>%s</LowerLimit>" % lowlim
        hilim = G("FunctionYUpperLimit")
        if hilim:
            yield "<UpperLimit>%s</UpperLimit>" % hilim
        yield "</Y>"

        yield "<Arguments>\n"
        for FunctionArgument in Function.Arguments:

            cont, ret = checkXML(FunctionArgument)
            if cont:
                yield ret
                continue

            GA = lambda name: GetValue(name, FunctionArgument=FunctionArgument)
            yield makeArgumentType("Argument", "FunctionArgument", GA)
        yield "</Arguments>"

        if hasattr(Function, "Parameters"):
            yield "<Parameters>"
            for FunctionParameter in makeiter(Function.Parameters):

                cont, ret = checkXML(FunctionParameter)
                if cont:
                    yield ret
                    continue

                GP = lambda name: GetValue(name, FunctionParameter=FunctionParameter)
                yield makeParameterType("Parameter", "FunctionParameter", GP)
            yield "</Parameters>"
        reframe = G("FunctionReferenceFrame")
        if reframe:
            yield "<ReferenceFrame>%s</ReferenceFrame>" % reframe
        descr = G("FunctionDescription")
        if descr:
            yield "<Description>%s</Description>" % descr
        scurl = G("FunctionSourceCodeURL")
        if scurl:
            yield "<SourceCodeURL>%s</SourceCodeURL>" % scurl
        yield '</Function>'

    yield '</Functions>'

def XsamsMethods(Methods):
    """
    Generator for the methods block of XSAMS
    """
    if not Methods:
        return
    yield '<Methods>\n'
    for Method in Methods:

        cont, ret = checkXML(Method)
        if cont:
            yield ret
            continue

        G = lambda name: GetValue(name, Method=Method)
        yield """<Method methodID="M%s-%s">\n""" % (NODEID, G('MethodID'))

        yield makeSourceRefs( G('MethodSourceRef') )
        yield """<Category>%s</Category>\n<Description>%s</Description>\n"""\
             % (G('MethodCategory'), G('MethodDescription'))
        yield '</Method>\n'
    yield '</Methods>\n'

def generatorError(where):
    log.warn('Generator error in%s!' % where, exc_info=sys.exc_info())
    return where

def XsamsHeader(HeaderInfo):
    head = ['<?xml version="1.0" encoding="UTF-8"?>\n']
    head.append('<XSAMSData xmlns="http://vamdc.org/xml/xsams/%s"' % XSAMS_VERSION )
    head.append(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
    head.append(' xmlns:cml="http://www.xml-cml.org/schema"')
    head.append(' xsi:schemaLocation="http://vamdc.org/xml/xsams/%s %s">'\
            % (XSAMS_VERSION, SCHEMA_LOCATION) )

    if HeaderInfo:
        HeaderInfo = CaselessDict(HeaderInfo)
        if HeaderInfo.has_key('Truncated'):
            if HeaderInfo['Truncated'] != None: # note: allow 0 percent
                head.append( """
<!--
   ATTENTION: The amount of data returned may have been truncated by the node.
   The data below represent %s percent of all available data at this node that
   matched the query.
-->
""" % HeaderInfo['Truncated'] )

    return ''.join(head)

def Xsams(tap, HeaderInfo=None, Sources=None, Methods=None, Functions=None,
          Environments=None, Atoms=None, Molecules=None, Solids=None, Particles=None,
          CollTrans=None, RadTrans=None, RadCross=None, NonRadTrans=None):
    """
    The main generator function of XSAMS. This one calls all the
    sub-generators above. It takes the query sets that the node's
    setupResult() has constructed as arguments with given names.
    This function is to be passed to the HTTP-response object directly
    and not to be looped over beforehand.
    """

    yield XsamsHeader(HeaderInfo)

    errs=''

    requestables = tap.requestables
    if requestables and Atoms and ('atomstates' not in requestables):
        for Atom in Atoms:
            Atom.States = []
    if requestables and Molecules and ('moleculestates' not in requestables):
        for Molecule in Molecules:
            Molecule.States = []
            Molecule.NormalModes = []

    if not requestables or 'sources' in requestables:
        log.debug('Working on Sources.')
        try:
            for Source in XsamsSources(Sources, tap):
                yield Source
        except: errs+=generatorError(' Sources')

    if not requestables or 'methods' in requestables:
        log.debug('Working on Methods.')
        try:
            for Method in XsamsMethods(Methods):
                yield Method
        except: errs+=generatorError(' Methods')

    if not requestables or 'functions' in requestables:
        log.debug('Working on Functions.')
        try:
            for Function in XsamsFunctions(Functions):
                yield Function
        except: errs+=generatorError(' Functions')

    if not requestables or 'environments' in requestables:
        log.debug('Working on Environments.')
        try:
            for Environment in XsamsEnvironments(Environments):
                yield Environment
        except: errs+=generatorError(' Environments')

    yield '<Species>\n'
    if not requestables or 'atoms' in requestables:
        log.debug('Working on Atoms.')
        try:
            for Atom in XsamsAtoms(Atoms):
                yield Atom
        except: errs+=generatorError(' Atoms')

    if not requestables or 'molecules' in requestables:
        log.debug('Working on Molecules.')
        try:
            for Molecule in XsamsMolecules(Molecules):
                yield Molecule
        except: errs+=generatorError(' Molecules')

    if not requestables or 'solids' in requestables:
        log.debug('Working on Solids.')
        try:
            for Solid in XsamsSolids(Solids):
                yield Solid
        except: errs += generatorError(' Solids')

    if not requestables or 'particles' in requestables:
        log.debug('Working on Particles.')
        try:
            for Particle in XsamsParticles(Particles):
                yield Particle
        except: errs += generatorError(' Particles')

    yield '</Species>\n'

    log.debug('Working on Processes.')
    yield '<Processes>\n'
    yield '<Radiative>\n'

    if not requestables or 'radiativecrosssections' in requestables:
        try:
            for RadCros in XsamsRadCross(RadCross):
                yield RadCros
        except: errs+=generatorError(' RadCross')

    if not requestables or 'radiativetransitions' in requestables:
        try:
            for RadTran in XsamsRadTrans(RadTrans):
                yield RadTran
        except:
            errs+=generatorError(' RadTran')

    yield '</Radiative>\n'

    if not requestables or 'collisions' in requestables:
        try:
            for CollTran in XsamsCollTrans(CollTrans):
                yield CollTran
        except: errs+=generatorError(' CollTran')

    if not requestables or 'nonradiativetransitions' in requestables:
        try:
            for NonRadTran in XsamsNonRadTrans(NonRadTrans):
                yield NonRadTran
        except: errs+=generatorError(' NonRadTran')

    yield '</Processes>\n'

    if errs: yield """<!--
           ATTENTION: There was an error in making the XML output and at least one item in the following parts was skipped: %s
-->
                 """ % errs

    yield '</XSAMSData>\n'
    log.debug('Done with XSAMS')


