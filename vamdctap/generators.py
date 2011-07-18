# -*- coding: utf-8 -*-

import re
import sys
from xml.sax.saxutils import quoteattr

# Get the node-specific parts
from django.conf import settings
from django.utils.importlib import import_module
DICTS = import_module(settings.NODEPKG + '.dictionaries')
from caselessdict import CaselessDict
RETURNABLES = CaselessDict(DICTS.RETURNABLES)

# This must always be set.
try:
    NODEID = RETURNABLES['NodeID']
except:
    NODEID = 'PleaseFillTheNodeID'

import logging
log = logging.getLogger('vamdc.tap.generator')

# Helper function to test if an object is a list or tuple
isiterable = lambda obj: hasattr(obj, '__iter__')
escape = lambda s: quoteattr(s)[1:-1]

def countReturnables(regexp):
    """
    count how often a certain matches the keys of the returnables
    """
    r = re.compile(regexp, flags=re.IGNORECASE)
    return len(filter(r.match, RETURNABLES.keys()))

# Define some globals that allow skipping parts
# of the generator below.
N_ENV_KWS = countReturnables('^Environment.*')
N_METHOD_KWS = countReturnables('^Method.*')
N_FUNCTION_KWS = countReturnables('^Function.*')
N_MOLESTATE_KWS = countReturnables('^MoleculeState.*')
N_MOLE_KWS = countReturnables('^Molecule.*') - N_MOLESTATE_KWS
N_ATOMSTATE_KWS = countReturnables('^AtomState.*')
N_ATOM_KWS = countReturnables('^Atom.*') - N_ATOMSTATE_KWS
N_COLLTRAN_KWS = countReturnables('Collision.*')
N_RADTRAN_KWS = countReturnables('^RadTran.*')
N_BROAD_KWS = countReturnables('^.*Broadening.*')

def makeiter(obj):
    """
    Return an iterable, no matter what
    """
    if not obj:
        return []
    if not isiterable(obj):
        return [obj]
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

def GetValue(name, **kwargs):
    """
    the function that gets a value out of the query set, using the global name
    and the node-specific dictionary.
    """
    try:
        name = RETURNABLES[name]
    except Exception:
        # The value is not in the dictionary for the node.  This is
        # fine.  Note that this is also used by if-clauses below since
        # the empty string evaluates as False.
        return ''

    if not name:
        # the key was in the dict, but the value was empty or None.
        return ''

    for key in kwargs:
        # assign the dict-value to a local variable named as the dict-key
        exec('%s=kwargs["%s"]' % (key, key))

    try:
        # here, the RHS of the RETURNABLES dict is executed.
        value = eval(name) # this works, if the dict-value is named
                           # correctly as the query-set attribute
    except Exception:
         # this catches the case where the dict-value is a string or mistyped.
#        log.debug('Exception in generators.py: GetValue()')
#        log.debug(str(e))
#        log.debug(name)
        value = name
    if value == None:
        # the database returned NULL
        return ''
    elif value == 0:
        if isinstance(value, float): return '0.0'
        else: return '0'

    # turn it into a string, quote it, but skip the quotation marks
    # edit - no, we need to have the object itself sometimes to loop over
    #return quoteattr('%s'%value)[1:-1] # re
    return value

def makeSourceRefs(refs):
    """
    Create a SourceRef tag entry
    """
    s = ''
    if refs:
        if isiterable(refs):
            for ref in refs:
                s += '<SourceRef>B%s-%s</SourceRef>' % (NODEID, ref)
        else: s += '<SourceRef>B%s-%s</SourceRef>' % (NODEID, refs)
    return s

def makePartitionfunc(keyword, G):
    """
    Create the Partionfunction tag element.
    """
    value = G(keyword)
    if not value: 
        return ''
    
    temperature = G(keyword + 'T')
    partitionfunc = G(keyword)
    
    string = '<PartitionFunction>\n'
    string += '  <T units="K">\n'
    string += '     <DataList>\n'
    for temp in temperature: 
        string += ' %s' % temp   
    string += '\n     </DataList>\n'
    string += '  </T>\n'
    string += '  <Q>\n'
    string += '     <DataList>\n'
    for q in partitionfunc: 
        string += ' %s' % q
    string += '\n     </DataList>\n'
    string += '  </Q>\n'
    string += '</PartitionFunction>\n'

    return string

def makePrimaryType(tagname, keyword, G, extraAttr=None):
    """
    Build the Primary-type base tags. Note that this method does NOT
    close the tag, </tagname> must be added manually by the calling function.    

    extraAttr is a dictionary of attributes-value pairs to add to the tag.
    """
    method = G("%sMethod" % keyword)
    comment = G("%sComment" % keyword)
    refs = G(keyword + 'Ref') # Sources

    string = "\n<%s" % tagname
    if method: 
        string += ' methodRef="M%s-%s"' % (NODEID, method)
    if extraAttr:
        for k, v in extraAttr.items():
            string += ' %s="%s"'% (k, G(v))
    string += '>'
    if comment:
        string += '<Comments>%s</Comments>' % quoteattr('%s' % comment)[1:-1]    
    string += makeSourceRefs(refs)    

    return string 

def makeDataType(tagname, keyword, G, extraAttr=None, extraElem=None):
    """
    This is for treating the case where a keyword corresponds to a
    DataType in the schema which can have units, comment, sources etc.
    The dictionary-suffixes are appended and the values retrieved. If the
    sources is iterable, it is looped over.

    #This extends the PrimaryType with some often-seen arguments. 

    """

    #string = makePrimaryType(tagname, keyword, G, extraAttr=extraAttr)

    # value = G(keyword)
    # if not value: 
    #     return ''

    # unit = G(keyword + 'Unit')    
    # acc = G(keyword + 'Accuracy')

    # string += '<Value units="%s">%s</Value>' % (unit or 'unitless', value)
    # if acc: 
    #     string += '<Accuracy>%s</Accuracy>' % acc
    # string += '</%s>' % tagname

    # if extraElem:
    #     for k, v in extraElem. items():
    #         string += '<%s>%s</%s>' % (k, G(v), k)

    value = G(keyword)
    if not value: 
        return ''
    
    unit = G(keyword + 'Unit')
    method = G(keyword + 'Method')
    comment = G(keyword + 'Comment')
    acc = G(keyword + 'Accuracy')
    refs = G(keyword + 'Ref')

    string = '\n<%s' % tagname
    if method: 
        string += ' methodRef="M%s-%s"' % (NODEID, method)
    if extraAttr:
        for k, v in extraAttr.items():
            string += ' %s="%s"'% (k, G(v))
    string += '>'

    if comment: 
        string += '<Comments>%s</Comments>' % quoteattr('%s' % comment)[1:-1]
    string += makeSourceRefs(refs)
    string += '<Value units="%s">%s</Value>' % (unit or 'unitless', value)
    if acc: 
        #string += '<Accuracy>%s</Accuracy>' % acc
        string += '<Accuracy><Statistical>%s</Statistical></Accuracy>' % acc
    string += '</%s>' % tagname

    if extraElem:
        for k, v in extraElem. items():
            string += '<%s>%s</%s>' % (k, G(v), k)

    return string

def makeArgumentType(tagname, keyword, G):
    """
    Build ArgumentType

    """
    string = "<%s name='%s' units='%s'>" % (tagname, G("%sName" % keyword), G("%sUnits" % keyword))
    string += "<Description>%s</Description>" % G("%sDescription" % keyword)
    string += "<LowerLimit>%s</LowerLimit>" % G("%sLowerLimit" % keyword)
    string += "<UpperLimit>%s</UpperLimit>" % G("%sUpperLimit" % keyword)
    string += "</%s>" % tagname    
    return string 

def makeDataFuncType(tagname, keyword, Parameter, G):
    """
    Build the DataFuncType.
    """

def makeNamedDataType(tagname, keyword, G):
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

    string = ''
    for i, val in enumerate(value):
        string += '\n<%s' % tagname
        if name[i]: 
            string += ' name="%s"' % name[i]
        if method[i]: 
            string += ' methodRef="M%s-%s"' % (NODEID, method[i])
        string += '>'
        if comment[i]: 
            string += '<Comments>%s</Comments>' % escape('%s' % comment[i])
        string += makeSourceRefs(refs[i])
        string += '<Value units="%s">%s</Value>' % (unit[i] or 'unitless', value[i])
        if acc[i]: 
            string += '<Accuracy>%s</Accuracy>' % acc[i]
        string += '</%s>' % tagname

    return string

def checkXML(obj,methodName='XML'):
    """
    If the queryset has an XML method, use that and
    skip the hard-coded implementation.
    """
    if hasattr(obj,methodName):
        try:
            return True, eval('obj.%s()' % methodName) 
        except Exception:
            pass
    return False, None 

def XsamsSources(Sources):
    """
    Create the Source tag structure (a bibtex entry)
    """

    if not Sources: 
        return
    yield '<Sources>'
    for Source in Sources:
        cont, ret = checkXML(Source)
        if cont:
            yield ret
            continue 
        G = lambda name: GetValue(name, Source=Source)
        yield '<Source sourceID="B%s-%s"><Authors>\n' % (NODEID, G('SourceID'))
        authornames = G('SourceAuthorName')
        # make it always into a list to be looped over, even if
        # only a single entry
        try:
            authornames = eval(authornames)
        except:
            pass
        if not isiterable(authornames): 
            authornames = [authornames]
        for author in authornames:
            yield '<Author><Name>%s</Name></Author>\n' % author

        yield """</Authors>
<Title>%s</Title>
<Category>%s</Category>
<Year>%s</Year>
<SourceName>%s</SourceName>
<Volume>%s</Volume>
<PageBegin>%s</PageBegin>
<PageEnd>%s</PageEnd>
<UniformResourceIdentifier>%s</UniformResourceIdentifier>
</Source>\n""" % ( G('SourceTitle'), G('SourceCategory'),
                   G('SourceYear'), G('SourceName'), G('SourceVolume'),
                   G('SourcePageBegin'), G('SourcePageEnd'), G('SourceURI') )
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
                yield '<Species name="%s" speciesRef="X%s-%s">' % (G('EnvironmentSpeciesName'), NODEID, GS('EnvironmentSpeciesRef'))
                yield makeDataType('PartialPressure', 'EnvironmentSpeciesPartialPressure', GS)
                yield makeDataType('MoleFraction', 'EnvironmentSpeciesMoleFraction', GS)
                yield makeDataType('Concentration', 'EnvironmentSpeciesConcentration', GS)
                yield '</Species>'
            yield '</Composition>'
        yield '</Environment>'
    yield '</Environments>\n'

def parityLabel(parity):
    """
    XSAMS whats this as strings "odd" or "even", not numerical

    """
    try: 
        parity = float(parity)
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
    s = G("%sS" % keyword)
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
        string += "<j1j2>"
        for j in j1j2:
            string += "<j>%s</j>" % j
        string += "</j1j2>"
    K = G("%sK" % keyword)
    if K:
        string += "<jK>"
        j = G("%sJKJ" % keyword)
        if j:
            string += "<j>%s</j>" % j
        S2 = G("sJKS" % keyword)
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
        string += " shellid=%s-%s" % (NODEID, sid)
    string += ">"
    string += "<PrincipalQuantumNumber>%s</PrincipalQuantumNumber>" % G("%sPrincipalQN" % keyword)

    string += "<OrbitalAngularMomentum>"
    string += "<Value>%s</Value>" % G("%sOrbitalAngMom" % keyword)
    symb = G("%sOrbitalAngMomSymbol" % keyword)
    if symb:
        string += "<Symbol>%s</Symbol>" % symb
    string += "</OrbitalAngularMomentum>"
    string += "<NumberOfElectrons>%s</NumberOfElectrons>" % G("%sNumberOfElectrons" % keyword)
    string += "<Parity>%s</Parity>" % G("%sParity" % keyword)
    string += "<Kappa>%s</Kappa>" % G("%sKappa" % keyword)
    string += "<TotalAngularMomentum>%s</TotalAngularMomentum>" % G("%sTotalAngularMomentum" % keyword)
    string += makeTermType("ShellTerm", "%sTerm" % keyword, G)
    string += "</%s>" % keyword
    return string


def makeAtomComponent(Atom, G):
    """
    This constructs the Atomic Component structure.
    
    Atom - the current Atom queryset
    G - the shortcut to the GetValue function
    """

    string = "<Component>"

    if hasattr(Atom, "SuperShells"):
        for SuperShell in makeiter(Atom.SuperShells):
            GA = lambda name: GetValue(name, SuperShell=SuperShell)
            string += "<SuperShell>"
            string += "<PrincipalQuantumNumber>%s</PrincipalQuantumNumber>" % GA("AtomStateSuperShellPrincipalQN")
            string += "<NumberOfElectrons>%s</NumberOfElectrons>" % GA("AtomStateSuperShellNumberOfElectrons")
            string += "</SuperShell>"

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

    if hasattr(Atom, "Shells"):
        for AtomShell in makeiter(Atom.Shells):
            GS = lambda name: GetValue(name, AtomShell=AtomShell)    
            string += makeShellType("Shell", "AtomStateShell", GS)

    if hasattr(Atom, "ShellPair"):
        for AtomShellPair in makeiter(Atom.ShellPairs):
            GS = lambda name: GetValue(name, AtomShellPair=AtomShellPair)
            string += "<ShellPair shellPairID=%s-%s>" % (NODEID, GS("AtomStateShellPairID"))
            string += makeShellType("Shell1", "AtomStateShellPairShell1", GS)
            string += makeShellType("Shell2", "AtomStateShellPairShell2", GS)
            string += makeTermType("ShellPairTerm", "AtomStateShellPairTerm", GS)
            string += "</ShellPair>"
    clabel = G("AtomStateConfigurationLabel") 
    if clabel:
        string += "<ConfigurationLabel>%s</ConfigurationLabel>" % clabel
    string += "</Configuration>"

    string += makeTermType("Term", "AtomStateTerm", G)
    mixCoe = G("AtomStateMixingCoeff")
    if mixCoe:
        string += '<MixingCoefficient mixingclass="%s">%s</MixingCoefficient>' % (G("AtomStateMixingCoeffClass"), mixCoe)
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

    if not isiterable(Atoms): 
        return
    if not Atoms.count(): 
        return

    yield '<Atoms>'

    for Atom in Atoms:
        cont, ret = checkXML(Atom)
        if cont:
            yield ret
            continue 

        G = lambda name: GetValue(name, Atom=Atom)
        yield """<Atom>
<ChemicalElement>
<NuclearCharge>%s</NuclearCharge>
<ElementSymbol>%s</ElementSymbol>
</ChemicalElement>""" % (G('AtomNuclearCharge'), G('AtomSymbol'))

        yield """<Isotope>
<IsotopeParameters>
<MassNumber>%s</MassNumber>%s""" % (G('AtomMassNumber'), makeDataType('Mass', 'AtomMass', G))
        nucspin = G('AtomNuclearSpin')
        if nucspin: 
            yield '<NuclearSpin>%s</NuclearSpin>' % nucspin
        yield '</IsotopeParameters>'

        yield '<Ion speciesID="X%s-%s"><IonCharge>%s</IonCharge>' % (NODEID, G('AtomSpeciesID'), G('AtomIonCharge'))
        if not hasattr(Atom,'States'): 
            Atom.States = []
        for AtomState in Atom.States:
            cont, ret = checkXML(AtomState)
            if cont:
                yield ret
                continue 
            G = lambda name: GetValue(name, AtomState=AtomState)
            yield """<AtomicState stateID="S%s-%s">""" % (G('NodeID'), G('AtomStateID'))
            comm = G('AtomStateDescription')
            if comm: 
                yield '<Comments>%s</Comments>' % comm
            yield makeSourceRefs(G('AtomStateRef'))
            desc = G('AtomStateDescription')
            if desc: 
                yield '<Description>%s</Description>' % desc

            yield '<AtomicNumericalData>'
            yield makeDataType('StateEnergy', 'AtomStateEnergy', G)
            yield makeDataType('IonizationEnergy', 'AtomStateIonizationEnergy', G)
            yield makeDataType('LandeFactor', 'AtomStateLandeFactor', G)
            yield makeDataType('QuantumDefect', 'AtomStateQuantumDefect', G)
            yield makeDataType('TotalLifeTime', 'AtomStateLifeTime', G)
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
                yield makePrimaryType("AtomicComposition", "AtomicStateComposition", G)
                yield makeAtomComponent(Atom, G)
                yield '</AtomicComposition>'

            yield '</AtomicState>'
        G = lambda name: GetValue(name, Atom=Atom) # reset G() to Atoms, not AtomStates
        yield '<InChI>%s</InChI>' % G('AtomInchi')
        yield '<InChIKey>%s</InChIKey>' % G('AtomInchiKey')
        yield """</Ion>
</Isotope>
</Atom>"""
    yield '</Atoms>'

# ATOMS END
#
# MOLECULES START

def XsamsMCSBuild(Molecule):
    """
    Generator for the MolecularChemicalSpecies
    """
    G = lambda name: GetValue(name, Molecule=Molecule)
    yield '<MolecularChemicalSpecies>\n'
    yield '<OrdinaryStructuralFormula><Value>%s</Value>'\
            '</OrdinaryStructuralFormula>\n'\
            % G("MoleculeOrdinaryStructuralFormula")

    yield '<StoichiometricFormula>%s</StoichiometricFormula>\n'\
            % G("MoleculeStoichiometricFormula")
    if G("MoleculeChemicalName"):
        yield '<ChemicalName><Value>%s</Value></ChemicalName>\n'\
            % G("MoleculeChemicalName")
    if G("MoleculeInChI"):
        yield '<InChI>%s</InChI>' % G("MoleculeInChI")
    yield '<InChIKey>%s</InChIKey>\n' % G("MoleculeInChIKey")

    yield makePartitionfunc("MoleculePartitionFunction", G)

    yield '<StableMolecularProperties>\n%s</StableMolecularProperties>\n' % makeDataType('MolecularWeight', 'MoleculeMolecularWeight', G)
    if G("MoleculeComment"):
        yield '<Comment>%s</Comment>\n' % G("MoleculeComment")
    yield '</MolecularChemicalSpecies>\n'

def makeCaseQNs(G):
    """
    return the Case and the QNs
    """
    case = G('MoleculeQnCase')
    if not case: return ''

    ElecStateLabel = G("MoleculeQNElecStateLabel")
    elecInv = G("MoleculeQNelecInv")
    elecRefl = G("MoleculeQNelecRefl")
    vi = G("MoleculeQNvi")
    viMode = G("MoleculeQNviMode")
    vibInv = G("MoleculeQNvibInv")
    vibSym = G("MoleculeQNvibSym")
    vibSymGroup = G("MoleculeQNvibSymGroup")
    J = G("MoleculeQNJ")
    Ka = G("MoleculeQNKa")
    Kc = G("MoleculeQNKc")
    rotSym = G("MoleculeQNrotSym")
    rotSymGroup = G("MoleculeQNrotSymGroup")
    I = G("MoleculeQNI")
    InuclSpin = G("MoleculeQNInuclSpin")
    Fj = G("MoleculeQNFj")
    Fjj = G("MoleculeQNFjj")
    FjnuclSpin = G("MoleculeQNFjnuclSpin")
    F = G("MoleculeQNF")
    FnuclSpin = G("MoleculeQNFnuclSpin")
    r = G("MoleculeQNr")
    rName = G("MoleculeQNrName")
    parity = G("MoleculeQNparity")
    S = G("MoleculeQNS")
    N = G("MoleculeQNN")
    v = G("MoleculeQNv")
    F1 = G("MoleculeQNF1")
    F1nuclSpin = G("MoleculeQNF1nuclSpin")
    asSym = G("MoleculeQNasSym")
    Lambda = G("MoleculeQNLambda")
    Sigma = G("MoleculeQNSigma")
    Omega = G("MoleculeQNOmega")
    kronigParity = G("MoleculeQNkronigParity")
    SpinComponentLabel = G("MoleculeQNSpinComponentLabel")
    li = G("MoleculeQNli")
    liMode = G("MoleculeQNliMode")
    l = G("MoleculeQNl")
    vibRefl = G("MoleculeQNvibRefl")
    v1 = G("MoleculeQNv1")
    v2 = G("MoleculeQNv2")
    v3 = G("MoleculeQNv3")
    l2 = G("MoleculeQNl2")
    F2 = G("MoleculeQNF2")
    F2nuclSpin = G("MoleculeQNF2nuclSpin")
    K = G("MoleculeQNK")

    result = '<Case xsi:type="case:Case" caseID="%s" xmlns:case="http://vamdc.org/xml/xsams/0.2/cases/%s">'
    result += '<case:QNs>'
    if ElecStateLabel: result += '<case:ElecStateLabel>%s</case:ElecStateLabel>'%ElecStateLabel
    if elecInv: result += '<case:elecInv>%s</case:elecInv>'%elecInv
    if elecRefl: result += '<case:elecRefl>%s</case:elecRefl>'%elecRefl
    if Lambda: result += '<case:Lambda>%s</case:Lambda>'%Lambda
    if Sigma: result += '<case:Sigma>%s</case:Sigma>'%Sigma
    if Omega: result += '<case:Omega>%s</case:Omega>'%Omega
    if S: result += '<case:S>%s</case:S>'%S
    if v: result += '<case:v>%s</case:v>'%v
    if v1: result += '<case:v1>%s</case:v1>'%v1
    if v2: result += '<case:v2>%s</case:v2>'%v2
    if l2: result += '<case:l2>%s</case:l2>'%l2
    if v3: result += '<case:v3>%s</case:v3>'%v3
    if vi:
        for val,i in enumerate(makeiter(vi)):
            result += '<case:vi mode="%s">%s</case:vi>'%(makeiter(viMode)[i],val)
    if li:
        for val,i in enumerate(makeiter(li)):
            result += '<case:vi mode="%s">%s</case:vi>'%(makeiter(liMode)[i],val)
    if l: result += '<case:l>%s</case:l>'%l
    if vibInv: result += '<case:vibInv>%s</case:vibInv>'%vibInv
    if vibRefl: result += '<case:vibRefl>%s</case:vibRefl>'%vibRefl
    if vibSym:
        if vibSymGroup: result += '<case:vibSym group="%s">%s</case:vibSym>'%(vibSymGroup,vibSym)
        else: result += '<case:vibSym>%s</case:vibSym>'%vibSym
    if J: result += '<case:J>%s</case:J>'%J
    if K: result += '<case:K>%s</case:K>'%K
    if Ka: result += '<case:Ka>%s</case:Ka>'%Ka
    if Kc: result += '<case:Kc>%s</case:Kc>'%Kc
    if rotSym:
        if rotSymGroup:  result += '<case:rotSym group="%s">%s</case:rotSym>'%(rotSymGroup,rotSym)
        else: result += '<case:rotSym>%s</case:rotSym>'%rotSym
    if I: result += '<case:I nuclearSpinRef="%s">%s</case:I>'%(InuclSpin,I)
    if Fj:
        for val,i in enumerate(makeiter(Fj)):
            result += '<case:Fj j="%s" nuclearSpinRef="%s">%s</case:Fj>'%(makeiter(Fjj)[i],makeiter(FjnuclSpin)[i],val)
    if N: result += '<case:N>%s</case:N>'%N
    if SpinComponentLabel: result += '<case:SpinComponentLabel>%s</case:SpinComponentLabel>'%SpinComponentLabel
    if F1: result += '<case:F1 nuclearSpinRef="%s">%s</case:F1>'%(F1nuclSpin,F1)
    if F2: result += '<case:F2 nuclearSpinRef="%s">%s</case:F2>'%(F2nuclSpin,F2)
    if F: result += '<case:F nuclearSpinRef="%s">%s</case:F>'%(FnuclSpin,F)
    if r:
        for val,i in enumerate(makeiter(r)):
            result += '<case:r name="%s">%s</case:r>'%(makeiter(rName)[i],val)
    if parity: result += '<case:parity>%s</case:parity>'%parity
    if kronigParity: result += '<case:kronigParity>%s</case:kronigParity>'%kronigParity
    if asSym: result += '<case:asSym>%s</case:asSym>'%asSym

    result += '</case:QNs>'
    return result+'</Case>'

def XsamsMSBuild(MoleculeState):
    """
    Generator for MolecularState tag
    """
    G = lambda name: GetValue(name, MoleculeState=MoleculeState)
    yield '<MolecularState stateID="S%s-%s">\n' % (G('NodeID'),
                                                   G("MoleculeStateID"))
    yield '  <Description/>\n'
    yield '  <MolecularStateCharacterisation>\n'
    yield makeDataType('StateEnergy', 'MoleculeStateEnergy', G,
                extraAttr={'energyOrigin':'MoleculeStateEnergyOrigin'})
    if G("MoleculeStateCharacTotalStatisticalWeight"):
        yield '  <TotalStatisticalWeight>%s</TotalStatisticalWeight>\n'\
                    % G("MoleculeStateCharacTotalStatisticalWeight")
    if G("MoleculeStateCharacNuclearStatisticalWeight"):
        yield '  <NuclearStatisticalWeight>%s</NuclearStatisticalWeight>\n'\
                    % G("MoleculeStateCharacNuclearStatisticalWeight")
    if G("MoleculeStateCharacNuclearSpinIsomer"):
        yield '  <NuclearSpinIsomer>%s</NuclearSpinIsomer>\n'\
                    % G("MoleculeStateCharacNuclearSpinIsomer")
    yield '  </MolecularStateCharacterisation>\n'




    cont, ret = checkXML(G("MoleculeStateQuantumNumbers"))
    if cont:
        yield ret
    else:
        yield makeCaseQNs(G)
    yield '</MolecularState>\n'

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
        yield '<Molecule speciesID="X%s-%s">\n' % (NODEID,G("MoleculeSpeciesID"))

        # write the MolecularChemicalSpecies description:
        for MCS in XsamsMCSBuild(Molecule):
            yield MCS

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
        makePrimaryType("Solid", "Solid", G, extraAttr={"stateID":"S%s-%s" % (NODEID, G("SolidStateID"))})
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
        makePrimaryType("Particle", "Particle", G, extraAttr={"stateID":G("ParticleStateID"), "name":G("ParticleName")})
        yield "<ParticleProperties>"
        yield "<ParticleCharge>%s</ParticleCharge>" % G("ParticleCharge")
        makeDataType("ParticleMass", "ParticleMass", G)
        yield "<ParticleSpin>%s</ParticleSpin>" % G("ParticleSpin")
        yield "<ParticlePolarization>%s</ParticlePolarization>" % G("ParticlePolarization")
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
    s = '<Broadening name="%s"' % name.lower()
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
    # per broadening type
    s += '<Lineshape name="%s">' % G('RadTransBroadening%sLineshapeName' % name)
    s += lsparams
    s += '</Lineshape>'
    s += '</Broadening>'
    return s

def XsamsRadTranBroadening(G):
    """
    helper function for line broadening, called from RadTrans

    allowed names are: pressure, instrument, doppler, natural
    """
    s=''
    if countReturnables('RadTransBroadeningNatural'):
        # attempt at making a loop to support multiple natural broadening effects
        if hasattr(G('RadTransBroadeningNatural'), "Broadenings"):
            for Broadening in  makeiter(G('RadTransBroadeningNatural').Broadenings):
                GB = lambda name: GetValue(name, Broadening=Broadening)
                s += makeBroadeningType(GB, name='Natural')  
        else:
            s += makeBroadeningType(G, name='Natural')
    if countReturnables('RadTransBroadeningInstrument'):
        s += makeBroadeningType(G, name='Instrument')
    if countReturnables('RadTransBroadeningDoppler'):
        s += makeBroadeningType(G, name='Doppler')
    if countReturnables('RadTransBroadeningPressure'):
        s += makeBroadeningType(G, name='Pressure')
    return s

def XsamsRadTranShifting(RadTran, G):
    """
    Shifting type
    """
    dic = {}
    nam = G("RadtransShiftingType")
    eref = G("RadtransShiftingEnv")
    if nam:
        dic["name"] = nam
    else:
        return ''
    if eref:
        dic["envRef"] = "E%s-%s"  % (NODEID, eref)
    string = makePrimaryType("Shifting", "RadtransShifting", G, extraAttr=dic)

    if hasattr(RadTran, "ShiftingParams"):
        for ShiftingParam in RadTran.ShiftingParams:
            GS = lambda name: GetValue(name, ShiftingParam=ShiftingParam)

            string = makePrimaryType("ShiftingParameter", "RadTransShiftingParam", GS, extraAttr={"name":GS("RadTransShiftingParamName")})

            val = GS("RadTransShiftingParamValueUnits")

            if val:
                string += "<Value units=%s>%s</Value>" % (GS("RadTransShiftingParamValueUnits"), GS("RadTransShiftingParamValue" ))
                string += makePrimaryType("Accuracy", "RadTransShiftingParamAcc" , GS, extraAttr={"calibration":GS("RadTransShiftingParamAccCalib" ), "quality":GS("RadTransShiftingParamAccQuality")})
                systerr = GS("RadTransShiftingParamAccSystematic")
                if systerr:
                    string += "<Systematic confidence=%s relative=%s>%s</Systematic>" % (GS("RadTransShiftingParamAccSystematicConfidence"), GS("RadTransShiftingParamAccSystematicRelative"), systerr)
                staterr = GS("RadTransShiftingParamAccStatistical")   
                if staterr:
                    string += "<Statistical confidence=%s relative=%s>%s</Statistical>" % (GS("RadTransShiftingParamAccStatisticalConfidence"), GS("RadTransShiftingParamAccStatisticalRelative"), staterr)
                stathigh = GS("RadTransShiftingParamAccStatHigh")
                statlow = GS("RadTransShiftingParamAccStatLow")
                if stathigh and statlow:
                    string += "<StatHigh confidence=%s relative=%s>%s</StatHigh>" % (GS("RadTransShiftingParamAccStatHighConfidence"), GS("RadTransShiftingParamAccStatHighRelative"), systerr)    
                    string += "<StatLow confidence=%s relative=%s>%s</StatLow>" % (GS("RadTransShiftingParamAccStatLowConfidence"), GS("RadTransShiftingParamAccStatLowRelative"), systerr)
                string += "</Accuracy>"
                string += "</Value>"

            if hasattr(ShiftingParam, "Fit"):        
                for Fit in makeiter(ShiftingParam.Fits):
                    GSF = lambda name: GetValue(name, Fit=Fit)
                    string += "<FitParameters functionRef=F%s-%s>" % (NODEID, GSF("RadTransShiftingParamFitFunction"))

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
        yield '<RadiativeTransition>'
        comm = G('RadTransComment')
        if comm: 
            yield '<Comments>%s</Comments>' % comm
        yield makeSourceRefs(G('RadTransRefs'))
        yield '<EnergyWavelength>'
        yield makeDataType('Wavelength', 'RadTransWavelength', G)
        yield makeDataType('Wavenumber', 'RadTransWavenumber', G)
        yield makeDataType('Frequency', 'RadTransFrequency', G)
        yield makeDataType('Energy', 'RadTransEnergy', G)
        yield '</EnergyWavelength>'

        initial = G('RadTransInitialStateRef')
        if initial: 
            yield '<InitialStateRef>S%s-%s</InitialStateRef>\n' % (NODEID, initial)
        final = G('RadTransFinalStateRef')
        if final: 
            yield '<FinalStateRef>S%s-%s</FinalStateRef>\n' % (NODEID, final)
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
        multipole = G('RadTransProbabilityMultipole')
        if multipole: 
            yield '<Multipole>%s</Multipole>' % multipole
        yield makeDataType('EffectiveLandeFactor', 'RadTransEffectiveLandeFactor', G)
        yield '</Probability>\n'

        if hasattr(RadTran, 'XML_Broadening'):
            yield RadTran.XML_Broadening()
        else:
            yield XsamsRadTranBroadening(G)
        if hasattr(RadTran, 'XML_Shifting'):
            yield RadTran.XML_Shifting()
        else:
            yield XsamsRadTranShifting(RadTran, G)
        yield '</RadiativeTransition>\n'

def makeDataSeriesType(tagname, keyword, G):
    """
    Creates the dataseries type
    """
    result=[]
    dic = {}
    xpara = G("%sParameter" % keyword)
    if xpara:
        dic["parameter"] = xpara
    xunits = G("%sUnits" % keyword)
    if xunits:
        dic["units"] = xunits
    xid = G("%sID" % keyword)
    if xid:
        dic["id"] = "%s-%s" % (NODEID, xid)
    result.append(makePrimaryType("%s" % tagname, "%s" % keyword, G, extraAttr=dic))

    dlist = makeiter(G("%s" % keyword))
    if dlist:
        result.append("<DataList n='%s' units='%s'>%s</DataList>" % (G("%sN" % keyword), G("%sUnits" % keyword), " ".join(dlist)))
    csec = G("%sLinearA0" % keyword) and G("%sLinearA1" % keyword)
    if csec:
        dic = {"a0":G("%sLinearA0" % keyword), "a1":G("%sLinearA1" % keyword)}
        nx = G("%sLinearN" % keyword)
        if nx:
            dic["n"] = nx
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
        result.append("<ErrorList n='%s' units='%s'>%s</ErrorList>" % (G("%sErrorListN" % keyword), G("%sErrorListUnits" % keyword), " ".join(elist)))
    err = G("%sError" % keyword)
    if err:
        result.append("<Error>%s</Error>" % err)

    result.append("</%s>" % tagname)
    return result


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

    yield "<CrossSection>"
    for RadCros in RadCross:
        cont, ret = checkXML(RadCros)
        if cont:
            yield ret
            continue

        # create header

        G = lambda name: GetValue(name, RadCros=RadCros)
        dic = {}
        envRef = G("CrossSectionEnvironment")
        if envRef:
            dic["envRef"] = "E%s-%s" % (NODEID, envRef)
        ID = G("CrossSectionID")
        if ID:
            dic["id": "%s-%s" % (NODEID, ID)]
        yield makePrimaryType("CrossSection", "CrossSection", G, extraAttr=dic)
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

        yield makePrimaryType("BandAssignment", "CrossSectionBand", G, extraAttr={"name":"CrossSectionBandName"})

        yield makeDataType("BandCentre", "CrossSectionBandCentre", G)
        yield makeDataType("BandWidth", "CrossSectionBandWidth", G)

        if hasattr(RadCros, "Modes"):
            for BandMode in RadCros.BandModes:

                cont, ret = checkXML(BandMode)
                if cont:
                    yield ret
                    continue 

                GM = lambda name: GetValue(name, BandMode=BandMode)
                yield makePrimaryType("Modes", "CrossSectionBandMode", GM, extraAttr={"name":"CrossSectionBandModeName"})

                for deltav, modeid in makeloop("CrossSectionBandMode", GM, "DeltaV", "DeltaVModeID"):              
                    if modeid:
                        yield "<DeltaV modeID=V%s-%s>%s</DeltaV>" % (deltav, NODEID, modeid)
                    else:
                        yield "<DeltaV>%s</DeltaV>" % deltav                    
                yield "</Modes>"
            yield "</BandAssignment>"
        yield "</CrossSection>"


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
        yield makePrimaryType("CollisionalTransition", "Collision", G)

        yield "<ProcessClass>"
        udef = G("CollisionUserDefinition")
        code = G("CollisionCode")
        iaea = G("CollisionIAEACode")
        if udef:
            yield "<UserDefinition>%s</UserDefinition>" % udef
        if code:
            yield "<Code>%s</Code>" % code
        if iaea:
            yield "<IAEACode>%s</IAEACode>" % iaea
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

        
        yield "<DataSets>"        
        if hasattr(CollTran, "DataSets"):
            for DataSet in CollTran.DataSets:

                cont, ret = checkXML(DataSet)
                if cont:
                    yield ret
                    continue 

                GD = lambda name: GetValue(name, DataSet=DataSet)

                yield makePrimaryType("DataSet", "CollisionDataSet", GD, extraArgs={"dataDescription":GD("CollisionDataSetDescription")})
                
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
                                yield "<FitParameters functionRef=F%s-%s>" % (NODEID, fref)
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
                                        yield "<UpperLimit>%s</UpperLimit>"
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
                                    yield "<Accuracy>%s</Accuracy>" % accur
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

                        yield "<DataXY>"

                        # handle X components of XY
                        Nx = G("CollisionTabulatedDataXN")
                        xunits = G("CollisionTabulatedDataXUnits")
                                                
                        yield "<X units='%s' parameter='%s'" % (Nx, xunits)                    
                        yield "<DataList n='%s' units='%s'>%s</DataList>" % (Nx, xunits, " ".join(makeiter(G("CollisionTabulatedDataX"))))
                        yield "<Error> n='%s' units='%s'>%s</Error>" % (Nx, xunits, " ".join(makeiter(G("CollisionTabulatedDataYError"))))
                        yield "<NegativeError> n='%s' units='%s'>%s</NegativeError>" % (Nx, xunits, " ".join(makeiter(G("CollisionTabulatedDataXNegativeError"))))
                        yield "<PositiveError> n='%s' units='%s'>%s</PositiveError>" % (Nx, xunits, " ".join(makeiter(G("CollisionTabulatedDataXPositiveError"))))
                        yield "<DataDescription>%s</DataDescription>" % G("CollisionTabulatedDataXDescription")
                        yield "</X>"                    

                        # handle Y components of XY
                        Ny = G("CollisionTabulatedDataYN")
                        yunits = G("CollisionTabulatedDataYUnits")

                        yield "<Y units='%s' parameter='%s'" % (Ny, yunits)                    
                        yield "<DataList n='%s' units='%s'>%s</DataList>" % (Ny, yunits, " ".join(makeiter(G("CollisionTabulatedDataY"))))
                        yield "<Error> n='%s' units='%s'>%s</Error>" % (Ny, yunits, " ".join(makeiter(G("CollisionTabulatedDataYError"))))
                        yield "<NegativeError> n='%s' units='%s'>%s</NegativeError>" % (Ny, yunits, " ".join(makeiter(G("CollisionTabulatedDataYNegativeError"))))
                        yield "<PositiveError> n='%s' units='%s'>%s</PositiveError>" % (Ny, yunits, " ".join(makeiter(G("CollisionTabulatedDataYPositiveError"))))
                        yield "<DataDescription>%s</DataDescription>" % G("CollisionTabulatedDataYDescription")
                        yield "</Y>"                    

                        yield "</DataXY>"

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
        yield makePrimaryType("NonRadiativeTransition", "NonRadTran", G)
        
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
        yield "<Expression computerLanguage=%s>%s</Expression>\n" % (G("FunctionComputerLanguage"), G("FunctionExpression"))
        yield "<Y name='%s', units='%s'>" % (G("FunctionYName"), G("FunctionYUnits"))
        desc = G("FunctionYDescription")        
        if desc:
            yield "<Description>%s</Description>" % desc
        lowlim = G("FunctionYLowerLimit")
        if lowlim: 
            yield "<LowerLimit>%s</LowerLimit>" % lowlim
        hilim = G("FunctionYUpperLimit")
        if hilim:
            yield "<UpperLimit>%s</UpperLimit>"
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
            for Parameter in makeiter(Function.Parameters):

                cont, ret = checkXML(Parameter)
                if cont:
                    yield ret
                    continue 

                GP = lambda name: GetValue(name, Parameter=Parameter)
                yield "<Parameter name='%s', units='%s'>" % (GP("FunctionParameterName"), GP("FunctionParameterUnits"))
                desc = GP("FunctionParameterDescription")
                if desc:
                    yield "<Description>%s</Description>" % desc
                yield "</Parameter>\n"
            yield "</Parameters>"

        yield """<ReferenceFrame>%s</ReferenceFrame>
<Description>%s</Description>
<SourceCodeURL>%s</SourceCodeURL>
""" % (G("FunctionReferenceFrame"), G("FunctionDescription"), G("FunctionSourceCodeURL"))        
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

        methodsourcerefs = G('MethodSourceRef')
        if methodsourcerefs != '':
            # make it always into a list to be looped over, even if
            # only single entry
            try:
                methodsourcerefs = eval(methodsourcerefs)
            except:
                pass
            if not isiterable(methodsourcerefs): 
                methodsourcerefs = [methodsourcerefs]
            for sourceref in methodsourcerefs:
                yield '<SourceRef>B%s-%s</SourceRef>\n'% (NODEID, sourceref)

        yield """<Category>%s</Category>\n<Description>%s</Description>\n"""\
             % (G('MethodCategory'), G('MethodDescription'))

        yield '</Method>\n'
    yield '</Methods>\n'

def generatorError(where):
    log.critical('Generator error in%s!' % where, exc_info=sys.exc_info())
    return where

def Xsams(HeaderInfo=None, Sources=None, Methods=None, Functions=None,
          Environments=None, Atoms=None, Molecules=None, Solids=None, Particles=None, 
          CollTrans=None, RadTrans=None, RadCross=None, NonRadTrans=None):
    """
    The main generator function of XSAMS. This one calls all the
    sub-generators above. It takes the query sets that the node's
    setupResult() has constructed as arguments with given names.
    This function is to be passed to the HTTP-respose object directly
    and not to be looped over beforehand.
    """

    yield """<?xml version="1.0" encoding="UTF-8"?>
<XSAMSData xmlns="http://vamdc.org/xml/xsams/0.2"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://vamdc.org/xml/xsams/0.2 ../../xsams.xsd">
"""

    if HeaderInfo:
        if HeaderInfo.has_key('Truncated'):
            if HeaderInfo['Truncated'] != None: # note: allow 0 percent
                yield """
<!--
   ATTENTION: The amount of data returned has been truncated by the node.
   The data below represent %s percent of all available data at this node that
   matched the query.
-->
""" % HeaderInfo['Truncated']

    errs=''

    log.debug('Working on Sources.')
    try:
        for Source in XsamsSources(Sources): 
            yield Source
    except: errs+=generatorError(' Sources')

    log.debug('Working on Methods, Functions, Environments.')
    try:
        for Method in XsamsMethods(Methods):
            yield Method
    except: errs+=generatorError(' Methods')

    try:
        for Function in XsamsFunctions(Functions):
            yield Function
    except: errs+=generatorError(' Functions')

    try:
        for Environment in XsamsEnvironments(Environments):
            yield Environment
    except: errs+=generatorError(' Environments')

    yield '<Species>\n'
    log.debug('Working on Atoms.')
    try:
        for Atom in XsamsAtoms(Atoms):
            yield Atom
    except: errs+=generatorError(' Atoms')

    log.debug('Working on Molecules.')
    try:
        for Molecule in XsamsMolecules(Molecules):
            yield Molecule
    except: errs+=generatorError(' Molecules')

    log.debug('Working on Solids.')
    try:
        for Solid in XsamsSolids(Solids):
            yield Solid
    except: errs += generatorError(' Solids')

    log.debug('Working on Particles.')
    try:
        for Particle in XsamsParticles(Particles):
            yield Particle
    except: errs += generatorError(' Particles')

    yield '</Species>\n'

    log.debug('Writing Processes.')
    yield '<Processes>\n'
    yield '<Radiative>\n'
    try:
        for RadTran in XsamsRadTrans(RadTrans):
            yield RadTran
    except: 
        errs+=generatorError(' RadTran')


    try:
        for RadCros in XsamsRadCross(RadCross):
            yield RadCros
    except: errs+=generatorError(' RadCross')

    yield '</Radiative>\n'

    try:
        for CollTran in XsamsCollTrans(CollTrans):
            yield CollTran
    except: errs+=generatorError(' CollTran')

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


#
################# Virtual Observatory TABLE GENERATORS ####################
#
# Obs - not updated to latest versions

def sources2votable(sources):
    """
    Sources to VO
    """
    for source in sources:
        yield ''

def states2votable(states):
    """
    States to VO 
    """
    yield """<TABLE name="states" ID="states">
      <DESCRIPTION>The States that are involved in transitions</DESCRIPTION>
      <FIELD name="species name" ID="specname" datatype="char" arraysize="*"/>
      <FIELD name="energy" ID="energy" datatype="float" unit="1/cm"/>
      <FIELD name="id" ID="id" datatype="int"/>
      <FIELD name="charid" ID="charid" datatype="char" arraysize="*"/>
      <DATA>
        <TABLEDATA>"""

    for state in states:
        yield  '<TR><TD>not implemented</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD></TR>' % (state.energy, state.id, state.charid)
    yield """</TABLEDATA></DATA></TABLE>"""

def transitions2votable(transs, count):
    """
    Transition to VO 
    """
    if type(transs) == type([]):
        n = len(transs)
    else:
        transs.count()
    yield u"""<TABLE name="transitions" ID="transitions">
      <DESCRIPTION>%d transitions matched the query. %d are shown here:</DESCRIPTION>
      <FIELD name="wavelength (air)" ID="airwave" datatype="float" unit="Angstrom"/>
      <FIELD name="wavelength (vacuum)" ID="vacwave" datatype="float" unit="Angstrom"/>
      <FIELD name="log(g*f)"   ID="loggf" datatype="float"/>
      <FIELD name="effective lande factor" ID="landeff" datatype="float"/>
      <FIELD name="radiative gamma" ID="gammarad" datatype="float"/>
      <FIELD name="stark gamma" ID="gammastark" datatype="float"/>
      <FIELD name="waals gamma" ID="gammawaals" datatype="float"/>
      <FIELD name="upper state id" ID="upstateid" datatype="char" arraysize="*"/>
      <FIELD name="lower state id" ID="lostateid" datatype="char" arraysize="*"/>
      <DATA>
        <TABLEDATA>""" % (count or n, n)
    for trans in transs:
        yield  '<TR><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD></TR>\n' % (trans.airwave, trans.vacwave, trans.loggf, 
                                                                                                                                   trans.landeff , trans.gammarad ,trans.gammastark , 
                                                                                                                                   trans.gammawaals , trans.upstateid, trans.lostateid)
    yield """</TABLEDATA></DATA></TABLE>"""


# DO NOT USE THIS, but quoteattr() as imported above
# Returns an XML-escaped version of a given string. The &, < and > characters are escaped.
#def xmlEscape(s):
#    if s:
#        return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
#    else:
#        return None


def votable(transitions, states, sources, totalcount=None):
    """
    VO base definition
    """

    yield """<?xml version="1.0"?>
<!--
<?xml-stylesheet type="text/xml" href="http://vamdc.fysast.uu.se:8888/VOTable2XHTMLbasic.xsl"?>
-->
<VOTABLE version="1.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xmlns="http://www.ivoa.net/xml/VOTable/v1.2"
 xmlns:stc="http://www.ivoa.net/xml/STC/v1.30" >
  <RESOURCE name="queryresults">
    <DESCRIPTION>
    </DESCRIPTION>
    <LINK></LINK>
"""
    for source in sources2votable(sources):
        yield source
    for state in states2votable(states):
        yield state
    for trans in transitions2votable(transitions,totalcount):
        yield trans
    yield """
</RESOURCE>
</VOTABLE>
"""

#######################

def transitions2embedhtml(transs,count):
    """
    Converting Transition to html
    """

    if type(transs) == type([]):
        n = len(transs)
    else:
        transs.count()
        n = transs.count()
    yield u"""<TABLE name="transitions" ID="transitions">
      <DESCRIPTION>%d transitions matched the query. %d are shown here:</DESCRIPTION>
      <FIELD name="AtomicNr" ID="atomic" datatype="int"/>
      <FIELD name="Ioniz" ID="ion" datatype="int"/>
      <FIELD name="wavelength (air)" ID="airwave" datatype="float" unit="Angstrom"/>
      <FIELD name="log(g*f)"   ID="loggf" datatype="float"/>
   <!--   <FIELD name="effective lande factor" ID="landeff" datatype="float"/>
      <FIELD name="radiative gamma" ID="gammarad" datatype="float"/>
      <FIELD name="stark gamma" ID="gammastark" datatype="float"/>
      <FIELD name="waals gamma" ID="gammawaals" datatype="float"/>
  -->    <FIELD name="upper state id" ID="upstateid" datatype="char" arraysize="*"/>
      <FIELD name="lower state id" ID="lostateid" datatype="char" arraysize="*"/>
      <DATA>
        <TABLEDATA>"""%(count or n, n)

    for trans in transs:
        yield  '<TR><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD></TR>\n' % (trans.species.atomic, trans.species.ion,
                                                                                                  trans.airwave, trans.loggf,) #trans.landeff , trans.gammarad ,
                                                                                                  #trans.gammastark , trans.gammawaals , xmlEscape(trans.upstateid), xmlEscape(trans.lostateid))
    yield '</TABLEDATA></DATA></TABLE>'

def embedhtml(transitions,totalcount=None):
    """
    Embed html 
    """

    yield """<?xml version="1.0"?>
<!--
<?xml-stylesheet type="text/xml" href="http://vamdc.fysast.uu.se:8888/VOTable2XHTMLbasic.xsl"?>
-->
<VOTABLE version="1.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xmlns="http://www.ivoa.net/xml/VOTable/v1.2" 
 xmlns:stc="http://www.ivoa.net/xml/STC/v1.30" >
  <RESOURCE name="queryresults">
    <DESCRIPTION>
    </DESCRIPTION>
    <LINK></LINK>
"""
    for trans in transitions2embedhtml(transitions, totalcount):
        yield trans
    yield """
</RESOURCE>
</VOTABLE>
"""

