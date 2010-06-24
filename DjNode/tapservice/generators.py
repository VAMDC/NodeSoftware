# -*- coding: utf-8 -*-

import sys
def LOG(s):
    print >> sys.stderr, s


# Get the node-specific pacakge!
from django.conf import settings
from django.utils.importlib import import_module

from xml.sax.saxutils import quoteattr


NODEPKG=import_module(settings.NODEPKG+'.views')

isiterable = lambda obj: hasattr(obj, '__iter__')

def GetValue(name,**kwargs):
    """
    the function that gets a value out of the query set, using the global name
    and the node-specific dictionary.
    """
    try: name=NODEPKG.RETURNABLES[name]
    except: return '' # The value is not in the dictionary for the node.
                      # This is fine
    if not name: return ''

    try: value=eval(name) # this works, if the dict-value is named correctly as the query-set attribute
    except Exception,e: 
        LOG(e)
        LOG(name)
        value=name  # this catches the case where the dict-value is a string or mistyped.
    return value
    

def XsamsSources(Sources):
    if not Sources: return
    yield '<Sources>'
    for Source in Sources:
        G=lambda name: GetValue(name,Source=Source)
        yield '<Source sourceID="B%s"><Authors>\n'%G('SourceID') 
        authornames=G('SourceAuthorName')
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

</Source>\n"""%( G('SourceTitle'), G('SourceCategory'), G('SourceYear'), G('SourceName'), G('SourceVolume'), G('SourcePageBegin'), G('SourcePageEnd'), quoteattr(G('SourceURI')) )

    yield '</Sources>\n'

def XsamsAtomTerm(AtomState,G):
    #pre-fetch the ones that will be tested for below
    coupling=G('AtomStateCoupling')
    l=G('AtomStateL')
    s=G('AtomStateS')
    k=G('AtomStateK')
    s2=G('AtomStateS2')
    j1=G('AtomStateJ1')
    j2=G('AtomStateJ2')
    
    result='<AtomicComposition>\n<Comments>Term reference: B%s</Comments>\n'%G('AtomStateCompositionComments')
    result+='<Component><Configuration><ConfigurationLabel>%s</ConfigurationLabel></Configuration>\n'%G('AtomStateConfigurationLabel')
    result+='<Term>'

def XsamsAtomTerm(state):    
    result='<AtomicComposition>\n<Comments>Term reference: B%s</Comments>\n'%state.level_ref
    result+='<Component><Configuration><ConfigurationLabel>%s</ConfigurationLabel></Configuration>\n'%state.term.replace('<','').replace('>','')
    result+='<Term>'
    if state.coupling == "LS" and state.l and state.s: 
        result+='<LS>'
        if state.l: result+='<L><Value>%d</Value></L>'%state.l
        if state.s: result+='<S>%.1f</S>'%state.s
        result+='</LS>'
        
    elif state.coupling == "JK" and state.s2 and state.k: 
        result+='<jK>'
        if state.s2: result+='<j>%s</j>'%state.s2
        if state.k: result+='<K> %s</K>'%state.k
        result+='</jK>'
        
    elif state.coupling == "JJ" and state.j1 and state.j2:
        result+='<J1J2>'
        if state.j1: result+='<j>%s</j>'%state.j1
        if state.j2: result+='<j>%s</j>'%state.j2
        result+='</J1J2>'
        
    result+='</Term></Component></AtomicComposition>'
    return result

def parityLabel(parity):
   if partity % 2:
      return 'odd'
   else:
      return 'even'

def XsamsAtomStates(AtomStates,VD):
    if not AtomStates: return
    yield '<Atoms>'
    for AtomState in AtomStates:
        G=lambda name: GetValue(name,AtomState=AtomState)
        mass = int(round(Atomtate.species.mass))
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
<StateEnergy sourceRef="B%s"><Value units="1/cm">%s</Value></StateEnergy>
<IonizationEnergy><Value units="eV">%s</Value></IonizationEnergy>
<LandeFactor sourceRef="B%s"><Value units="unitless">%s</Value></LandeFactor>
</AtomicNumericalData>
"""%( G(''), G(''), G(''), G(''), G(''), G(''), G(''), G(''), G(''), G(''), G(''))

        if (state.p or state.j):
            yield "<AtomicQuantumNumbers>"
            if state.p: '<Parity>%s</Parity>'%parityLabel(state.p)
            if state.j: '<TotalAngularMomentum>%s</TotalAngularMomentum>'%state.j
            yield "</AtomicQuantumNumbers>"

        yield XsamsAtomTerm(state)
        yield """</AtomicState>
</IonState>
</Isotope>
</Atom>"""

    yield '</Atoms>'

def XsamsMolStates(MolStates,VD):
    if not MolStates: return
    yield '<Molecules>'
    for MolState in MolStates:
        G=lambda name: GetValue(name,MolState=MolState)
        yield """
<Molecule>
<MolecularChemicalSpecies>
<OrdinaryStructuralFormula>%s</OrdinaryStructuralFormula>
<StoichiometricFormula>%s</StoichiometricFormula>
<ChemicalName>%s</ChemicalName>
</MolecularChemicalSpecies>
<MolecularState stateID="S%s">
<Description>%s</Description>
<MolecularStateCharacterisation>
<StateEnergy energyOrigin="%s">
<Value units="%s">%s</Value>
</StateEnergy>
<TotalStatisticalWeight>%s</TotalStatisticalWeight>
</MolecularStateCharacterisation>
"""% (G("MolecularSpeciesOrdinaryStructuralFormula"),
      G("MolecularSpeciesStoichiometrcFormula"),
      G("MolecularSpeciesChemicalName"),
      G("MolecularStateStateID"),
      G("MolecularStateDescription"),
      G("MolecularStateEnergyOrigin"),
      G("MolecularStateEnergyUnit"),
      G("MolecularStateEnergyValue"),
      G("MolecularStateCharacTotalStatisticalWeight"))

        yield """</MolecularState>
</Molecule> """
    yield '</Molecules>'

#This thing yields MolecularChemicalSpecies
def XsamsMCSBuild(Moldesc):
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

def XsamsMSBuild(Molstate):
    G=lambda name: GetValue(name,Molstate=Molstate)
    ret="""<MolecularState stateID="S%s">
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
        for syme in Moldesc.symmels.all():
            for et in syme.etables.all():
                yield XsamsMSBuild(et)
        
        
        #for Molstate in G('MolecularStates'):
        #for elev in Moldesc.symmel.all().levels.select_related.all():
        #    yield XsamsMSBuild(elev)
        #    yield molst#yield XsamsMSBuild(Molstate)
        yield '</Molecule>\n'
    yield '</Molecules>\n'
    


                               

def XsamsRadTrans(RadTrans):
    if not RadTrans: return
    yield '<Radiative>'
    for RadTran in RadTrans:
        yield """
<RadiativeTransition methodRef="MOBS">
<Comments>Effective Lande factor and broadening gammas: 
lande_eff: %s (Ref B%d)
gamma_rad: %s (Ref B%d)
gamma_stark: %s (Ref B%d)
gamma_waals: %s (Ref B%d)
air wavelength: %s (Ref B%d)
</Comments>
<EnergyWavelength>
<Wavelength><Experimental sourceRef="B%d">
<Comments>Wavelength in vaccuum. For air see the comment field.</Comments><Value units="1/cm">%s</Value><Accuracy>Flag: %s, Value: %s</Accuracy>
</Experimental></Wavelength></EnergyWavelength>"""%( RadTran.landeff , RadTran.lande_ref , RadTran.gammarad , RadTran.gammarad_ref , RadTran.gammastark , RadTran.gammastark_ref , RadTran.gammawaals , RadTran.gammawaals_ref , RadTran.airwave, RadTran.wave_ref, RadTran.wave_ref , RadTran.vacwave , RadTran.acflag , RadTran.accur)

        if RadTran.upstateid: yield '<InitialStateRef>S%s</InitialStateRef>'%RadTran.upstate.id
        if RadTran.lostateid: yield '<FinalStateRef>S%s</FinalStateRef>'%RadTran.lostate.id
        if RadTran.loggf: yield """<Probability>
<Log10WeightedOscillatorStregnth sourceRef="B%d"><Value units="unitless">%s</Value></Log10WeightedOscillatorStregnth>
</Probability>
</RadiativeTransition>"""%(RadTran.loggf_ref,RadTran.loggf)

    yield '<Radiative>'


def XsamsMethods(Methods):
    if not Methods: return
    yield '<Methods>\n'
    for Method in Methods:
        yield """<Method methodID="%s">
<Category>%s</Category>
<Description>%s</Description>
</Method>
"""%(Method.id,Method.category,Method.description)
    yield '</Methods>\n'

def Xsams(Sources=None,AtomStates=None,MoleStates=None,CollTrans=None,RadTrans=None,Methods=None):
    yield """<?xml version="1.0" encoding="UTF-8"?>
<XSAMSData xsi:noNamespaceSchemaLocation="http://www-amdis.iaea.org/xsams/schema/xsams-0.1.xsd"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
"""
    for Source in XsamsSources(Sources): yield Source
#    for Method in XsamsMethods(Methods): yield Method
    
    yield '<States>\n'
    for AtomState in XsamsAtomStates(AtomStates): yield AtomState
    for MolState in XsamsMolecs(MoleStates): yield MolState
    yield '</States>\n'
    yield '<Processes>\n'
#    for RadTrans in XsamsRadTrans(RadTrans): yield RadTrans
    #for CollTrans in XsamsCollTrans(CollTrans): yield CollTrans
    yield '</Processes>\n'
    yield '</XSAMSData>\n'








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
        yield  '<TR><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD></TR>\n'%(trans.airwave, trans.vacwave, trans.loggf, trans.landeff , trans.gammarad ,trans.gammastark , trans.gammawaals , xmlEscape(trans.upstateid), xmlEscape(trans.lostateid))
        
    yield """</TABLEDATA></DATA></TABLE>"""


# Returns an XML-escaped version of a given string. The &, < and > characters are escaped.
def xmlEscape(s):
    if s:
        return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    else:
        return None


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
