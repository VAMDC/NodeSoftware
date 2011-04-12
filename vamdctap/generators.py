# -*- coding: utf-8 -*-

import re
import sys
from xml.sax.saxutils import quoteattr

# Get the node-specific parts
from django.conf import settings
from django.utils.importlib import import_module
DICTS=import_module(settings.NODEPKG+'.dictionaries')

# This must always be set.
try:
    NODEID = DICTS.RETURNABLES['NodeID']
except:
    NODEID = 'PleaseFillTheNodeID'

def LOG(s):
    if settings.DEBUG: print >> sys.stderr, s.encode('utf-8')

# Helper function to test if an object is a list or tuple
isiterable = lambda obj: hasattr(obj, '__iter__')
escape = lambda s: quoteattr(s)[1:-1]

def countReturnables(regexp):
    """
    count how often a certain matches the keys of the returnables
    """
    r = re.compile(regexp,flags=re.IGNORECASE)
    return len(filter(r.match, DICTS.RETURNABLES.keys()))

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

def GetValue(name,**kwargs):
    """
    the function that gets a value out of the query set, using the global name
    and the node-specific dictionary.
    """
    try:
        name=DICTS.RETURNABLES[name]
    except:
        return ''     # The value is not in the dictionary for the node.
                      # This is fine.
                      # Note that this is also used by if-clauses below
                      # since the empty string evaluates as False.

    if not name:
        return '' # if the key was in the dict, but the value empty or None

    for key in kwargs:
        # assign the dict-value to a local variable named as the dict-key
        exec('%s=kwargs["%s"]'%(key,key))

    try:
        value = eval(name) # this works, if the dict-value is named
                         # correctly as the query-set attribute
    except Exception,e: 
#        LOG('Exception in generators.py: GetValue()')
#        LOG(str(e))
#        LOG(name)
        value = name      # this catches the case where the dict-value
                        # is a string or mistyped.

    if value==None:
        return ''       # if the database returned NULL

    # turn it into a string, quote it, but skip the quotation marks
    # edit - no, we need to have the object itself sometimes to loop over
    #return quoteattr('%s'%value)[1:-1] # re
    return value

def makeSourceRefs(refs):
    s=''
    if refs:
        if isiterable(refs):
            for ref in refs:
                s+='<SourceRef>B%s-%s</SourceRef>'%(NODEID,ref)
        else: s+='<SourceRef>B%s-%s</SourceRef>'%(NODEID,refs)
    return s

def makePartitionfunc(keyword,G):
    """
    This is for creating the partionfunction - element.
    """
    value=G(keyword)
    if not value: return ''
    
    temperature=G(keyword+'T')
    partitionfunc = G(keyword)
    
    s='<PartitionFunction>\n'
    s+='  <T units="K">\n'
    s+='     <Datalist>\n'
    for temp in temperature: s+=' %s' % temp   
    s+='\n     </Datalist>\n'
    s+='  </T>\n'
    s+='  <Q>\n'
    s+='     <Datalist>\n'
    for q in partitionfunc: s+=' %s' % q
    s+='\n     </Datalist>\n'
    s+='  </Q>\n'
    s+='</PartitionFunction>\n'

    return s

def makeDataType(tagname,keyword,G,extraAttr=None,extraElem=None):
    """
    This is for treating the case where a keyword corresponds to a
    DataType in the schema which can have units, comment, sources etc.
    The dictionary-suffixes are appended and the values retrieved. If the
    sources is iterable, it is looped over.
    """
    value=G(keyword)
    if not value: return ''

    unit=G(keyword+'Unit')
    method=G(keyword+'Method')
    comment=G(keyword+'Comment')
    acc=G(keyword+'Accuracy')
    refs=G(keyword+'Ref')

    s='\n<%s'%tagname
    if method: s+=' methodRef="M%s-%s"'%(NODEID,method)
    if extraAttr:
        for key,value in extraAttr.items():
            s+=' %s="%s"'%(key,G(value))
    s+='>'

    if comment: s+='<Comments>%s</Comments>'%quoteattr('%s'%comment)[1:-1]
    s+=makeSourceRefs(refs)
    s+='<Value units="%s">%s</Value>'%(unit or 'unitless',value)
    if acc: s+='<Accuracy>%s</Accuracy>'%acc
    s+='</%s>'%tagname

    if extraElem:
        for key,value in extraElem.items():
            s+='<%s>%s</%s>'%(key,G(value),key)

    return s

def makeNamedDataType(tagname,keyword,G):
    """
    Similar to makeDataType above, but allows the result of G()
    to be iterable and adds the name-attribute. If the 
    corresponding refs etc are not iterable, they are replicated
    for each tag.
    """
    value=G(keyword)
    if not value: return ''

    unit=G(keyword+'Unit')
    method=G(keyword+'Method')
    comment=G(keyword+'Comment')
    acc=G(keyword+'Accuracy')
    refs=G(keyword+'Ref')
    name=G(keyword+'Name')

# make everything iterable
    value,unit,method,comment,acc,refs,name = [ [x] if not isiterable(x) else x  for x in [value,unit,method,comment,acc,refs,name]]

# if some are shorter than the value list, replicate them
    l = len(value)
    value,unit,method,comment,acc,refs,name = [ x*l if len(x)<l else x for x in [value,unit,method,comment,acc,refs,name]]

    s = ''
    for i,val in enumerate(value):
        s+='\n<%s'%tagname
        if method[i]: s+=' methodRef="M%s-%s"'%(NODEID,method[i])
        s+='>'
        if name[i]: s+='<Name>%s</Name>'%name[i]
        if comment[i]: s+='<Comments>%s</Comments>'%escape('%s'%comment[i])
        s+=makeSourceRefs(refs[i])
        s+='<Value units="%s">%s</Value>'%(unit[i] or 'unitless',value[i])
        if acc[i]: s+='<Accuracy>%s</Accuracy>'%acc[i]
        s+='</%s>'%tagname

    return s

def XsamsSources(Sources):
    if not Sources: return
    yield '<Sources>'
    for Source in Sources:
        if hasattr(Source,'XML'):
            try:
                yield Source.XML()
                continue
            except:
                pass

        G = lambda name: GetValue(name, Source=Source)
        yield '<Source sourceID="B%s-%s"><Authors>\n' % (NODEID, G('SourceID'))
        authornames=G('SourceAuthorName')
        # make it always into a list to be looped over, even if
        # only single entry
        try:
            authornames = eval(authornames)
        except:
            pass
        if not isiterable(authornames): authornames=[authornames]
        for author in authornames:
            yield '<Author><Name>%s</Name></Author>\n'%author

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
    if not isiterable(Environments): return
    yield '<Environments>'
    for Environment in Environments:
        if hasattr(Environment,'XML'):
            try:
                yield Environment.XML()
                continue
            except:
                pass

        G = lambda name: GetValue(name, Environment=Environment)
        yield '<Environment envID="E%s-%s">' % (NODEID, G('EnvironmentID'))
        yield makeSourceRefs(G('EnvironmentRef'))
        yield '<Comments>%s</Comments>' % G('EnvironmentComment')
        yield makeDataType('Temperature', 'EnvironmentTemperature', G)
        yield makeDataType('TotalPressure', 'EnvironmentTotalPressure', G)
        yield makeDataType('TotalNumberDensity', 
            'EnvironmentTotalNumberDensity', G)
        species=G('EnvironmentSpecies')
        if species:
            yield '<Composition>'
            if isiterable(species):
                for Species in species:
                    yield '<Species name="%s" speciesRef="X%s-%s">'%(G('EnvironmentSpeciesName'),NODEID,G('EnvironmentSpeciesRef'))
                    yield
                    makeDataType('PartialPressure', 
                        'EnvironmentSpeciesPartialPressure', G)
                    yield makeDataType('MoleFraction',
                        'EnvironmentSpeciesMoleFraction', G)
                    yield makeDataType('Concentration',
                        'EnvironmentSpeciesConcentration', G)
                    yield '</Species>'
            else:
                yield '<Species name="%s" speciesRef="X%s-%s">'%(G('EnvironmentSpeciesName'),NODEID,G('EnvironmentSpeciesRef'))
                yield makeDataType('PartialPressure',
                    'EnvironmentSpeciesPartialPressure', G)
                yield makeDataType('MoleFraction',
                    'EnvironmentSpeciesMoleFraction', G)
                yield makeDataType('Concentration',
                    'EnvironmentSpeciesConcentration', G)
                yield '</Species>'
            yield '</Composition>'
        yield '</Environment>'
    yield '</Environments>\n'

def XsamsAtomTerm(G):
    """
    The part of XSAMS with the term designation and coupling for atoms.
    """
    coupling=G('AtomStateCoupling')
    if not coupling: return ''
    l=G('AtomStateL')
    s=G('AtomStateS')
    k=G('AtomStateK')
    s2=G('AtomStateS2')
    j1=G('AtomStateJ1')
    j2=G('AtomStateJ2')

    result = '<Term>'
    if coupling == "LS" and l and s:
        result += '<LS><L><Value>%d</Value></L><S>%.1f</S></LS>' % (l, s)

    elif coupling == "JK" and s2 and k:
        result += '<jK><j>%s</j><K> %s</K></jK>' % (s2, k)

    elif coupling == "JJ" and j1 and j2:
        result += '<J1J2><j>%s</j><j>%s</j></J1J2>' % (j1, j2)

    result += '</Term>'
    return result

def parityLabel(parity):
    """
    XSAMS whats this as strings "odd" or "even", not numerical

    """
    try: parity = float(parity)
    except: return parity

    if parity % 2:
        return 'odd'
    else:
        return 'even'

def XsamsAtoms(Atoms):
    """
    Generator (yield) for the main block of XSAMS for the atoms, with an inner
    loop for the states. The QuerySet that comes in needs to have a nested
    QuerySet called States attached to each entry in Atoms.

    """

    if not isiterable(Atoms): return
    if not Atoms.count(): return

    yield '<Atoms>'

    for Atom in Atoms:
        G=lambda name: GetValue(name,Atom=Atom)
        yield """<Atom>
<ChemicalElement>
<NuclearCharge>%s</NuclearCharge>
<ElementSymbol>%s</ElementSymbol>
</ChemicalElement>"""%(G('AtomNuclearCharge'),G('AtomSymbol'))

        yield """<Isotope>
<IsotopeParameters>
<MassNumber>%s</MassNumber>%s"""%(G('AtomMassNumber'), makeDataType('Mass','AtomMass',G))
        nucspin=G('AtomNuclearSpin')
        if nucspin: yield '<NuclearSpin>%s</NuclearSpin>'%nucspin
        yield '</IsotopeParameters>'

        yield '<Ion speciesID="X%s-%s"><IonCharge>%s</IonCharge>' % ( NODEID, G('AtomSpeciesID'), G('AtomIonCharge'))
        if not hasattr(Atom,'States'): Atom.States = []
        for AtomState in Atom.States:
            G=lambda name: GetValue(name, AtomState=AtomState)
            yield """<AtomicState stateID="S%s-%s">"""%( G('NodeID'), G('AtomStateID') )
            comm = G('AtomStateDescription')
            if comm: yield '<Comments>%s</Comments>'%comm
            yield makeSourceRefs(G('AtomStateRef'))
            desc = G('AtomStateDescription')
            if desc: yield '<Description>%s</Description>'%desc

            yield '<AtomicNumericalData>'
            yield makeDataType('StateEnergy','AtomStateEnergy',G)
            yield makeDataType('IonizationEnergy','AtomStateIonizationEnergy',G)
            yield makeDataType('LandeFactor','AtomStateLandeFactor',G)
            yield makeDataType('QuantumDefect','AtomStateQuantumDefect',G)
            yield makeDataType('TotalLifeTime','AtomStateLifeTime',G)
            yield makeDataType('Polarizability','AtomStatePolarizability',G)
            statweig = G('AtomStateStatisticalWeight')
            if statweig: yield '<StatisticalWeight></StatisticalWeight>'%statweig
            yield makeDataType('HyperfineConstantA','AtomStateHyperfineConstantA',G)
            yield makeDataType('HyperfineConstantB','AtomStateHyperfineConstantB',G)
            yield '</AtomicNumericalData><AtomicQuantumNumbers>'
            p,j,k,hfm,mqn = G('AtomStateParity'), G('AtomStateTotalAngMom'),\
                         G('AtomStateKappa'), G('AtomStateHyperfineMomentum'),\
                         G('AtomStateMagneticQuantumNumber')
            if p: yield '<Parity>%s</Parity>'%parityLabel(p)
            if j: yield '<TotalAngularMomentum>%s</TotalAngularMomentum>'%j
            if k: yield '<Kappa>%s</Kappa>'%k
            if hfm: yield '<HyperfineMomentum>%s</HyperfineMomentum>'%hfm
            if mqn: yield '<MagneticQuantumNumber>%s</MagneticQuantumNumber>'%mqn
            yield '</AtomicQuantumNumbers>'

            yield '<AtomicComposition>'
            comm = G('AtomStateCompositionComments')
            if comm: yield '<Comments>%s</Comments>\n'%comm
            yield '<Component><Configuration>'
            confl = G('AtomStateConfigurationLabel')
            if confl: yield '<ConfigurationLabel>%s</ConfigurationLabel>'%confl
# AtomicCore and Shells are missing here!
            yield '</Configuration>\n'

            yield XsamsAtomTerm(G)

            mixcoef = G('AtomStateMixingCoefficient')
            if mixcoef: yield '<MixingCoefficient>%s</MixingCoefficient>'%mixcoef
            yield '</Component></AtomicComposition>'
            yield '</AtomicState>'
        yield '<InChI>%s</InChI>'%G('AtomInchi')
        yield '<InChIKey>%s</InChIKey>'%G('AtomInchiKey')
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
    G=lambda name: GetValue(name, Molecule=Molecule)
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

    yield makePartitionfunc("MoleculePartitionFunction",G)

    yield '<StableMolecularProperties>\n%s</StableMolecularProperties>\n'%makeDataType('MolecularWeight','MoleculeMolecularWeight',G)
    if G("MoleculeComment"):
        yield '<Comment>%s</Comment>\n' % G("MoleculeComment")
    yield '</MolecularChemicalSpecies>\n'

def XsamsMSQNsBuild(MolQNs):
    G = lambda name: GetValue(name, MolQN=MolQN)
    MolQN = MolQNs[0]; case = G('MoleculeQnCase')
    yield '<%s:QNs>\n' % case
    for MolQN in MolQNs:
        qn_attr = ''
        if G('MoleculeQnAttribute'):
            qn_attr = ' %s' % G('MoleculeQnAttribute')
        yield '<%s:%s%s>%s</%s:%s>\n' % (G('MoleculeQnCase'), G('MoleculeQnLabel'),
            qn_attr, G('MoleculeQnValue'), G('MoleculeQnCase'), G('MoleculeQnLabel'))
    yield '</%s:QNs>\n' % case

def XsamsMSBuild(MoleculeState):
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
    yield '  </MolecularStateCharacterisation>\n'
    if G("MoleculeStateQuantumNumbers"):
        for MSQNs in XsamsMSQNsBuild(G("MoleculeStateQuantumNumbers")):
            yield MSQNs
    yield '</MolecularState>\n'

def XsamsMolecules(Molecules):
    if not Molecules: return
    yield '<Molecules>\n'
    for Molecule in Molecules:
        G = lambda name: GetValue(name, Molecule=Molecule)
        yield '<Molecule speciesID="X%s">\n' % G("MoleculeID")
        # write the MolecularChemicalSpecies description:
        for MCS in XsamsMCSBuild(Molecule):
            yield MCS

        if not hasattr(Molecule,'States'): Molecule.States = []
        for MoleculeState in Molecule.States:
            for MS in XsamsMSBuild(MoleculeState):
                yield MS

        yield '</Molecule>\n'
    yield '</Molecules>\n'

###############
# END SPECIES
# BEGIN PROCESSES
#################

def makeBroadeningType(G,btype='Natural'):
    lsparams = makeNamedDataType('LineshapeParameter','RadTransBroadening%sLineshapeParameter'%btype,G)
    if not lsparams: return ''

    env = G('RadTransBroadening%sEnvironment'%btype)
    meth = G('RadTransBroadening%sMethod'%btype)
    comm = G('RadTransBroadening%sComment'%btype)
    s = '<%sBroadening'%btype
    if meth: s += ' methodRef="%s"'%meth
    if env: s += ' envRef="%s"'%env
    s += '>'
    if comm: s +='<Comments>%s</Comments>'%comm
    s += makeSourceRefs(G('RadTransBroadening%sRef'%btype))

    # in principle we should loop over lineshapes but
    # lets not do so unless somebody actually has several lineshapes
    # per broadening type
    s += '<Lineshape name="%s">'%G('RadTransBroadening%sLineshapeName'%btype)
    s += lsparams
    s += '</Lineshape>'
    s += '</%sBroadening>'%btype
    return s

def XsamsRadTranBroadening(G):
    """
    helper function for line broadening, called from RadTrans
    """
    s = '<Broadenings>'
    comm = G('RadTransBroadeningComment')
    if comm: s +='<Comments>%s</Comments>'%comm
    s += makeSourceRefs(G('RadTransBroadeningRef'))
    if countReturnables('RadTransBroadeningStark'):
        s += makeBroadeningType(G,btype='Stark')
    if countReturnables('RadTransBroadeningVanDerWaals'):
        s += makeBroadeningType(G,btype='VanDerWaals')
    if countReturnables('RadTransBroadeningNatural'):
        s += makeBroadeningType(G,btype='Natural')
    if countReturnables('RadTransBroadeningInstrument'):
        s += makeBroadeningType(G,btype='Instrument')
    s += '</Broadenings>\n'
    return s

def XsamsRadTranShifting(G):
    return ''

def XsamsRadTrans(RadTrans):
    """
    Generator for the XSAMS radiative transitions.
    """

    if not isiterable(RadTrans): return

    for RadTran in RadTrans:
        G=lambda name: GetValue(name,RadTran=RadTran)
        yield '<RadiativeTransition>'
        comm = G('RadTransComments')
        if comm: yield '<Comments>%s</Comments>'%comm
        yield makeSourceRefs(G('RadTransRefs'))
        yield '<EnergyWavelength>'
        yield makeDataType('Wavelength','RadTransWavelength',G)
        yield makeDataType('Wavenumber','RadTransWavenumber',G)
        yield makeDataType('Frequency','RadTransFrequency',G)
        yield makeDataType('Energy','RadTransEnergy',G)
        yield '</EnergyWavelength>'

        initial = G('RadTransInitialStateRef')
        if initial: yield '<InitialStateRef>S%s-%s</InitialStateRef>\n' % (NODEID, initial)
        final = G('RadTransFinalStateRef')
        if final: yield '<FinalStateRef>S%s-%s</FinalStateRef>\n' % (NODEID, final)
        species = G('RadTransSpeciesRef')
        if species: yield '<SpeciesRef>X%s-%s</SpeciesRef>\n' % (NODEID, species)

        yield '<Probability>'
        yield makeDataType('TransitionProbabilityA','RadTransProbabilityA',G)
        yield makeDataType('OscillatorStrength','RadTransProbabilityOscillatorStrength',G)
        yield makeDataType('LineStrength','RadTransProbabilityLineStrength',G)
        yield makeDataType('WeightedOscillatorStrength','RadTransProbabilityWeightedOscillatorStrength',G)
        yield makeDataType('Log10WeightedOscillatorStrength','RadTransProbabilityLog10WeightedOscillatorStrength',G)
        yield makeDataType('IdealisedIntensity','RadTransProbabilityIdealisedIntensity',G)
        multipole = G('RadTransProbabilityMultipole')
        if multipole: yield '<Multipole>%s</Multipole>'%multipole
        yield makeDataType('EffectiveLandeFactor','RadTransEffectiveLandeFactor',G)
        yield '</Probability>\n'

        if hasattr(RadTran,'XML_Broadening'):
            yield RadTran.XML_Broadening()
        else:
            yield XsamsRadTranBroadening(G)
        if hasattr(RadTran,'XML_Shifting'):
            yield RadTran.XML_Shifting()
        else:
            yield XsamsRadTranShifting(G)
        yield '</RadiativeTransition>\n'


def XsamsRadCross(RadCross):
    """
    for the Radiative/CrossSection part
    """
    yield ''

def XsamsCollTrans(CollTrans):
    """
    collisional transitions
    """
    yield ''

def XsamsNonRadTrans(NonRadTrans):
    """
    non-radiative transitions
    """
    yield ''

def XsamsFunctions(Functions):
    if not isiterable(Functions): return
    yield '<Functions>'
    for Function in Functions:
        if hasattr(Function,'XML'):
            try:
                yield Function.XML()
                continue
            except:
                pass
    yield '</Functions>'

def XsamsMethods(Methods):
    """
    Generator for the methods block of XSAMS
    """
    if not Methods: return
    yield '<Methods>\n'
    for Method in Methods:
        G=lambda name: GetValue(name,Method=Method)
        yield """<Method methodID="M%s-%s">
<Category>%s</Category>
<Description>%s</Description>
"""%(NODEID, G('MethodID'),G('MethodCategory'),G('MethodDescription'))


        methodsourcerefs=G('MethodSourceRef')
        # make it always into a list to be looped over, even if
        # only single entry
        try:
           methodsourcerefs = eval(methodsourcerefs)
        except:
           pass
        if not isiterable(methodsourcerefs): methodsourcerefs=[methodsourcerefs]
        for sourceref in methodsourcerefs:
            yield '<SourceRef>B%s-%s</SourceRef>\n'% (NODEID, sourceref)

        yield '</Method>'


    yield '</Methods>\n'


def Xsams(HeaderInfo=None, Sources=None, Methods=None, Functions=None,
    Environments=None, Atoms=None, Molecules=None, CollTrans=None,
    RadTrans=None, RadCross=None, NonRadTrans=None
          ):
    """
    The main generator function of XSAMS. This one calls all the
    sub-generators above. It takes the query sets that the node's
    setupResult() has constructed as arguments with given names.
    This function is to be passed to the HTTP-respose object directly
    and not to be looped over beforehand.
    """

    yield """<?xml version="1.0" encoding="UTF-8"?>
<XSAMSData xmlns="http://xsams.svn.sourceforge.net/viewvc/xsams/branches/vamdc-working"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://xsams.svn.sourceforge.net/viewvc/xsams/branches/vamdc-working http://xsams.svn.sourceforge.net/viewvc/xsams/branches/vamdc-working/xsams.xsd"
 xmlns:dcs="http://www.ucl.ac.uk/~ucapch0/XSAMS/cases/0.2.1/dcs"  
 xmlns:hunda="http://www.ucl.ac.uk/~ucapch0/XSAMS/cases/0.2.1/hunda" 
 xmlns:hundb="http://www.ucl.ac.uk/~ucapch0/XSAMS/cases/0.2.1/hundb"
 xmlns:ltcs="http://www.ucl.ac.uk/~ucapch0/XSAMS/cases/0.2.1/ltcs"
 xmlns:nltcs="http://www.ucl.ac.uk/~ucapch0/XSAMS/cases/0.2.1/nltcs"
 xmlns:stcs="http://www.ucl.ac.uk/~ucapch0/XSAMS/cases/0.2.1/stcs"
 xmlns:lpcs="http://www.ucl.ac.uk/~ucapch0/XSAMS/cases/0.2.1/lpcs"
 xmlns:asymcs="http://www.ucl.ac.uk/~ucapch0/XSAMS/cases/0.2.1/asymcs"
 xmlns:asymos="http://www.ucl.ac.uk/~ucapch0/XSAMS/cases/0.2.1/asymos"
 xmlns:sphcs="http://www.ucl.ac.uk/~ucapch0/XSAMS/cases/0.2.1/sphcs"
 xmlns:sphos="http://www.ucl.ac.uk/~ucapch0/XSAMS/cases/0.2.1/sphos"
 xmlns:ltos="http://www.ucl.ac.uk/~ucapch0/XSAMS/cases/0.2.1/ltos"
 xmlns:lpos="http://www.ucl.ac.uk/~ucapch0/XSAMS/cases/0.2.1/lpos"
 xmlns:nltos="http://www.ucl.ac.uk/~ucapch0/XSAMS/cases/0.2.1/nltos"
>
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

    LOG('Working on Sources.')
    for Source in XsamsSources(Sources): yield Source

    LOG('Working on Methods, Functions, Environments.')
    for Method in XsamsMethods(Methods): yield Method
    for Function in XsamsFunctions(Functions): yield Function
    for Environment in XsamsEnvironments(Environments): yield Environment

    LOG('Writing States.')
    yield '<Species>\n'
    for Atom in XsamsAtoms(Atoms): yield Atom
    for Molecule in XsamsMolecules(Molecules): yield Molecule
    # old way:
    #for MolState in XsamsMolStates(Molecules, MoleStates, MoleQNs):
    #    yield MolState
    yield '</Species>\n'

    LOG('Writing Processes.')
    yield '<Processes>\n'
    yield '<Radiative>\n'
    for RadTran in XsamsRadTrans(RadTrans): yield RadTran
    for RadCros in XsamsRadCross(RadCross): yield RadCros
    yield '</Radiative>\n'
    for CollTran in XsamsCollTrans(CollTrans): yield CollTran
    for NonRadTran in XsamsNonRadTrans(NonRadTrans): yield NonRadTran
    yield '</Processes>\n'
    yield '</XSAMSData>\n'
    LOG('Done with XSAMS')
















##########################################################
######## VO TABLE GENERATORS ####################

def sources2votable(sources):
    for source in sources:
        yield ''

def states2votable(states):
    yield """<TABLE name="states" ID="states">
      <DESCRIPTION>The States that are involved in transitions</DESCRIPTION>
      <FIELD name="species name" ID="specname" datatype="char" arraysize="*"/>
      <FIELD name="energy" ID="energy" datatype="float" unit="1/cm"/>
      <FIELD name="id" ID="id" datatype="int"/>
      <FIELD name="charid" ID="charid" datatype="char" arraysize="*"/>
      <DATA>
        <TABLEDATA>"""

    for state in states:
        yield  '<TR><TD>not implemented</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD></TR>'%(state.energy,state.id,state.charid)

    yield """</TABLEDATA></DATA></TABLE>"""

def transitions2votable(transs,count):
    if type(transs)==type([]):
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
        <TABLEDATA>"""%(count or n,n)

    for trans in transs:
        yield  '<TR><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD></TR>\n'%(trans.airwave, trans.vacwave, trans.loggf, trans.landeff , trans.gammarad ,trans.gammastark , trans.gammawaals , trans.upstateid, trans.lostateid)

    yield """</TABLEDATA></DATA></TABLE>"""


# DO NOT USE THIS, but quoteattr() as imported above
# Returns an XML-escaped version of a given string. The &, < and > characters are escaped.
#def xmlEscape(s):
#    if s:
#        return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
#    else:
#        return None


def votable(transitions,states,sources,totalcount=None):
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
    if type(transs)==type([]):
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
        <TABLEDATA>"""%(count or n,n)

    for trans in transs:
        yield  '<TR><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD></TR>\n'%(trans.species.atomic, trans.species.ion,trans.airwave, trans.loggf,) #trans.landeff , trans.gammarad ,trans.gammastark , trans.gammawaals , xmlEscape(trans.upstateid), xmlEscape(trans.lostateid))
    yield '</TABLEDATA></DATA></TABLE>'

def embedhtml(transitions,totalcount=None):
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
    for trans in transitions2embedhtml(transitions,totalcount):
        yield trans
    yield """
</RESOURCE>
</VOTABLE>
"""

