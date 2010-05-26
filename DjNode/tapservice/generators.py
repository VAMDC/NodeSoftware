from base64 import b64encode as b64
def enc(s):
    return b64(s).replace('=','')


def sources2xsams(sources):
    for source in sources:
        yield """<Source sourceID="B%d">
<Authors>
<Author>
<Name>%s, List type: %d, Source file: %s</Name>
</Author>
</Authors>
<Category>journal</Category>
<Year>2222</Year>
<SourceName>SomeJournal</SourceName>
<Volume>666</Volume>
<PageBegin>666</PageBegin>
</Source>"""%( source.id , source.srcdescr, source.listtype , source.srcfile )

def term2xsams(state):
    
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


def states2xsams(states):
    for state in states:
        mass = int(round(state.species.mass))
        yield """<Atom>
<ChemicalElement>
<NuclearCharge>%d</NuclearCharge>
<ElementSymbol>%s</ElementSymbol>
</ChemicalElement>
<Isotope>
<IsotopeParameters>
<MassNumber>%d</MassNumber>
</IsotopeParameters>
<IonState>
<IonCharge>%d</IonCharge>
<AtomicState stateID="S%s"><Description>%s</Description>
<AtomicNumericalData>
<StateEnergy sourceRef="B%d"><Value units="1/cm">%s</Value></StateEnergy>
<IonizationEnergy><Value units="eV">%s</Value></IonizationEnergy>
<LandeFactor sourceRef="B%d"><Value units="unitless">%s</Value></LandeFactor>
</AtomicNumericalData>
"""%( state.species.atomic , state.species.name , mass , state.species.ion , state.id , state.id , state.energy_ref , state.energy , state.species.ionen , state.lande_ref , state.lande)

        if (state.p or state.j):
            yield "<AtomicQuantumNumbers>"
            if state.p: '<Parity>%s</Parity>'%('odd' if state.p%2 else 'even')
            if state.j: '<TotalAngularMomentum>%s</TotalAngularMomentum>'%state.j
            yield "</AtomicQuantumNumbers>"

        yield term2xsams(state)
        yield """</AtomicState>
</IonState>
</Isotope>
</Atom>"""

def transitions2xsams(transitions):
    for trans in transitions:
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
</Experimental></Wavelength></EnergyWavelength>"""%( trans.landeff , trans.lande_ref , trans.gammarad , trans.gammarad_ref , trans.gammastark , trans.gammastark_ref , trans.gammawaals , trans.gammawaals_ref , trans.airwave, trans.wave_ref, trans.wave_ref , trans.vacwave , trans.acflag , trans.accur)

        if trans.upstateid: yield '<InitialStateRef>S%s</InitialStateRef>'%trans.upstate.id
        if trans.lostateid: yield '<FinalStateRef>S%s</FinalStateRef>'%trans.lostate.id
        if trans.loggf: yield """<Probability>
<Log10WeightedOscillatorStregnth sourceRef="B%d"><Value units="unitless">%s</Value></Log10WeightedOscillatorStregnth>
</Probability>
</RadiativeTransition>"""%(trans.loggf_ref,trans.loggf)


def xsams(transitions,states,sources):
    yield """<?xml version="1.0" encoding="UTF-8"?>
<XSAMSData xsi:noNamespaceSchemaLocation="http://www-amdis.iaea.org/xsams/schema/xsams-0.1.xsd"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<Sources>"""
    for source in sources2xsams(sources): yield source
    yield """</Sources>
<Methods>
<Method methodID="MOBS">
<Category>observed</Category>
<Description />
</Method>
</Methods>

<States>
<Atoms>"""
    for state in states2xsams(states): yield state
    yield '</Atoms></States><Processes><Radiative>'
    for trans in transitions2xsams(transitions): yield trans
    yield '</Radiative></Processes >\n</XSAMSData>\n'

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
    n=len(transs) if (type(transs)==type([])) else transs.count()
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
        yield  '<TR><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD></TR>\n'%(trans.airwave, trans.vacwave, trans.loggf, trans.landeff , trans.gammarad ,trans.gammastark , trans.gammawaals , trans.upstateid.replace('<','').replace('>','') if trans.upstateid else None, trans.lostateid.replace('<','').replace('>','') if trans.lostateid else None)
        
    yield """</TABLEDATA></DATA></TABLE>"""

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
    n=len(transs) if (type(transs)==type([])) else transs.count()
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
        yield  '<TR><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD></TR>\n'%(trans.species.atomic, trans.species.ion,trans.airwave, trans.loggf, #trans.landeff , trans.gammarad ,trans.gammastark , trans.gammawaals , 
trans.upstateid.replace('<','').replace('>','') if trans.upstateid else None, trans.lostateid.replace('<','').replace('>','') if trans.lostateid else None)
        
    yield """</TABLEDATA></DATA></TABLE>"""

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
