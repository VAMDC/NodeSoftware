# -*- coding: utf-8 -*-

import re
import sys
from xml.sax.saxutils import quoteattr

# Get the node-specific parts
from django.conf import settings
from django.utils.importlib import import_module
DICTS=import_module(settings.NODEPKG+'.dictionaries')

# This must always be 
try:
    NODEID = DICTS.RETURNABLES['NodeID']
except:
    NODEID = 'PleaseFillTheNodeID'

def LOG(s):
    if settings.DEBUG: print >> sys.stderr, s.encode('utf-8')

# Helper function to test if an object is a list or tuple
isiterable = lambda obj: hasattr(obj, '__iter__')

def countReturnables(s):
    """
    count how often a certain (sub)string is in the keys of the returnables
    """
    return len(filter(lambda key: 'atomstate' in key, DICTS.RETURNABLES.keys()))

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

def makeDataType(tagname,keyword,G):
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
    s+='>'
    
    if comment: s+='<Comments>%s</Comments>'%quoteattr('%s'%comment)[1:-1]
    s+=makeSourceRefs(refs)
    s+='<Value units="%s">%s</Value>'%(unit or 'unitless',value)
    if acc: s+='<Accuracy>%s</Accuracy>'%acc
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
        yield '<Source sourceID="B%s"><Authors>\n'%G('SourceID') 
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
        yield '<Environment envID="E%s-%s">'%(NODEID,G('EnvironmentID'))
        yield makeSourceRefs(G('EnvironmentRef'))
        yield '<Comments>%s</Comments>'%G('EnvironmentComment')
        yield makeDataType('Temperature','EnvironmentTemperature')
        yield makeDataType('TotalPressure','EnvironmentTotalPressure')
        yield makeDataType('TotalNumberDensity','EnvironmentTotalNumberDensity')
        species=G('EnvironmentSpecies')
        if species:
            yield '<Composition>'
            if isiterable(species):
                for Species in species:
                    yield '<Species name="%s" speciesRef="X%s-%s">'%(G('EnvironmentSpeciesName'),NODEID,G('EnvironmentSpeciesRef'))
                    yield makeDataType('ParitalPressure','EnvironmentSpeciesParitalPressure')
                    yield makeDataType('MoleFraction','EnvironmentSpeciesMoleFraction')
                    yield makeDataType('Concentration','EnvironmentSpeciesConcentration')
                    yield '</Species>'
            else:
                yield '<Species name="%s" speciesRef="X%s-%s">'%(G('EnvironmentSpeciesName'),NODEID,G('EnvironmentSpeciesRef'))
                yield makeDataType('ParitalPressure','EnvironmentSpeciesParitalPressure')
                yield makeDataType('MoleFraction','EnvironmentSpeciesMoleFraction')
                yield makeDataType('Concentration','EnvironmentSpeciesConcentration')
                yield '</Species>'
            yield '</Composition>'
        yield '</Environment>'
    yield '</Environments>'

def XsamsAtomTerm(G):
    """
    The part of XSAMS with the term designation and coupling for atoms.
    Note that this is not a generator but a plain function that returns
    its result.
    """

    #pre-fetch the values that will be tested for below
    coupling=G('AtomStateCoupling')
    l=G('AtomStateL')
    s=G('AtomStateS')
    k=G('AtomStateK')
    s2=G('AtomStateS2')
    j1=G('AtomStateJ1')
    j2=G('AtomStateJ2')
    
    result = '<AtomicComposition>\n<Comments>%s</Comments>\n' \
            % G('AtomStateCompositionComments')
    result += '<Component><Configuration><ConfigurationLabel>%s' \
              '</ConfigurationLabel></Configuration>\n' \
            %G('AtomStateConfigurationLabel')
    result += '<Term>'

    if coupling == "LS" and l and s: 
        result += '<LS><L><Value>%d</Value></L><S>%.1f</S></LS>' % (l, s)
        
    elif coupling == "JK" and s2 and k: 
        result += '<jK><j>%s</j><K> %s</K></jK>' % (s2, k)
        
    elif coupling == "JJ" and j1 and j2:
        result += '<J1J2><j>%s</j><j>%s</j></J1J2>' % (j1, j2)
        
    result += '</Term></Component></AtomicComposition>'
    return result

def parityLabel(parity):
    """
    XSAMS whats this as strings "odd" or "even", not numerical

    """
    if parity % 2:
        return 'odd'
    else:
        return 'even'

def XsamsAtoms(Atoms):
    """
    Generator (yield) for the main block of XSAMS for the atoms, with an inner loop for
    the states. The QuerySet that comes in needs to have a nested QuerySet called States
    attached to each entry in Atoms.

    """

    if not isiterable(Atoms): return

    yield '<Atoms>'

    for Atom in Atoms:
        G=lambda name: GetValue(name,Atom=Atom)
        yield """<Atom>
<ChemicalElement>
<NuclearCharge>%s</NuclearCharge>
<ElementSymbol>%s</ElementSymbol>
</ChemicalElement>
<Isotope>
<IsotopeParameters>
<MassNumber>%s</MassNumber>
</IsotopeParameters>
<Ion speciesID="X%s">
<IonCharge>%s</IonCharge>""" % ( G('AtomNuclearCharge'),
	G('AtomSymbol'), G('AtomMassNumber'), G('AtomSpeciesID'), 
	G('AtomIonCharge'))

        for AtomState in Atom.States:
            G=lambda name: GetValue(name, AtomState=AtomState)
            yield """<AtomicState stateID="S%s"><Description>%s</Description>
<AtomicNumericalData>""" % ( G('AtomStateID'), G('AtomStateDescription') )
            yield makeDataType('IonizationEnergy','AtomStateIonizationEnergy',G)
            yield makeDataType('StateEnergy','AtomStateEnergy',G)
            yield makeDataType('LandeFactor','AtomStateLandeFactor',G)
            yield '</AtomicNumericalData>'
            if (G('AtomStateParity') or G('AtomStateTotalAngMom')):
                yield '<AtomicQuantumNumbers><Parity>%s</Parity>' \
                  '<TotalAngularMomentum>%s</TotalAngularMomentum>' \
                  '</AtomicQuantumNumbers>' % (G('AtomStateParity'),
                                               G('AtomStateTotalAngMom'))

            yield XsamsAtomTerm(G)
            yield '</AtomicState>'
        yield '<InChIKey>%s</InChIKey>'%G('AtomInchiKey')
        yield """</Ion>
</Isotope>
</Atom>"""
    yield '</Atoms>'


def XsamsMolStates(Molecules, MoleStates, MoleQNs=None):
    """
    This function creates the molecular states part.
    In its current form MoleStates contains all information
    about the state including the species part. It does
    not contain informations on the quantum numbers. These
    are provided in the MoleQNs - List. Both are linked via
    the StateId. In the first loop, the MoleQN-List copied into
    a new list of lists using the StateID as keyword.
    Maybe this part could be moved to the view.py in each node.
    In this approach the molecular species information is part
    of the MoleStates, which can be discussed, but probably 
    this approach is faster in terms of performance and more
    appropriate for the VO-Table output, because it reduces the
    number of tables. Here, the MoleStates have to be sorted 
    by Species. If we keep this approach the condition prooves
    the identity of species should use the dictionary which
    is currently under development
    """

    # nothing to see here if the data has no molecules
    if not Molecules: return

    # if MoleQNs was passed as None or not passed at all,
    # it is effectively an empty list:
    if MoleQNs is None:
        MoleQNs = []

    # rearrange QN-Lists into dictionary with stateID as key
    QNList={}
    for MolQN in MoleQNs:
       G=lambda name: GetValue(name,MolQN=MolQN)
       #print '+++G("MolQnStateID") =',G("MolQnStateID")
       if QNList.has_key(G("MolQnStateID")):
          QNList[G("MolQnStateID")].append(MolQN)
          #print G("MolQnStateID")
       else:
          QNList[G("MolQnStateID")]=[MolQN]
    #print 'MoleQNs is %d items long' % len(MoleQNs)
    #print 'QNList is %d items long' % len(QNList)
    #print QNList.keys()

    yield '<Molecules>'
    for Molecule in Molecules:
        G=lambda name: GetValue(name, Molecule=Molecule)
        yield '<Molecule>\n'
        yield '<MolecularChemicalSpecies>\n'
        yield '<OrdinaryStructuralFormula>%s</OrdinaryStructuralFormula>\n' \
            % G("MolecularSpeciesOrdinaryStructuralFormula")
        yield '<StoichiometricFormula>%s</StoichiometricFormula>\n' \
            % G("MolecularSpeciesStoichiometricFormula")
        yield '<ChemicalName>%s</ChemicalName>\n' \
            % G("MolecularSpeciesChemicalName")
        yield '</MolecularChemicalSpecies>\n'
#        thisInchiKey = G("InchiKey")
        speciesid = G("MolecularSpeciesID")
         
        for MolState in MoleStates:
            G = lambda name: GetValue(name, MolState=MolState)
#            if G("InchiKey") != thisInchiKey:

            if G("MolecularStateMolecularSpeciesID") != speciesid:
                continue
            
            yield """<MolecularState stateID="S%s">
<Description>%s</Description>
<MolecularStateCharacterisation>
<StateEnergy energyOrigin="%s">
<Value units="%s">%s</Value>
</StateEnergy>
<TotalStatisticalWeight>%s</TotalStatisticalWeight>
</MolecularStateCharacterisation>
""" %           ( 
                G("MolecularStateStateID"),
                G("MolecularStateDescription"),
                G("MolecularStateEnergyOrigin"),
                G("MolecularStateEnergyUnit"),
                G("MolecularStateEnergyValue"),
                G("MolecularStateCharacTotalStatisticalWeight")
                )
            if QNList.has_key(G("MolecularStateStateID")):
#              G=lambda name: GetValue(name, MolQN=MolQN)

              case=""
              for MolQN in QNList[G("MolecularStateStateID")]:
                G=lambda name: GetValue(name, MolQN=MolQN)
                if G("MolQnCase")!=case :
                   if case:
                       yield '</%s:QNs>' % case
                   yield '<%s:QNs> \n' % G("MolQnCase")
                   case=G("MolQnCase")

                yield """
    <%s:%s """ % (G("MolQnCase"), G("MolQnLabel"))
                if G("MolQnSpinRef"):
                    yield """nuclearSpinRef="%s" """ % (G("MolQnSpinRef"))
                if G("MolQnAttribute"):
                    yield G("MolQnAttribute")
                yield """>%s</%s:%s>""" \
                    % (G("MolQnValue"),G("MolQnCase"),G("MolQnLabel") )

              yield '</%s:QNs>' % case
            yield '</MolecularState>'
        yield '</Molecule>'
    yield '</Molecules>'

def XsamsMCSBuild(Molecule):
    """
    Generator for the MolecularChemicalSpecies
    """
    G=lambda name: GetValue(name, Molecule=Molecule)
    yield '<MolecularChemicalSpecies>\n'
    yield '<OrdinaryStructuralFormula>%s</OrdinaryStructuralFormula>'\
            % G("MolecularSpeciesOrdinaryStructuralFormula")

    yield '<StoichiometricFormula>%s</StoichiometricFormula>'\
            % G("MolecularSpeciesStoichiometrcFormula")
    if G("MolecularSpeciesChemicalName"):
        yield '<ChemicalName>%s</ChemicalName>'\
            % G("MolecularSpeciesChemicalName")
    if G("MolecularSpeciesMolecularWeight"):
        yield '<StableMolecularProperties>'
        yield '<MolecularWeight>'
        yield '  <Value units="%s">%s</Value>'\
            % (G("MolecularSpeciesMolecularWeightUnits"),
               G("MolecularSpeciesMolecularWeight"))
        yield '</MolecularWeight>'
        yield '</StableMolecularProperties>'
    if G("MolecularSpeciesComment"):
        yield '<Comments>%s</Comments>' % G("MolecularSpeciesComment")
    yield '</MolecularChemicalSpecies>\n'


# THIS NEEDS WORK, CDMS-specific things ahead.
def XsamsMSBuild(Molstate):
    G=lambda name: GetValue(name,Molstate=Molstate)
    ret="""<MolecularState stateID="S%">
<Description>%s</Description>
<MolecularStateCharacterisation>
<StateEnergy energyOrigin="%s">
<Value units="%s">%s</Value>
</StateEnergy>
<TotalStatisticalWeight>%s</TotalStatisticalWeight>
</MolecularStateCharacterisation>"""%(
"",
quoteattr(Molstate.title),
"calc",
"1/cm",
"0",
"1")
    ret+="</MolecularState>"
    return ret


def XsamsMolecules(Molecules):
    if not Molecules: return
    yield '<Molecules>\n'
    for Molecule in Molecules:
        G = lambda name: GetValue(name, Molecule=Molecule)
        yield '<Molecule speciesID="%s">\n' % G("MolecularSpeciesID")
        # write the MolecularChemicalSpecies description:
        for MCS in XsamsMCSBuild(Molecule):
            yield MCS
        if Molecule.States:
            for MolecularState in Molecule.States:
                for MS in XsamsMSBuild(MolecularState):
                    yield MS            
        yield '</Molecule>\n'
    yield '</Molecules>\n'

###############
# END SPECIES
# BEGIN PROCESSES
#################

def makeBroadeningType(G,type='Natural'):
    s = '<%sBroadening methodRef=>'%type
    s +='<Comments>%s</Comments>' % G('RadTransBroadening%sComment'%type)
    s += makeSourceRefs(G('RadTransBroadening%sRef'%type))
    s += '</%sBroadening>'%type
    return s

def XsamsRadTranBroadening(G):
    """
    helper function for line broadening, called from RadTrans
    """
    s = '<Broadenings>'
    s +='<Comments>%s</Comments>' % G('RadTransBroadeningComment')
    s += makeSourceRefs(G('RadTransBroadeningRef'))
    if countReturnables('RadTransBroadeningNatural'):
        s += makeBroadeningType(G,type='Natural')
    if countReturnables('RadTransBroadeningStark'):
        s += makeBroadeningType(G,type='Stark')
    if countReturnables('RadTransBroadeningVanDerWaals'):
        s += makeBroadeningType(G,type='VanDerWaals')
    if countReturnables('RadTransBroadeningInstrument'):
        s += makeBroadeningType(G,type='Instrument')
    s += '</Broadenings>'
    return s

def XsamsRadTrans(RadTrans):
    """
    Generator for the XSAMS radiative transitions.
    """

    if not isiterable(RadTrans): return

    yield '<Radiative>'
    for RadTran in RadTrans:
        G=lambda name: GetValue(name,RadTran=RadTran)
        yield '\n<RadiativeTransition><EnergyWavelength>'
        yield makeDataType('Wavelength','RadTransWavelength',G)
        yield makeDataType('Wavenumber','RadTransWavenumber',G)
        yield makeDataType('Frequency','RadTransFrequency',G)
        
        yield '</EnergyWavelength>'

        yield XsamsRadTranBroadening(G)

        initial = G('RadTransInitialStateRef')
        if initial: yield '<InitialStateRef>S%s</InitialStateRef>'%initial
        final = G('RadTransFinalStateRef')
        if final: yield '<FinalStateRef>S%s</FinalStateRef>'%final

        yield '<Probability>'
        yield makeDataType('Log10WeightedOscillatorStrength','RadTransLogGF',G)
        yield makeDataType('TransitionProbabilityA','RadTransProbabilityA',G)
        yield makeDataType('EffectiveLandeFactor','RadTransEffLande',G)        
        yield '</Probability></RadiativeTransition>'
        
    yield '</Radiative>'

def XsamsFunctions(Functions):
    yield ''

def XsamsMethods(Methods):
    """
    Generator for the methods block of XSAMS
    """
    if not Methods: return
    yield '<Methods>\n'
    for Method in Methods:
        G=lambda name: GetValue(name,Method=Method)
        yield """<Method methodID="%s">
<Category>%s</Category>
<Description>%s</Description>
</Method>
"""%(G('MethodID'),G('MethodCategory'),G('MethodDescription'))
    yield '</Methods>\n'


def Xsams(HeaderInfo=None, Sources=None, Methods=None, Functions=None, Environments=None,
          Atoms=None, Molecules=None, CollTrans=None, RadTrans=None, 
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
    xsi:schemaLocation="http://xsams.svn.sourceforge.net/viewvc/xsams/branches/vamdc-working http://xsams.svn.sourceforge.net/viewvc/xsams/branches/vamdc-working/xsams.xsd">
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
    for RadTran in XsamsRadTrans(RadTrans): yield RadTran
    #for CollTrans in XsamsCollTrans(CollTrans): yield CollTrans
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

##############################
### GENERATORS END HERE
##############################

