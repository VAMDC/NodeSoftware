# -*- coding: utf-8 -*-

import re
import sys
from xml.sax.saxutils import quoteattr

# Get the node-specific parts
from django.conf import settings
from django.utils.importlib import import_module
NODEPKG=import_module(settings.NODEPKG+'.views')


def LOG(s):
    if settings.DEBUG: print >> sys.stderr, s.encode('utf-8')

# Helper function to test if an object is a list or tuple
isiterable = lambda obj: hasattr(obj, '__iter__')

def GetValue(name,**kwargs):
    """
    the function that gets a value out of the query set, using the global name
    and the node-specific dictionary.
    """
    try:
        name=NODEPKG.RETURNABLES[name]
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
#        LOG(e)
#        LOG(name)
        value = name      # this catches the case where the dict-value
                        # is a string or mistyped.

    if not value:
        return ''       # if the database returned NULL

    # turn it into a string, quote it, but skip the quotation marks
    return quoteattr('%s'%value)[1:-1] # re
    
def XsamsSources(Sources):
    if not Sources: return
    yield '<Sources>'
    for Source in Sources:
        G = lambda name: GetValue(name,Source=Source)
        yield '<Source sourceID="B%s"><Authors>\n'%G('SourceID') 
        authornames=G('SourceAuthorName')
        # make it always into a list to be looped over, even if
        # only single entry
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

def XsamsAtomTerm(AtomState,G):
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

def XsamsAtomStates(AtomStates):
    """
    Generator (yield) for the main block of XSAMS for the atomic states.

    """

    # if the data has no atomic states, there is nothing to see here...
    if not AtomStates: return

    yield '<Atoms>'

    # Note and Todo: In principle we here abuse the Atom-tag by writing it
    # for new into each state. With some clever re-ordering, we could
    # order the states by atoms and write each of them only once with all
    # its states inside.
    # It needs to be seen however if this is at all possible when we get in
    # data from various nodes.

    for AtomState in AtomStates:
        G=lambda name: GetValue(name,AtomState=AtomState)
        yield """<Atom>
<ChemicalElement>
<NuclearCharge>%s</NuclearCharge>
<ElementSymbol>%s</ElementSymbol>
</ChemicalElement>
<Isotope>
<IsotopeParameters>
<MassNumber>%s</MassNumber>
</IsotopeParameters>
<IonState>
<IonCharge>%s</IonCharge>
<AtomicState stateID="S%s"><Description>%s</Description>
<AtomicNumericalData>
<StateEnergy sourceRef="B%s"><Value units="%s">%s</Value></StateEnergy>
<IonizationEnergy><Value units="eV">%s</Value></IonizationEnergy>
<LandeFactor sourceRef="B%s"><Value units="unitless">%s</Value></LandeFactor>
</AtomicNumericalData>
""" % ( G('AtomNuclearCharge'), G('AtomSymbol'), G('AtomMassNumber'),
        G('AtomIonCharge'), G('AtomStateID'), G('AtomStateDescription'),
        G('AtomStateEnergyRef'), G('AtomStateEnergyUnits'),
        G('AtomStateEnergy'), G('AtomIonizationEnergy'),
        G('AtomStateLandeFactorRef'), G('AtomStateLandeFactor'))

        if (G('AtomStateParity') or G('AtomStateTotalAngMom')):
            yield '<AtomicQuantumNumbers><Parity>%s</Parity>' \
                  '<TotalAngularMomentum>%s</TotalAngularMomentum>' \
                  '</AtomicQuantumNumbers>' % (G('AtomStateParity'),
                                               G('AtomStateTotalAngMom'))

        # call the function that returns the term part
        yield XsamsAtomTerm(AtomState,G)
        yield """</AtomicState>
</IonState>
</Isotope>
</Atom>"""
        #end of loop
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

    # nothing to see here if the data has no molecular states
    if not MoleStates: return

    # if MoleQNs was passed as None or not passed at all,
    # it is effectively an empty list:
    if MoleQNs is None:
        MoleQNs = []

    # rearrange QN-Lists into dictionary with stateID as key
    QNList={}
    for MolQN in MoleQNs:
       G=lambda name: GetValue(name,MolQN=MolQN)
       if QNList.has_key(G("MolQnStateID")):
          QNList[G("MolQnStateID")].append(MolQN)
       else:
          QNList[G("MolQnStateID")]=[MolQN]

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
        thisInchiKey = G("InchiKey")

        for MolState in MoleStates:
            G = lambda name: GetValue(name, MolState=MolState)
            if G("InchiKey") != thisInchiKey:
                break
	        
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
              for MolQN in QNList[G("MolecularStateStateID")]:
                G=lambda name: GetValue(name, MolQN=MolQN)
                yield """
    <%s:%s """ % (G("MolQnCase"), G("MolQnLabel"))
                if G("MolQnSpinRef"):
                    yield """nuclearSpinRef="%s" """ % (G("MolQnSpinRef"))
                if G("MolQnAttribute"):
                    yield G("MolQnAttribute")
                yield """> %s </%s:%s>""" \
                    % (G("MolQnValue"),G("MolQnCase"),G("MolQnLabel") )

            yield '</MolecularState>'
        yield '</Molecule>'
    yield '</Molecules>'

def XsamsMCSBuild(Moldesc):
    """
    Generator for the MolecularChemicalSpecies
    """
    G=lambda name: GetValue(name,Moldesc=Moldesc)
    yield '<MolecularChemicalSpecies>\n'
    yield """
    <OrdinaryStructuralFormula>%s</OrdinaryStructuralFormula>
    <StoichiometricFormula>%s</StoichiometricFormula>
    <ChemicalName>%s</ChemicalName>
    <StableMolecularProperties>
    <MolecularWeight>
        <Value units="%s">%s</Value>
    </MolecularWeight>
    </StableMolecularProperties>
    <Comment>%s</Comment>
    """%(G("MolecularSpeciesOrdinaryStructuralFormula"),
    G("MolecularSpeciesStoichiometrcFormula"),
    G("MolecularSpeciesChemicalName"),
    G("MolecularSpeciesMolecularWeightUnits"),
    G("MolecularSpeciesMolecularWeight"),
    G("MolecularSpeciesComment"))
    
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


def XsamsMolecs(Molecules):
    if not Molecules: return
    yield '<Molecules>\n'
    for Moldesc in Molecules:
        #G=lambda name: GetValue(name,Moldesc=Moldesc)
        yield '<Molecule>\n'
        for MCS in XsamsMCSBuild(Moldesc):
            yield MCS
            
        #Build all levels for element:
#        for syme in Moldesc.symmels.all():
#            for et in syme.etables.all():
#                yield XsamsMSBuild(et)
        
        
        #for Molstate in G('MolecularStates'):
        #for elev in Moldesc.symmel.all().levels.select_related.all():
        #    yield XsamsMSBuild(elev)
        #    yield molst#yield XsamsMSBuild(Molstate)
        yield '</Molecule>\n'
    yield '</Molecules>\n'
    
def XsamsRadTranBroadening(typedescr,ref,params):
    """
    helper function for line broadening below
    """

    result='<BroadeningProcess sourceRef="B%s"><BroadeningSpecies>'%ref
    result+='<Comments>%s</Comments>'%typedescr
    result+='<LineshapeParameter>'
    for par in params:
        result+='<Value>%s</Value>'%par

    result+='</LineshapeParameter>'
    result+='</BroadeningSpecies></BroadeningProcess>'
    return result

def XsamsRadTrans(RadTrans):
    """
    Generator for the XSAMS radiative transitions.
    """

    # nothing to do, if data has no radiative transitions
    if not RadTrans: return

    yield '<Radiative>'
    for RadTran in RadTrans:
        G=lambda name: GetValue(name,RadTran=RadTran)
        yield """
<RadiativeTransition methodRef="M%s">
<Comments>%s</Comments>
<EnergyWavelength>"""%(G('RadTransMethodRef'),G('RadTransComments'))

        # pre-fetch the values that decide which branch to enter
        WaveLenE=G('RadTransWavelengthExperimentalValue')
        WaveLenT=G('RadTransWavelengthTheoreticalValue')
        WaveLenR=G('RadTransWavelengthRitzValue')
        WaveNumE=G('RadTransWavenumberExperimentalValue')
        WaveNumT=G('RadTransWavenumberTheoreticalValue')
        WaveNumR=G('RadTransWavenumberRitzValue')
        FreqE=G('RadTransFrequencyExperimentalValue')
        FreqT=G('RadTransFrequencyTheoreticalValue')
        FreqR=G('RadTransFrequencyRitzValue')

        if WaveLenE: yield """<Wavelength><Experimental sourceRef="B%s">
<Comments>%s</Comments><Value units="%s">%s</Value><Accuracy>%s</Accuracy>
</Experimental></Wavelength>"""%(G('RadTransWavelengthExperimentalSourceRef'),
                                 G('RadTransWavelengthExperimentalComments'),
                                 G('RadTransWavelengthExperimentalUnits'),
                                 WaveLenE,
                                 G('RadTransWavelengthExperimentalAccuracy'))

        if WaveLenT: yield """<Wavelength><Theoretical sourceRef="B%s">
<Comments>%s</Comments><Value units="%s">%s</Value><Accuracy>%s</Accuracy>
</Theoretical></Wavelength>"""%(G('RadTransWavelengthTheoreticalSourceRef'),
                                G('RadTransWavelengthTheoreticalComments'),
                                G('RadTransWavelengthTheoreticalUnits'),
                                WaveLenT,
                                G('RadTransWavelengthTheoreticalAccuracy'))

        if WaveLenR: yield """<Wavelength><Ritz sourceRef="B%s">
<Comments>%s</Comments><Value units="%s">%s</Value><Accuracy>%s</Accuracy>
</Ritz></Wavelength>"""%(G('RadTransWavelengthRitzSourceRef'),
                         G('RadTransWavelengthRitzComments'),
                         G('RadTransWavelengthRitzUnits'),
                         WaveLenR,
                         G('RadTransWavelengthRitzAccuracy'))

        if WaveNumE: yield """<Wavenumber><Experimental sourceRef="B%s">
<Comments>%s</Comments><Value units="%s">%s</Value><Accuracy>%s</Accuracy>
</Experimental></Wavenumber>"""%(G('RadTransWavenumberExperimentalSourceRef'),
                                 G('RadTransWavenumberExperimentalComments'),
                                 G('RadTransWavenumberExperimentalUnits'),
                                 WaveNumE,
                                 G('RadTransWavenumberExperimentalAccuracy'))

        if WaveNumT: yield """<Wavenumber><Theoretical sourceRef="B%s">
<Comments>%s</Comments><Value units="%s">%s</Value><Accuracy>%s</Accuracy>
</Theoretical></Wavenumber>"""%(G('RadTransWavenumberTheoreticalSourceRef'),
                                G('RadTransWavenumberTheoreticalComments'),
                                G('RadTransWavenumberTheoreticalUnits'),
                                WaveNumT,
                                G('RadTransWavenumberTheoreticalAccuracy'))

        if WaveNumR: yield """<Wavenumber><Ritz sourceRef="B%s">
<Comments>%s</Comments><Value units="%s">%s</Value><Accuracy>%s</Accuracy>
</Ritz></Wavenumber>"""%(G('RadTransWavenumberRitzSourceRef'),
                         G('RadTransWavenumberRitzComments'),
                         G('RadTransWavenumberRitzUnits'),
                         WaveNumR,
                         G('RadTransWavenumberRitzAccuracy'))

        if FreqE: yield """<Frequency><Experimental sourceRef="B%s">
<Comments>%s</Comments><Value units="%s">%s</Value><Accuracy>%s</Accuracy>
</Experimental></Frequency>"""%(G('RadTransFrequencyExperimentalSourceRef'),
                                 G('RadTransFrequencyExperimentalComments'),
                                 G('RadTransFrequencyExperimentalUnits'),
                                 FreqE,
                                 G('RadTransFrequencyExperimentalAccuracy'))

        if FreqT: yield """<Frequency><Theoretical sourceRef="B%s">
<Comments>%s</Comments><Value units="%s">%s</Value><Accuracy>%s</Accuracy>
</Theoretical></Frequency>"""%(G('RadTransFrequencyTheoreticalSourceRef'),
                                G('RadTransFrequencyTheoreticalComments'),
                                G('RadTransFrequencyTheoreticalUnits'),
                                FreqT,
                                G('RadTransFrequencyTheoreticalAccuracy'))

        if FreqR: yield """<Frequency><Ritz sourceRef="B%s">
<Comments>%s</Comments><Value units="%s">%s</Value><Accuracy>%s</Accuracy>
</Ritz></Frequency>"""%(G('RadTransFrequencyRitzSourceRef'),
                         G('RadTransFrequencyRitzComments'),
                         G('RadTransFrequencyRitzUnits'),
                         WaveNumR,
                         G('RadTransFrequencyRitzAccuracy'))

        yield '</EnergyWavelength>'

        if G('RadTransEffLande'): yield """<EffLandeFactor><Value sourceRef="B%s">%s</Value></EffLandeFactor>"""%(G('RadTransEffLandeRef'),G('RadTransEffLande'))

	yield '<Broadening>'
        if G('RadTransBroadRadGammaLog'): yield XsamsRadTranBroadening('log10 of the radiative damping constant in radians per second',G('RadTransBroadRadRef'),[G('RadTransBroadRadGammaLog')])
        if G('RadTransBroadStarkGammaLog'): yield XsamsRadTranBroadening('log10 quadratic Stark damping constant computed for 10000 K per one charged particle',G('RadTransBroadStarkRef'),[G('RadTransBroadStarkGammaLog')])
        if G('RadTransBroadWaalsGammaLog'): yield XsamsRadTranBroadening('log10 van der Waals damping constant for 10000 K and per one neutral particle',G('RadTransBroadWaalsRef'),[G('RadTransBroadWaalsGammaLog')])
        if G('RadTransBroadWaalsAlpha'): yield XsamsRadTranBroadening('Anstee-Barklem fit to the van der Waals damping constants alpha and sigma',G('RadTransBroadWaalsRef'),[G('RadTransBroadWaalsAlpha'),G('RadTransBroadWaalsSigma')])
	yield '</Broadening>'
        
        if G('RadTransInitialStateRef'): yield '<InitialStateRef>S%s</InitialStateRef>'%G('RadTransInitialStateRef')
        if G('RadTransFinalStateRef'): yield '<FinalStateRef>S%s</FinalStateRef>'%G('RadTransFinalStateRef')
        if G('RadTransProbabilityLog10WeightedOscillatorStrengthValue'): yield """<Probability>
<Log10WeightedOscillatorStregnth sourceRef="B%s"><Value units="unitless">%s</Value><Accuracy>%s</Accuracy></Log10WeightedOscillatorStregnth>
</Probability>
"""%(G('RadTransProbabilityLog10WeightedOscillatorStrengthSourceRef'),G('RadTransProbabilityLog10WeightedOscillatorStrengthValue'),G('RadTransProbabilityLog10WeightedOscillatorStrengthAccuracy'))
        yield '</RadiativeTransition>'
        # loop ends
    yield '</Radiative>'


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


def Xsams(Sources=None, AtomStates=None, MoleStates=None, CollTrans=None,
          RadTrans=None, Methods=None, MoleQNs=None, Molecules=None,
          HeaderInfo=None):
    """
    The main generator function of XSAMS. This one calles all the
    sub-generators above. It takes the query sets that the node's
    setupResult() has constructed as arguments with given names.
    This function is to be passed to the HTTP-respose object directly
    and not to be looped over beforehand.

    """

    yield """<?xml version="1.0" encoding="UTF-8"?>
<XSAMSData xsi:noNamespaceSchemaLocation="http://www-amdis.iaea.org/xsams/schema/xsams-0.1.xsd"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xmlns:dcs="http://www.ucl.ac.uk/~ucapch0/dcs"  
 xmlns:hundb="http://www.ucl.ac.uk/~ucapch0/hundb"  
 xmlns:ltcs="http://www.ucl.ac.uk/~ucapch0/ltcs"  
 xmlns:nltcs="http://www.ucl.ac.uk/~ucapch0/nltcs"  
 xmlns:stcs="http://www.ucl.ac.uk/~ucapch0/stcs"  
 xmlns:lp="http://www.ucl.ac.uk/~ucapch0/lp"  
 xmlns:nlp="http://www.ucl.ac.uk/~ucapch0/nlp"  
 xmlns:lmp="http://www.ucl.ac.uk/~ucapch0/lmp"  >
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

    LOG('Writing Sources.')
    for Source in XsamsSources(Sources): yield Source

    LOG('Writing Methods.')
    for Method in XsamsMethods(Methods): yield Method
    
    LOG('Writing States.')
    yield '<States>\n'
    for AtomState in XsamsAtomStates(AtomStates): yield AtomState
    for MolState in XsamsMolStates(Molecules, MoleStates, MoleQNs):
        yield MolState
    yield '</States>\n'

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
