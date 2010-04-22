from DjVAMDC.node.views import *
from DjVAMDC.vald.models import Transition,State,Source,Species
import cStringIO, gzip

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
    result+='<ConfigurationLabel>%s</ConfigurationLabel></Configuration>'%state.term
    result+='<Term><Comments>Term reference: S-%s</Comments>'%state.level_ref
    if state.coupling == "LS": result+='<LS><L><Value>%f</Value></L><S>%f</S></LS>'%( state.l,state.s)
    elif state.coupling == "JK": result+='<jK><j>%f</j><K> %f</K></jK>'%(state.s2 ,state.k)
    elif state.coupling == "JJ": result+='<J1J2><j>%f<j></j>%f</j></J1J2>'%(state.j1, state.j2 )
    result+='</Term></Component></AtomicComposition>'
    return result


def states2xsams(states):
    for state in states:
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
<AtomicState stateID="S-%s">
<Description></Description>
<AtomicNumericalData>
<StateEnergy><Value units="1/cm" sourceRef="S-%d">%f</Value></StateEnergy>
<IonizationEnergy><Value units="eV">%f</Value></IonizationEnergy>
<LandeFactor><Value units="unitless" sourceRef="S-%d">%f</Value><LandeFactor/>
</AtomicNumericalData>
<AtomicQuantumNumbers>
<Parity>%s</Parity>
<TotalAngularMomentum>%f</TotalAngularMomentum>
</AtomicQuantumNumbers>"""%( state.species.atomic , state.species.name , round(state.species.mass) , state.species.ion , state.id , state.id , state.energy_ref , state.energy , state.species.ionen , state.lande_ref , state.lande , 'odd 'if (state.p%2) else 'even', state.j )

        yield stateterm2xsams(state)
        yield """</AtomicState>
</IonState>
</Isotope>
</Atom>"""

def transitions2xsams(transitions):
    for trans in transitions:
        yield """<RadiativeTransition methodRef="MEXP">
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
</EnergyWavelength>
<InitialStateRef>S-%s</InitialStateRef>
<FinalStateRef>S-%s</FinalStateRef>
<Probability>
<Log10WeightedOscillatorStrength sourceRef="S-%d"><Value units="unitless">%d</Value></Log10WeightedOscillatorStrength>
<Probability>
</RadiativeTransition>"""%( trans.landeff , trans.lande_ref , trans.gammarad , trans.gammarad_ref , trans.gammastark , trans.gammastark_ref , trans.gammawaals , trans.gammawaals_ref , trans.wave_ref , trans.vacwave , trans.airwave , trans.acflag , trans.accur , trans.upstate , trans.lostate , trans.loggf_ref , trans.loggf )

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
    #for state in states2xsams(transitions): yield state
    yield '</Atoms></States><Processes><Radiative>'
    for trans in transitions2xsams(transitions): yield trans
    yield '</Radiative><Processes/></XSAMSData>'

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
    waverefs=Q(iswaveref_trans__in=transs)
    landerefs=Q(islanderef_trans__in=transs)
    loggfrefs=Q(isloggfref_trans__in=transs)
    g1refs=Q(isgammaradref_trans__in=transs)
    g2refs=Q(isgammastarkref_trans__in=transs)
    g3refs=Q(isgammawaalsref_trans__in=transs)
    refQs=[waverefs, landerefs, loggfrefs, g1refs, g2refs, g3refs]
    sources=set()
    for q in refQs:
        refs=Source.objects.filter(q)
        for r in refs:
            sources.add(r)
    return sources

def getVALDsources3(transs):
    sids=set([])
    for trans in transs:
        s=set([trans.wave_ref,trans.loggf_ref,trans.lande_ref,trans.gammarad_ref,trans.gammastark_ref,trans.gammawaals_ref])
        sids=sids.union(s)
    return list(sids)

def getVALDsources4(transs):
    sids=set([])
    for trans in transs:
        s=set([trans.wave_ref.id,trans.loggf_ref.id,trans.lande_ref.id,trans.gammarad_ref.id,trans.gammastark_ref.id,trans.gammawaals_ref.id])
        sids=sids.union(s)
    sources=[]
    for sid in sids:
        sources.append(Source.objects.get(pk=sid))
    return sources

def getVALDsources5(transs):
    sids=set([])
    for trans in transs:
        s=set([trans.wave_ref,trans.loggf_ref,trans.lande_ref,trans.gammarad_ref,trans.gammastark_ref,trans.gammawaals_ref])
        sids=sids.union(s)
    sources=[]
    for sid in sids:
        sources.append(Source.objects.get(pk=sid))
    return sources

def getVALDstates1(transs):
    lostates=State.objects.filter(islowerstate_trans__in=transs)
    histates=State.objects.filter(islowerstate_trans__in=transs)
    states = lostates | histates
    return states.distinct()
    

def getVALDstates2(transs):
    sids=set([])
    for trans in transs:
        s=set([trans.lostate,trans.upstate])
        sids=sids.union(s)
    states=[]
    for sid in sids:
        states.append(State.objects.get(pk=sid))
    return states

def compressedview(request):
    zbuf = cStringIO.StringIO()
    zfile = gzip.GzipFile(mode='wb', compresslevel=6, fileobj=zbuf)
    zfile.write(template.render(context).encode('utf-8'))
    zfile.close()
    
    compressed_content = zbuf.getvalue()
    response = HttpResponse(compressed_content)
    response['Content-Encoding'] = 'gzip'
    response['Content-Length'] = str(len(compressed_content))
    return response
