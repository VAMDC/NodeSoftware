from django.shortcuts import render_to_response,get_object_or_404
from django.db.models import Q
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


from DjVALD.vald.models import Transition,State,Source,Species

from DjVAMDC.tapservice.views import *

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



def sources2xsams(sources):
    for source in sources:
        yield """<Source sourceID="S-%d">
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

def stateterm2xsams(state):
    
    if not (state.term and state.coupling): return ''
    
    result='<AtomicComposition><Component><Configuration>'
    result+='<ConfigurationLabel>%s</ConfigurationLabel></Configuration>\n'%state.term
    result+='<Term><Comments>Term reference: S-%s</Comments>'%state.level_ref
    if state.coupling == "LS": 
        result+='<LS>'
        if state.l: '<L><Value>%f</Value></L>'%state.l
        if state.s: '<S>%f</S>'%state.s
        result+='</LS>'
        
    elif state.coupling == "JK": 
        result+='<jK>'
        if state.s2: '<j>%f</j>'%state.s2
        if state.k: '<K> %f</K>'%state.k
        result+='</jK>'
        
    elif state.coupling == "JJ":
        result+='<J1J2>'
        if state.j1: '<j>%f</j>'%state.j1
        if state.j2: '<j>%f</j>'%state.j2
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
<AtomicState stateID="S-%s"><Description>%s</Description>
<AtomicNumericalData>
<StateEnergy><Value units="1/cm" sourceRef="S-%d">%f</Value></StateEnergy>
<IonizationEnergy><Value units="eV">%f</Value></IonizationEnergy>
<LandeFactor><Value units="unitless" sourceRef="S-%d">%f</Value><LandeFactor/>
</AtomicNumericalData>
"""%( state.species.atomic , state.species.name , mass , state.species.ion , state.id , state.id , state.energy_ref , state.energy , state.species.ionen , state.lande_ref , state.lande)

        if (state.p or state.j):
            yield "<AtomicQuantumNumbers>"
            if state.p: '<Parity>%s</Parity>'%('odd' if state.p%2 else 'even')
            if state.j: '<TotalAngularMomentum>%f</TotalAngularMomentum>'%state.j
            yield "</AtomicQuantumNumbers>"

        yield stateterm2xsams(state)
        yield """</AtomicState>
</IonState>
</Isotope>
</Atom>"""

def transitions2xsams(transitions):
    for trans in transitions:
        yield """
<RadiativeTransition methodRef="MEXP">
<Comments>Effective Lande factor and broadening gammas: 
lande_eff: %f (Ref S-%d)
gamma_rad: %f (Ref S-%d)
gamma_stark: %f (Ref S-%d)
gamma_waals: %f (Ref S-%d)
</Comments>
<EnergyWavelength>
<Wavelength>
<Experimental sourceRef="S-%d">
<Comments>Wavelength in vaccuum (first) and air.</Comments>
<Value units="1/cm">%f</Value>
<Value units="1/cm">%f</Value>
<Accuracy>Flag: %s, Value: %s</Accuracy>
</Experimental>
</Wavelength>
</EnergyWavelength>"""%( trans.landeff , trans.lande_ref , trans.gammarad , trans.gammarad_ref , trans.gammastark , trans.gammastark_ref , trans.gammawaals , trans.gammawaals_ref , trans.wave_ref , trans.vacwave , trans.airwave , trans.acflag , trans.accur )

        if trans.upstateid: yield '<InitialStateRef>S-%s</InitialStateRef>'%trans.upstateid
        if trans.lostateid: yield '<FinalStateRef>S-%s</FinalStateRef>'%trans.lostateid
        if trans.loggf: yield """<Probability>
<Log10WeightedOscillatorStrength sourceRef="S-%d"><Value units="unitless">%f</Value></Log10WeightedOscillatorStrength>
</Probability>
</RadiativeTransition>"""%(trans.loggf_ref,trans.loggf)


def vald2xsams(transitions,states,sources):
    yield """<?xml version="1.0" encoding="UTF-8"?>
<XSAMSData xsi:noNamespaceSchemaLocation="http://www-amdis.iaea.org/xsams/schema/xsams-0.1.xsd"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<Sources>"""
    for source in sources2xsams(sources): yield source
    yield """</Sources>
<Methods>
<Method methodID="MEXP">
<Category>measured</Category>
<Description />
</Method>
</Methods>

<States>
<Atoms>"""
    for state in states2xsams(states): yield state
    yield '</Atoms></States><Processes><Radiative>'
    for trans in transitions2xsams(transitions): yield trans
    yield '</Radiative><Processes/>\n</XSAMSData>\n'



def sync(request):
    tap=TAPQUERY(request.REQUEST)
    if not tap.isvalid:
        # return http error
        pass

    qtup=parseSQL(tap.query)
    
    ts=time()

    transs = Transition.objects.filter(*qtup).order_by('vacwave')
    #print '%d transitions set up'%len(transs),time()-ts
    
    sources = getVALDsources(transs)
    #print '%d sources set up'%len(sources),time()-ts
       
    states = getVALDstates(transs)
    #print '%d states set up'%len(states),time()-ts
    
    #response = renderedResponse(transs,states,sources,tap)
    response=HttpResponse(vald2xsams(transs,states,sources),mimetype='application/xml')
    response['Content-Disposition'] = 'attachment; filename=%s.%s'%(tap.queryid,tap.format)
    return response
     
## LEGACY below


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
    
