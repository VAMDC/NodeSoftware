# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,get_object_or_404
from django.db.models import Q
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

#from DjVALD.vald.models import Transition,State,Source,Species
from DjCDMS.cdms.models import RadiativeTransitions,StatesMolecules,Sources #,Species

import sys
def LOG(s):
    print >> sys.stderr, s




RETURNABLES={\
'SourceID':'Sources.rId', #.id',
'SourceAuthorName':'Sources.authors', #.srcdescr',
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

RESTRICTABLES = {\
'AtomSymbol':'species__name',
'AtomNuclearCharge':'species__atomic',
'AtomStateEnergy':'upstate__energy',
'RadTransWavelengthExperimentalValue':'vacwave',
'RadTransLogGF':'loggf',
'AtomIonCharge':'species__ion',
}


from DjNode.tapservice.sqlparse import *

def getCDMSsources(transs):
    return # no sources yet for CDMS, afaik
    #return Source.objects.filter(pk__in=sids)

def getCDMSstates(transs):
    q1,q2=Q(isupperstate_trans__in=transs),Q(islowerstate_trans__in=transs)
    return State.objects.filter(q1|q2).distinct()
    



def setupResults(sql):
    LOG(sql)
    q=where2q(sql.where,RESTRICTABLES)
    try: q=eval(q)
    except: return {}
   
    transs = Transition.objects.select_related().filter(q)

    sources = getCDMSsources(transs)
    states = getCDMSstates(transs)
    return {'RadTrans':transs,
            'MoleStates':states,
            'Sources':sources,
            }


