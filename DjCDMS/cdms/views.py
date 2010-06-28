# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,get_object_or_404
from django.db.models import Q
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

from DjVALD.vald.models import Transition,State,Source,Species

# This imports all the generic tap views and functions
from DjNode.tapservice.views import *

from base64 import b64encode as b64
def enc(s):
    return b64(s).replace('=','')

from lxml import etree as E
vo2html=E.XSLT(E.parse(open(settings.BASEPATH+'DjNode/static/xsl/VOTable2XHTML_mine.xsl')))


VALD_DICT={'1':'species__atomic',
           '2':'species__ion',
           '3':'vacwave',
           '4':'airwave',
           '5':'loggf',
           '6':'lostate__energy',
           '7':'lostate__J',
           }

VAMDC_DICT={\
'4':'RadiativeTransitions.frequencyvalue',
'SourceID':'Sources.rId',
'SourceAuthorName':'Sources.authors',
'SourceCategory':'Sources.category',
'SourcePageBegin':'Sources.pageBegin',
'SourcePageEnd':'Sources.pageEnd',
'SourceName':'Sources.name',
'SourceTitle':'Sources.title',
'SourceURI':'Sources.uri',
'SourceVolume':'Sources.vol',
'SourceYear':'Sources.year',
'MethodID':'"MCALC"',
'MethodCategory':'"calculated"',
'MethodDescription':'',
'AtomStateID':'',
'AtomSymbol':'',
'AtomNuclearCharge':'',
'AtomCompositionComments':'',
'AtomConfigurationLabel':'',
'AtomCompositionComponentTerm':'',
'AtomIonizationEnergy':'',
'AtomLandeFactor':'',
'AtomStateEnergy':'',
'AtomStateDescription':'',
'AtomIonCharge':'',
'AtomMassNumber':'',
#'RadTransComments':'',
#'RadTransWavelengthAir':'',
#'RadTransWavelengthVac':'',
#'RadTransWavelengthAccuracyFlag':'',
#'RadTransWavelengthAccuracy':'',

'RadTransComments':'',

'RadTransFinalStateRef':'RadiativeTransitions.FinalStateRef',
'RadTransInitialStateRef':'RadiativeTransitions.InitialStateRef',

'RadTransWavenumberRitzComments':'',
'RadTransWavenumberRitzSourceRef':'',
'RadTransWavenumberRitzMethodRef':'',
'RadTransWavenumberRitzValue':'',
'RadTransWavenumberRitzUnits':'',
'RadTransWavenumberRitzAccuracy':'',
'RadTransWavenumberExperimentalComments':'',
'RadTransWavenumberExperimentalSourceRef':'',
'RadTransWavenumberExperimentalMethodRef':'',
'RadTransWavenumberExperimentalValue':'',
'RadTransWavenumberExperimentalUnits':'',
'RadTransWavenumberExperimentalAccuracy':'',
'RadTransWavenumberTheoreticalComments':'',
'RadTransWavenumberTheoreticalSourceRef':'',
'RadTransWavenumberTheoreticalMethodRef':'',
'RadTransWavenumberTheoreticalValue':'',
'RadTransWavenumberTheoreticalUnits':'',
'RadTransWavenumberTheoreticalAccuracy':'',
'RadTransWavelengthRitzComments':'',
'RadTransWavelengthRitzSourceRef':'',
'RadTransWavelengthRitzMethodRef':'',
'RadTransWavelengthRitzValue':'',
'RadTransWavelengthRitzUnits':'',
'RadTransWavelengthRitzAccuracy':'',
'RadTransWavelengthExperimentalComments':'',
'RadTransWavelengthExperimentalSourceRef':'',
'RadTransWavelengthExperimentalMethodRef':'',
'RadTransWavelengthExperimentalValue':'',
'RadTransWavelengthExperimentalUnits':'',
'RadTransWavelengthExperimentalAccuracy':'',
'RadTransWavelengthTheoreticalComments':'',
'RadTransWavelengthTheoreticalSourceRef':'',
'RadTransWavelengthTheoreticalMethodRef':'',
'RadTransWavelengthTheoreticalValue':'',
'RadTransWavelengthTheoreticalUnits':'',
'RadTransWavelengthTheoreticalAccuracy':'',
'RadTransEnergyRitzComments':'',
'RadTransEnergyRitzSourceRef':'',
'RadTransEnergyRitzMethodRef':'',
'RadTransEnergyRitzValue':'',
'RadTransEnergyRitzUnits':'',
'RadTransEnergyRitzAccuracy':'',
'RadTransEnergyExperimentalComments':'',
'RadTransEnergyExperimentalSourceRef':'',
'RadTransEnergyExperimentalMethodRef':'',
'RadTransEnergyExperimentalValue':'',
'RadTransEnergyExperimentalUnits':'',
'RadTransEnergyExperimentalAccuracy':'',
'RadTransEnergyTheoreticalComments':'',
'RadTransEnergyTheoreticalSourceRef':'',
'RadTransEnergyTheoreticalMethodRef':'',
'RadTransEnergyTheoreticalValue':'',
'RadTransEnergyTheoreticalUnits':'',
'RadTransEnergyTheoreticalAccuracy':'',
'RadTransFrequencyRitzComments':'',
'RadTransFrequencyRitzSourceRef':'',
'RadTransFrequencyRitzMethodRef':'',
'RadTransFrequencyRitzValue':'',
'RadTransFrequencyRitzUnits':'',
'RadTransFrequencyRitzAccuracy':'',
'RadTransFrequencyExperimentalComments':'',
'RadTransFrequencyExperimentalSourceRef':'',
'RadTransFrequencyExperimentalMethodRef':'',
'RadTransFrequencyExperimentalValue':'',
'RadTransFrequencyExperimentalUnits':'',
'RadTransFrequencyExperimentalAccuracy':'',
'RadTransFrequencyTheoreticalComments':'',
'RadTransFrequencyTheoreticalSourceRef':'',
'RadTransFrequencyTheoreticalMethodRef':'',
'RadTransFrequencyTheoreticalValue':'RadiativeTransitions.frequencyvalue',
'RadTransFrequencyTheoreticalUnits':'RadiativeTransitions.frequencyunit',
'RadTransFrequencyTheoreticalAccuracy':'RadiativeTransitions.energywavelengthaccuracy',
'RadTransProbabilityTransitionProbabilityAComments ':'',
'RadTransProbabilityTransitionProbabilityASourceRef':'',
'RadTransProbabilityTransitionProbabilityAMethodRef':'',
'RadTransProbabilityTransitionProbabilityAValue':'',
'RadTransProbabilityTransitionProbabilityAUnits':'',
'RadTransProbabilityTransitionProbabilityAAccuracy':'',
'RadTransProbabilityOscillatorStrengthComments ':'',
'RadTransProbabilityOscillatorStrengthSourceRef':'',
'RadTransProbabilityOscillatorStrengthMethodRef':'',
'RadTransProbabilityOscillatorStrengthValue':'',
'RadTransProbabilityOscillatorStrengthUnits':'',
'RadTransProbabilityOscillatorStrengthAccuracy':'',
'RadTransProbabilityLineStrengthComments ':'',
'RadTransProbabilityLineStrengthSourceRef':'',
'RadTransProbabilityLineStrengthMethodRef':'',
'RadTransProbabilityLineStrengthValue':'',
'RadTransProbabilityLineStrengthUnits':'',
'RadTransProbabilityLineStrengthAccuracy':'',
'RadTransProbabilityWeightedOscillatorStrengthComments ':'',
'RadTransProbabilityWeightedOscillatorStrengthSourceRef':'',
'RadTransProbabilityWeightedOscillatorStrengthMethodRef':'',
'RadTransProbabilityWeightedOscillatorStrengthValue':'',
'RadTransProbabilityWeightedOscillatorStrengthUnits':'',
'RadTransProbabilityWeightedOscillatorStrengthAccuracy':'',
'RadTransProbabilityLog10WeightedOscillatorStrengthComments ':'',
'RadTransProbabilityLog10WeightedOscillatorStrengthSourceRef':'',
'RadTransProbabilityLog10WeightedOscillatorStrengthMethodRef':'',
'RadTransProbabilityLog10WeightedOscillatorStrengthValue':'RadiativeTransitions.log10weightedoscillatorstrengthvalue',
'RadTransProbabilityLog10WeightedOscillatorStrengthUnits':'RadiativeTransitions.log10weightedoscillatorstrengthunit',
'RadTransProbabilityLog10WeightedOscillatorStrengthAccuracy':'',
'RadTransProbabilityIdealisedIntensityComments ':'',
'RadTransProbabilityIdealisedIntensitySourceRef':'',
'RadTransProbabilityIdealisedIntensityMethodRef':'',
'RadTransProbabilityIdealisedIntensityValue':'',
'RadTransProbabilityIdealisedIntensityUnits':'',
'RadTransProbabilityIdealisedIntensityAccuracy':'',
'RadTransProbabilityProbability:MultipoleValue':'RadiativeTransitions.multipole',


'CollisionComments':'',
'CollisionTabulatedData':'',
'CollisionProcessClassCode':'',
'CollisionProductsStateRef':'',
'CollisionReactantsStateRef':'',


# table for molecular states 
# (maybe molecular species should be a separate table)
    
'MolecularSpeciesChemicalName':'StatesMolecules.molecularchemicalspecies',
'MolecularSpeciesOrdinaryStructuralFormula':'',
'MolecularSpeciesStoichiometrcFormula':'StatesMolecules.isotopomer',
'MolecularSpeciesIonCharge':'',
'MolecularSpeciesIUPACName':'',
'MolecularSpeciesURLFigure':'',
'MolecularSpeciesInChl':'',
'MolecularSpeciesCASRegistryNumber':'',
'MolecularSpeciesCNPIGroup':'',
'MolecularSpeciesMoleculeNuclearSpins':'',
'MolecularSpeciesStableMolecularProperties':'',
'MolecularSpeciesMolecularWeight':'',
'MolecularSpeciesComment':'',
'MoleculeNuclearSpinsAtomArray':'',
'MoleculeNuclearSpinsBondArray':'',

'MolecularStateStateID':'',
'MolecularStateDescription':'',
'MolecularStateEnergyComments':'',
'MolecularStateEnergySourceRef':'',
'MolecularStateEnergyMethodRef':'',
'MolecularStateEnergyValue':'StatesMolecules.stateenergyvalue',
'MolecularStateEnergyUnit':'StatesMolecules.stateenergyunit',
'MolecularStateEnergyAccuracy':'StatesMolecules.stateenergyaccuracy',
'MolecularStateEnergyOrigin':'',
'MolecularStateMixingCoefficient':'StatesMolecules.mixingcoefficient',

'MolecularStateCharacTotalStatisticalWeight':'',
'MolecularStateCharacNuclearStatisticalWeight':'StatesMolecules.statenuclearstatisticalweight',
'MolecularStateCharacNuclearSpinSymmetry':'',
'MolecularStateCharacLifeTime':'',
'MolecularStateCharacParameters':'',

# table for quantum numbers

'MolQnStateID':'',
'MolQnCase':'',  #(for case-by-case)
'MolQnLabel':'', #(for case-by-case) (should be labels suggested by Christian Hill)
'MolXPath':'',   #(for classical)
'MolTag':'',     #(for classical)
'MolQnValue':'',
'MolQnSpinRef':'',
'MolQnAttribute':'',
'MolQnComment':''

}

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
    q1,q2=Q(isupperstate_trans__in=transs),Q(islowerstate_trans__in=transs)
    return State.objects.filter(q1|q2).distinct()
    



def setupResults(tap,limit=0):
    if (1==1): #tap.lang=='vamdc':
        tap.query=tap.query%VAMDC_DICT
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


