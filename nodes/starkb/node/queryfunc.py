# -*- coding: utf-8 -*-
#
# This module (which must have the name queryfunc.py) is responsible
# for converting incoming queries to a database query understood by
# this particular node's database schema.
# 
# This module must contain a function setupResults, taking a sql object
# as its only argument. 
#

# library imports 

import sys
from itertools import chain
from django.conf import settings
from vamdctap.sqlparse import sql2Q
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import logging
log=logging.getLogger('vamdc.tap')
from django.db import connection


import dictionaries
import models # this imports models.py from the same directory as this file

def getSources(transs):
    """
        Get sources for a list of transitions
        @type  transs: list
        @param transs: a list of Transition
        @rtype:   list
        @return:  list of Article
        
    """
    sources = []
    datasets = transs.values_list('dataset', flat=True).distinct()    
    articledatasets = models.ArticleDataset.objects.filter(dataset__pk__in = datasets)    
    for article in articledatasets :
        sources.append(article.article)
        
    return sources
    
def getDatasetSources(datasetid):
    """
        Get sources for a dataset
        @type  datasetid: int
        @param datasetid: id of a dataset
        @rtype:   list
        @return:  list of Article
        
    """    
    sources = []    
    articledatasets = models.ArticleDataset.objects.filter(dataset__pk = datasetid)    
    for article in articledatasets :
        sources.append(article.article.pk)

    return sources



def getSpeciesWithStates(transs):
    """
        Use the Transition matches to obtain the related Species (only atoms in this example)
        and the states related to each transition.         
        We also return some statistics of the result 
        @type  transs: list
        @param transs: a list of Transition
        @rtype:   list
        @return:  a list of Species
        @rtype:   int
        @return:  number of species
        @rtype:   int
        @return:  number of states
        
    """
    # get ions according to selected transitions    
    targetids = transs.values_list('target', flat=True).distinct()
    targets = models.Species.objects.filter(pk__in=targetids)   
    colliders = getIonCollidersByTransitions(transs)        
    species = targets | colliders  
    # get all states.    
    nstates = 0
    
    for specie in species:
        try :            
            target = targets.get(id = specie.pk)# if ion is a target, look for states      
            # get all transitions in linked to this particular species 
            spec_transitions = transs.filter(target__pk = target.pk)   

            # extract reference ids for the states from the transion, combining both
            # upper and lower unique states together
            up = spec_transitions.values_list('upper_level',flat=True)
            lo = spec_transitions.values_list('lower_level',flat=True)
            sids = set(chain(up, lo))

            specie.States = models.Level.objects.filter( pk__in = sids )
            for i in range(len(specie.States)):
                specie.States[i].Sources = getDatasetSources(specie.States[i].dataset.pk)

            nstates += specie.States.count() 
        except ObjectDoesNotExist as e:
            log.debug(str(e)) # this species is a collider

    nspecies = len(species) # get some statistics 
    return species, nspecies, nstates  
        
def getTransitionsData(transs):
	"""
		Returns all the data  corresponding to the list of transitions : broadening, source, shifting
		@type  transs: list
		@param transs: a list of Transition
		@rtype:   list
		@return:  a list of TemperatureCollider
		@rtype:   list
		@return:  a list of Transitions
	"""
	allenvironments = []
	#dictionnary of transition, key is transition id
	uniquetransitions = {}
	for trans in transs :
		broadenings = []
		shiftings = []
		environments = models.TemperatureCollider.objects.filter(temperature__pk = trans.temperatureid)
	   
		for environment in environments : 
			collider = environment.species
			environment.Species = []             
			environment.Species.append(collider)       
			# note : 
			# generators.py do not create broadening element when broadening.value is empty
			broadenings.append(getBroadening(environment))            
			# shifting to be added later
			#shiftings.append(getShifting(environment))
			allenvironments.append(environment)
		trans.Broadenings = broadenings
		trans.Sources = getDatasetSources(trans.dataset.pk)
		#trans.ShiftingParams = shiftings  
		
		# check if this transitions already exists and extract informations if it is the case
		if trans.id not in uniquetransitions :
			uniquetransitions[trans.id] = trans
		else :
			uniquetransitions[trans.id] .Broadenings.extend(trans.Broadenings)
	
	transitions = uniquetransitions.values()
	return transitions, allenvironments

def getIonCollidersByTransitions(transs): 
    """
        Returns the available perturbers for a list of transitions
        @type  transs: list
        @param transs: a list of Transition
        @rtype:   list
        @return:  a list of Species
    """
    datasets = transs.values_list('dataset', flat=True).distinct()
    datasetcolliders = models.DatasetCollider.objects.filter(dataset__in = datasets)
    colliderids = datasetcolliders.values_list('species', flat=True).distinct()
    return models.Species.objects.filter(pk__in = colliderids).filter(particle = None)
    
def getBroadening(environment):
    """
        extract broadening data from environment
        @type  environment: TemperatureCollider
        @param environment: broadening data container
        @rtype: LineshapeParameter
        @return:  LineshapeParameter
    """
    param = models.LineshapeParameter()
    param.environment = environment.id
    param.value = environment.w
    param.accurracy = 0
    param.comment = getValidity(environment.w, environment.n_w)
    return param
    
def getShifting(environment):
    """
        extract shifting data from environment
        @type  environment: TemperatureCollider
        @param environment: shifting data container
        @rtype: ShiftingParameter
        @return:  ShiftingParameter
    """
    param = models.ShiftingParameter()
    param.environment = environment.id
    param.value = environment.d
    param.accurracy = 0
    param.comment = getValidity(environment.d, environment.n_d)
    return param
    
def getParticles(ntranss):
    """
        returns list of particle perturbers (only electron for now)
        @type  ntranss: int
        @param transs: number of transitions found
        @rtype: list
        @return:  list of Species        
    """
    if ntranss > 0 :
        return models.Species.objects.filter(particle__isnull=False)
    return []
    
def getValidity(value, nvalue):
    """
        get validity condition for broadening and shifting
        @type  value: float
        @param value: shifting or broadening value
        @type  nvalue: string
        @param nvalue: validity indicator in starkb
        @rtype: string
        @return:  validity condition
    """
    if nvalue is None : 
        return None        
    if nvalue == '*':
        if value is None :
            return 'the impact approximation is not valid, because NV > 0.5'
        else : 
            return 'the impact approximation reachs its limit of validity, 0.1 < NV ≤ 0.5'
            
def truncateTransitions(transitions, request, maxTransitionNumber):
    """
    Limit the number of transitions when it is too high
    """
    percentage='%.1f' % (float(maxTransitionNumber) / transitions.count() * 100)
    transitions = transitions.order_by('wavelength')
    newmax = transitions[maxTransitionNumber].wavelength
    return models.Transition.objects.filter(request,Q(wavelength__lt=newmax)), percentage
            

def setupResults(sql, limit=1000):
    """
    This function is always called by the software.
    """
    # convert the incoming sql to a correct django query syntax object 
    # based on the RESTRICTABLES dictionary in dictionaries.py
    # (where2q is a helper function to do this for us).
    q = sql2Q(sql)    
    
    transs = models.Transition.objects.filter(q)
    ntranss=transs.count()

    if limit < ntranss :
        transs, percentage = truncateTransitions(transs, q, limit)
    else:
        percentage=None  

        
    # Through the transition-matches, use our helper functions to extract 
    # all the relevant database data for our query. 
    #sources = getRefs(transs)
    log.debug(ntranss)
    if ntranss > 0 :		
		species, nspecies, nstates = getSpeciesWithStates(transs)           
		transitions, environments = getTransitionsData(transs)    
		particles = getParticles(ntranss) 
		sources =  getSources(transs)
		nsources = len(sources)

		# Create the header with some useful info. The key names here are
		# standardized and shouldn't be changed.
		headerinfo={\
				'Truncated':percentage,
				#'count-sources':nsources,
				'count-species':nspecies,
				'count-states':nstates,
				'count-radiative':len(transitions)
				}
				
		# Return the data. The keynames are standardized. 
		return {'RadTrans':transitions,
				'Atoms':species,
				'Environments':environments,
				'Particles' : particles,
				'Sources':sources,
				'HeaderInfo':headerinfo,
				#'Methods':methods
				#'Functions':functions
			   }   
    else :
        headerinfo={\
                'Truncated':percentage,
                'count-states':0,
                'count-radiative':0
                }
                
        # Return the data. The keynames are standardized. 
        return {'HeaderInfo':headerinfo}           
    

