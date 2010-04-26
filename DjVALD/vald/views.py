from django.shortcuts import render_to_response,get_object_or_404
from django.db.models import Q
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


from DjVALD.vald.models import Transition,State,Source,Species
from DjVAMDC.tapservice.views import *


VALD_DICT={'1':'species.atomic',
           '2':'species.ion',
           '3':'transitions.vacwave',
           '4':'transitions.airwave',
           '5':'transitions.loggf',
           '6':'state.energy',
           '7':'state.J',
           }


from base64 import b64encode as b64
def enc(s):
    return b64(s).replace('=','')

def index(request):
    c=RequestContext(request,{})
    return render_to_response('vald/index.html', c)


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
    result+='<Component><Configuration><ConfigurationLabel>%s</ConfigurationLabel></Configuration>\n'%state.term
    result+='<Term>'
    if state.coupling == "LS" and state.l and state.s: 
        result+='<LS>'
        if state.l: result+='<L><Value>%d</Value></L>'%state.l
        if state.s: result+='<S>%.1f</S>'%state.s
        result+='</LS>'
        
    elif state.coupling == "JK" and state.s2 and state.k: 
        result+='<jK>'
        if state.s2: result+='<j>%f</j>'%state.s2
        if state.k: result+='<K> %f</K>'%state.k
        result+='</jK>'
        
    elif state.coupling == "JJ" and state.j1 and state.j2:
        result+='<J1J2>'
        if state.j1: result+='<j>%f</j>'%state.j1
        if state.j2: result+='<j>%f</j>'%state.j2
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
<StateEnergy sourceRef="B%d"><Value units="1/cm">%f</Value></StateEnergy>
<IonizationEnergy><Value units="eV">%f</Value></IonizationEnergy>
<LandeFactor sourceRef="B%d"><Value units="unitless">%f</Value></LandeFactor>
</AtomicNumericalData>
"""%( state.species.atomic , state.species.name , mass , state.species.ion , enc(state.id) , state.id , state.energy_ref , state.energy , state.species.ionen , state.lande_ref , state.lande)

        if (state.p or state.j):
            yield "<AtomicQuantumNumbers>"
            if state.p: '<Parity>%s</Parity>'%('odd' if state.p%2 else 'even')
            if state.j: '<TotalAngularMomentum>%f</TotalAngularMomentum>'%state.j
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
lande_eff: %f (Ref B%d)
gamma_rad: %f (Ref B%d)
gamma_stark: %f (Ref B%d)
gamma_waals: %f (Ref B%d)
air wavelength: %f (Ref B%d)
</Comments>
<EnergyWavelength>
<Wavelength><Experimental sourceRef="B%d">
<Comments>Wavelength in vaccuum. For air see the comment field.</Comments><Value units="1/cm">%f</Value><Accuracy>Flag: %s, Value: %s</Accuracy>
</Experimental></Wavelength></EnergyWavelength>"""%( trans.landeff , trans.lande_ref , trans.gammarad , trans.gammarad_ref , trans.gammastark , trans.gammastark_ref , trans.gammawaals , trans.gammawaals_ref , trans.airwave, trans.wave_ref, trans.wave_ref , trans.vacwave , trans.acflag , trans.accur)

        if trans.upstateid: yield '<InitialStateRef>S%s</InitialStateRef>'%enc(trans.upstateid)
        if trans.lostateid: yield '<FinalStateRef>S%s</FinalStateRef>'%enc(trans.lostateid)
        if trans.loggf: yield """<Probability>
<Log10WeightedOscillatorStregnth sourceRef="B%d"><Value units="unitless">%f</Value></Log10WeightedOscillatorStregnth>
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
      <GROUP ID="">
        <PARAM datatype="char" arraysize="*" ucd="pos.frame" name="cooframe"
             utype="stc:AstroCoords.coord_system_id" value="UTC-ICRS-TOPO" />
        <FIELDref ref="col1"/>
        <FIELDref ref="col2"/>
      </GROUP>
      <FIELD name="RA"   ID="col1" ucd="pos.eq.ra;meta.main" ref="J2000" 
             utype="stc:AstroCoords.Position2D.Value2.C1"
             datatype="float" width="6" precision="2" unit="deg"/>
      <DATA>
        <TABLEDATA>"""

    for state in states:
        yield  '<TR><TD>010.68</TD><TD>+41.27</TD><TD>N  224</TD><TD>-297</TD><TD>5</TD><TD>0.7</TD></TR>'
        
    yield """</TABLEDATA></DATA></TABLE>"""

def valdtransitions2votable(transs):
    yield """<TABLE name="transitions" ID="transitions">
      <DESCRIPTION>The transitions</DESCRIPTION>
      <FIELD name="wavelength in vacuum" ID="vacwave" datatype="float" unit="cm-1"/>
      <FIELD name="wavelength in air" ID="airwave" datatype="float" unit="cm-1"/>
      <FIELD name="log(g*f)"   ID="loggf" datatype="float"/>
      <FIELD name="effective lande factor" ID="landeff" datatype="float"/>
      <FIELD name="radiative gamma" ID="gammarad" datatype="float"/>
      <FIELD name="stark gamma" ID="gammastark" datatype="float"/>
      <FIELD name="waals gamma" ID="gammawaals" datatype="float"/>
      <FIELD name="upper state id" ID="upstateid" datatype="char" arraysize="*"/>
      <FIELD name="lower state id" ID="lostateid" datatype="char" arraysize="*"/>
      <DATA>
        <TABLEDATA>"""

    for trans in transs:
        yield  '<TR><TD>%f</TD><TD>%f</TD><TD>%f</TD><TD>%f</TD><TD>%f</TD><TD>%f</TD><TD>%f</TD><TD>%s</TD><TD>%s</TD></TR>\n'%( trans.vacwave , trans.airwave, trans.loggf, trans.landeff , trans.gammarad ,trans.gammastark , trans.gammawaals , trans.upstateid, trans.lostateid)
        
    yield """</TABLEDATA></DATA></TABLE>"""

def vald2votable(transitions,states,sources,query):
    yield """<?xml version="1.0"?>
<VOTABLE version="1.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xmlns="http://www.ivoa.net/xml/VOTable/v1.2" 
 xmlns:stc="http://www.ivoa.net/xml/STC/v1.30" >
  <RESOURCE name="queryresults">
    <DESCRIPTION>
    </DESCRIPTION>
    <LINK></LINK>
    
"""
    #yield valdsources2votable(sources):
    #yield valdstates2votable(states):
    for trans in valdtransitions2votable(transitions):
        yield trans
    yield """
</RESOURCE>
</VOTABLE>
"""




###########################################################

def setupGenerator(transs,states,sources,tap):
    if tap.format == 'xsams': return vald2xsams(transs,states,sources)
    if tap.format == 'votable': return vald2votable(transs,states,sources,tap)

def setupResults(tap):
    #ts=time()

    qtup=parseSQL(tap.query)
    transs = Transition.objects.filter(*qtup).order_by('vacwave')
    #print '%d transitions set up'%len(transs),time()-ts
    
    sources = getVALDsources(transs)
    #print '%d sources set up'%len(sources),time()-ts
       
    states = getVALDstates(transs)
    #print '%d states set up'%len(states),time()-ts
    
    return transs,states,sources
    
def sync(request):
    tap=TAPQUERY(request.REQUEST)
    if not tap.isvalid:
        # return http error
        pass

    transs,states,sources=setupResults(tap)
    generator=setupGenerator(transs,states,sources,tap)

    #response = renderedResponse(transs,states,sources,tap)
    response=HttpResponse(generator,mimetype='application/xml')
    response['Content-Disposition'] = 'attachment; filename=%s.%s'%(tap.queryid,tap.format)
    return response










#############################################################     
############### LEGACY below ################################
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



def RenderXSAMSmulti(format,transs,states,sources):
    # this turned out to be inefficient
    # due to large overhead of python threads
    n=int(transs.count()/3)
    trans1=transs[:n]
    trans2=transs[n:2*n]
    trans3=transs[2*n:]
    t1=loader.get_template('vald/valdxsams_p1.xml')
    t2=loader.get_template('vald/valdxsams_p2.xml')
    th1=RenderThread(t1,Context({'sources':sources,'states':states,}))
    th2=RenderThread(t2,Context({'transitions':trans1}))
    th3=RenderThread(t2,Context({'transitions':trans2}))
    th4=RenderThread(t2,Context({'transitions':trans3}))
    th1.start()
    th2.start()
    th3.start()
    th4.start()
    th1.join()
    th2.join()
    th3.join()
    th4.join()
    rend=th1.r + th2.r + th3.r + th4.r + u'\n</XSAMSData>'
    return rend

def RenderXSAMSsingle(format,transs,states,sources):
    c=Context({'transitions':transs,'sources':sources,'states':states,})
    t=loader.get_template('vald/valdxsams.xml')
    return t.render(c)


def MyRender(format,transs,states,sources):
    if format=='xsams':
        rend=RenderXSAMSsingle(format,transs,states,sources)
    elif format=='csv': 
        t=loader.get_template('vald/valdtable.csv')
        c=Context({'transitions':transs,'sources':sources,'states':states,})
        rend=t.render(c)
    else: 
        rend=''   
    return rend

def renderedResponse(transs,states,sources,tap):
    rendered=MyRender(tap.format,transs,states,sources)
    
    zbuf = StringIO()
    zfile = gzip.GzipFile(mode='wb', compresslevel=6, fileobj=zbuf)
    zfile.write(rendered)
    zfile.close()
    compressed_content = zbuf.getvalue()
    response = HttpResponse(compressed_content,mimetype='application/x-gzip')
    response['Content-Encoding'] = 'gzip'
    response['Content-Length'] = str(len(compressed_content))
    response['Content-Disposition'] = 'attachment; filename=%s.%s.gz'%(tap.queryid,tap.format)
    return response
    
