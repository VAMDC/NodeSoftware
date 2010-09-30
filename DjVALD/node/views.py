# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,get_object_or_404
from django.db.models import Q
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

from DjVALD.node.models import *

import sys
def LOG(s):
    if settings.DEBUG: print >> sys.stderr, s

#from lxml import etree as E
#vo2html=E.XSLT(E.parse(open(settings.BASEPATH+'DjNode/static/xsl/VOTable2XHTML_mine.xsl')))


RETURNABLES={\
'SourceID':'Source.id',
'SourceAuthorName':'Source.publications.all()[0].author',
'SourceCategory':'Source.publications.all()[0].category',
'SourcePageBegin':'Source.publications.all()[0].pages',
'SourcePageEnd':'Source.publications.all()[0].pages',
'SourceName':'Source.publications.all()[0].journal',
'SourceTitle':'Source.publications.all()[0].title',
'SourceURI':'Source.publications.all()[0].url',
'SourceVolume':'Source.publications.all()[0].volume',
'SourceYear':'Source.publications.all()[0].year',
'MethodID':'"MOBS"',
'MethodCategory':'"observed"',
'MethodDescription':'',
'AtomStateID':'AtomState.id',
'AtomSymbol':'AtomState.species.name',
'AtomNuclearCharge':'AtomState.species.atomic',
'AtomConfigurationLabel':'AtomState.charid',
'AtomCompositionComponentTerm':'AtomState.term',
'AtomIonizationEnergy':'AtomState.species.ionen',
'AtomStateLandeFactor':'AtomState.lande',
'AtomStateLandeFactorRef':'AtomState.lande_ref',
'AtomStateEnergy':'AtomState.energy',
'AtomStateEnergyRef':'AtomState.energy_ref',
'AtomStateEnergyUnits':'1/cm',
'AtomStateDescription':'',
'AtomIonCharge':'AtomState.species.ion',
'AtomMassNumber':'AtomState.species.massno',
'RadTransComments':'Wavelength is for vacuum.',
'RadTransWavelengthExperimentalValue':'RadTran.vacwave',
'RadTransWavelengthExperimentalUnits':u'\xc5',
'RadTransProbabilityLog10WeightedOscillatorStrengthAccuracy':'RadTran.accur',
'RadTransWavelengthExperimentalSourceRef':'RadTran.wave_ref',
'RadTransFinalStateRef':'RadTran.lostate.id',
'RadTransInitialStateRef':'RadTran.upstate.id',
'RadTransLogGF':'RadTran.loggf',
'RadTransMethodRef':'OBS',
'RadTransProbabilityLog10WeightedOscillatorStrengthSourceRef':'RadTran.loggf_ref',
'RadTransProbabilityLog10WeightedOscillatorStrengthValue':'RadTran.loggf',
'RadTransBroadRadGammaLog':'RadTran.gammarad',
'RadTransBroadRadRef':'RadTran.gammarad_ref',
'RadTransBroadStarkGammaLog':'RadTran.gammastark',
'RadTransBroadStarkRef':'RadTran.gammastark_ref',
'RadTransBroadWaalsGammaLog':'RadTran.gammawaals',
'RadTransBroadWaalsAlpha':'RadTran.alphawaals',
'RadTransBroadWaalsSigma':'RadTran.sigmawaals',
'RadTransBroadWaalsRef':'RadTran.waals_ref',
'RadTransEffLande':'RadTran.landeff',
'RadTransEffLandeRef':'RadTran.lande_ref',
}

RESTRICTABLES = {\
'AtomSymbol':'species__name',
'AtomNuclearCharge':'species__atomic',
'AtomStateEnergy':'upstate__energy',
'RadTransWavelengthExperimentalValue':'vacwave',
'RadTransLogGF':'loggf',
'AtomIonCharge':'species__ion',
}

from DjNode.tapservice.sqlparse import *


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
    
    #solution 1
    #q1,q2=Q(isupperstate_trans__in=transs),Q(islowerstate_trans__in=transs)
    #return State.objects.filter(q1|q2).distinct()

    # solution 2
    #lostates=State.objects.filter(islowerstate_trans__in=transs)
    #histates=State.objects.filter(isupperstate_trans__in=transs)
    #states = lostates | histates
    #return states.distinct()

    #solution 3, similar to sources
    sids=set([])
    for trans in transs:
        s=set([trans.upstate.pk,trans.lostate.pk])
        sids=sids.union(s)
    return State.objects.filter(pk__in=sids)
   

def setupResults(sql,limit=0):
    LOG(sql)
    q=where2q(sql.where,RESTRICTABLES)
    try: q=eval(q)
    except: return {}
    
    transs = Transition.objects.select_related(depth=2).filter(q)
    
    totalcount=transs.count()
    if limit :
        transs = transs[:limit]

    sources = getVALDsources(transs)
    states = getVALDstates(transs)

    # in order to not forget it:
    # write a small function that defines/fixes the
    # string representation of the wavelengths which
    # should have 8 significant dicits, i.e. variable
    # number of decimals.
    # maybe this can be achieved in the model itself.

    return {'RadTrans':transs,
            'AtomStates':states,
            'Sources':sources,
           }







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


