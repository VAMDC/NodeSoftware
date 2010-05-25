# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,get_object_or_404
from django.db.models import Q
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


from DjVALD.vald.models import Transition,State,Source,Species
from DjVAMDC.tapservice.views import *

from base64 import b64encode as b64
def enc(s):
    return b64(s).replace('=','')

CDMS_DICT={'1':'species__atomic',
           '2':'species__ion',
           '3':'vacwave',
           '4':'airwave',
           '5':'loggf',
           '6':'lostate__energy',
           '7':'lostate__J',
           }


def index(request):
    c=RequestContext(request,{})
    return render_to_response('vald/index.html', c)

######################## GENERATORS START HERE

def valdsources2xsams(sources):
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

def valdterm2xsams(state):
    
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


def valdstates2xsams(states):
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

        yield valdterm2xsams(state)
        yield """</AtomicState>
</IonState>
</Isotope>
</Atom>"""

def valdtransitions2xsams(transitions):
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

        if trans.upstateid: yield '<InitialStateRef>S%s</InitialStateRef>'%enc(trans.upstateid)
        if trans.lostateid: yield '<FinalStateRef>S%s</FinalStateRef>'%enc(trans.lostateid)
        if trans.loggf: yield """<Probability>
<Log10WeightedOscillatorStregnth sourceRef="B%d"><Value units="unitless">%s</Value></Log10WeightedOscillatorStregnth>
</Probability>
</RadiativeTransition>"""%(trans.loggf_ref,trans.loggf)


def vald2xsams(transitions,states,sources):
    yield """<?xml version="1.0" encoding="UTF-8"?>
<XSAMSData xsi:noNamespaceSchemaLocation="http://www-amdis.iaea.org/xsams/schema/xsams-0.1.xsd"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<Sources>"""
    for source in valdsources2xsams(sources): yield source
    yield """</Sources>
<Methods>
<Method methodID="MOBS">
<Category>observed</Category>
<Description />
</Method>
</Methods>

<States>
<Atoms>"""
    for state in valdstates2xsams(states): yield state
    yield '</Atoms></States><Processes><Radiative>'
    for trans in valdtransitions2xsams(transitions): yield trans
    yield '</Radiative></Processes >\n</XSAMSData>\n'

##########################################################
######## VO TABLE GENERATORS ####################
def valdsources2votable(sources):
    for source in sources:
        yield ''

def valdstates2votable(states):
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

def valdtransitions2votable(transs,count):
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

def vald2votable(transitions,states,sources,totalcount=None):
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
    for source in valdsources2votable(sources):
        yield source
    for state in valdstates2votable(states):
        yield state
    for trans in valdtransitions2votable(transitions,totalcount):
        yield trans
    yield """
</RESOURCE>
</VOTABLE>
"""
#######################

def valdtransitions2embedhtml(transs,count):
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

def vald2embedhtml(transitions,totalcount=None):
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
    for trans in valdtransitions2embedhtml(transitions,totalcount):
        yield trans
    yield """
</RESOURCE>
</VOTABLE>
"""

##############################
### GENERATORS END HERE
##############################
### VALD-specific helper functions start
##############################


def getVALDsources(transs):
    sids=set([])
    for trans in transs:
        s=set([trans.wave_ref,trans.loggf_ref,trans.lande_ref,trans.gammarad_ref,trans.gammastark_ref,trans.gammawaals_ref])
        sids=sids.union(s)
    return Source.objects.filter(pk__in=sids)

def getVALDstates(transs):
    #lostates=State.objects.filter(islowerstate_trans__in=transs)
    #histates=State.objects.filter(islowerstate_trans__in=transs)
    #states = lostates | histates
    q1,q2=Q(islowerstate_trans__in=transs),Q(islowerstate_trans__in=transs)
    return State.objects.filter(q1|q2).distinct()
    



def setupResults(tap,limit=0):
    if tap.lang=='vamdc':
        tap.query=tap.query%VALD_DICT
        print tap.query
        #transs = Transition.objects.extra(tables=['species','states'],where=[tap.query,'(transitions.lostate=states.id OR transitions.upstate=states.id)','transitions.species=species.id'],).order_by('airwave')
        qtup=vamdc2queryset(tap.query)
        transs = Transition.objects.filter(*qtup).order_by('airwave')
    else:
        qtup=parseSQL(tap.query)
        transs = Transition.objects.filter(*qtup).order_by('airwave')
    
    totalcount=transs.count()
    if limit :
        transs = transs[:limit]

    sources = getVALDsources(transs)
    states = getVALDstates(transs)
    if limit:
        return transs,states,sources,totalcount
    else:
        return transs,states,sources








#############################################################     
############### LEGACY code below ###########################
#############################################################





def getVALDstates2(transs):
    sids=set([])
    for trans in transs:
        sids.add(trans.lostate)
        sids.add(trans.upstate)
        
    states=[]
    sids.remove(None)
    for sid in sids:
        states.append(State.objects.get(pk=sid))
    return states

def getVALDsources1(transs):
    # this is REALLY slow
    waverefs=Q(iswaveref_trans__in=transs)
    landerefs=Q(islanderef_trans__in=transs)
    loggfrefs=Q(isloggfref_trans__in=transs)
    g1refs=Q(isgammaradref_trans__in=transs)
    g2refs=Q(isgammastarkref_trans__in=transs)
    g3refs=Q(isgammawaalsref_trans__in=transs)
    refQ= waverefs | landerefs | loggfrefs | g1refs | g2refs | g3refs
    sources=Source.objects.filter(refQ).distinct()
    return sources

def getVALDsources2(transs):
    #resonably fast
    waverefs=Q(iswaveref_trans__in=transs)
    landerefs=Q(islanderef_trans__in=transs)
    loggfrefs=Q(isloggfref_trans__in=transs)
    g1refs=Q(isgammaradref_trans__in=transs)
    g2refs=Q(isgammastarkref_trans__in=transs)
    g3refs=Q(isgammawaalsref_trans__in=transs)
    refQs=[waverefs, landerefs, loggfrefs, g1refs, g2refs, g3refs]
    sources=set()
    for q in refQs:
        refs=Source.objects.filter(q).distinct()
        for r in refs:
            sources.add(r)
    return sources

def getVALDsources3(transs):
    # slower than v2
    sids=set([])
    for trans in transs:
        s=set([trans.wave_ref,trans.loggf_ref,trans.lande_ref,trans.gammarad_ref,trans.gammastark_ref,trans.gammawaals_ref])
        sids=sids.union(s)
    return list(sids)

def getVALDsources4(transs):
    # as slow as v3
    sids=set([])
    for trans in transs:
        s=set([trans.wave_ref.id,trans.loggf_ref.id,trans.lande_ref.id,trans.gammarad_ref.id,trans.gammastark_ref.id,trans.gammawaals_ref.id])
        sids=sids.union(s)
    sources=[]
    for sid in sids:
        sources.append(Source.objects.get(pk=sid))
    return sources


