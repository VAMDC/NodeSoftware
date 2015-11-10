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
from django.db import connection
import dictionaries
import models as django_models
import util_models as util_models # utility classes

if hasattr(settings,'LAST_MODIFIED'):
  LAST_MODIFIED = settings.LAST_MODIFIED
else: LAST_MODIFIED = None

def setupResults(sql):
	"""		
		Return results for request
		@type  sql: string
		@param sql: vss request
		@type  limit: int
		@param limit: maximum number of results
		@rtype:   dict
		@return:  dictionnary containig data		
	"""
	result = None
	# return all species
	if str(sql).strip().lower() == 'select species': 
		result = setupSpecies()
	# all other requests
	else:		
		result = setupVssRequest(sql)			

	if isinstance(result, util_models.Result) :
		return result.getResult()
	else:
		raise Exception('error while generating result')
		
def setupSpecies():
	"""		
		Return all target species
		@rtype:   util_models.Result
		@return:  Result object		
	"""
	result = util_models.Result()
	species = getSpecies()
	result.addHeaderField('COUNT-SPECIES',len(species))
	result.addDataField('Atoms',species)	
	return result
	
def setupVssRequest(sql, limit=500):
    """		
        Execute a vss request
        @type  sql: string
        @param sql: vss request
        @rtype:   util_models.Result
        @return:  Result object		
    """

    result = util_models.Result()
    q = sql2Q(sql)    

    #select transitions : combination of density/temperature
    transs = django_models.Transition.objects.filter(q)
    ntranss=transs.count()

    if limit < ntranss :
        transs, percentage = truncateTransitions(transs, q, limit)
    else:
        percentage=None 
        
    # Through the transition-matches, use our helper functions to extract 
    # all the relevant database data for our query. 
    if ntranss > 0 :	
        species, nspecies, nstates = getSpeciesWithStates(transs)      
        transitions, environments = getTransitionsData(transs)    
        particles = getParticles(ntranss) 
        functions = getFunctions()
        sources =  getSources(transs)
        nsources = len(sources)
        

        # Create the header with some useful info. The key names here are
        # standardized and shouldn't be changed.
        result.addHeaderField('TRUNCATED',percentage)
        result.addHeaderField('COUNT-SPECIES',nspecies)
        result.addHeaderField('COUNT-STATES',nstates)
        result.addHeaderField('COUNT-RADIATIVE',len(transitions))	
        
        if LAST_MODIFIED is not None : 
          result.addHeaderField('LAST-MODIFIED',LAST_MODIFIED)
       
        result.addDataField('RadTrans',transitions)        
        result.addDataField('Atoms',species)
        result.addDataField('Environments',environments)
        result.addDataField('Particles',particles)
        result.addDataField('Functions',functions)
        result.addDataField('Sources',sources)
        
    else : # only fill header
        result.addHeaderField('APPROX-SIZE', 0)    
        result.addHeaderField('TRUNCATED',percentage)
        result.addHeaderField('COUNT-STATES',0)
        result.addHeaderField('COUNT-RADIATIVE',0)
    return result	
	
def truncateTransitions(transitions, request, maxTransitionNumber):
	"""		
		limit the number of transitions
		@type  transitions: list
		@param transitions: a list of Transition
		@type  request: Q()
		@param request: sql query
		@type  maxTransitionNumber: int
		@param maxTransitionNumber: max number of transitions
		@rtype:   list
		@return:  truncated list of transitions		
	"""
	percentage='%.1f' % (float(maxTransitionNumber) / transitions.count() * 100)
	transitions = transitions.order_by('wavelength')
	newmax = transitions[maxTransitionNumber].wavelength
	return django_models.Transition.objects.filter(request,Q(wavelength__lt=newmax)), percentage

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
    articledatasets = django_models.ArticleDataset.objects.filter(dataset__pk__in = datasets)    
    for article in articledatasets :
        if article.article not in sources : 
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
    articledatasets = django_models.ArticleDataset.objects.filter(dataset__pk = datasetid)    
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
    targets = django_models.Species.objects.filter(pk__in=targetids)   
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
            getStates(specie, sids)
            for i in range(len(specie.States)):
                specie.States[i].Sources = getDatasetSources(specie.States[i].Components[0].dataset.pk)

            nstates += len(specie.States)
        except ObjectDoesNotExist as e:
            pass
            #log.debug(str(e)) # this species is a collider

    nspecies = len(species) # get some statistics 
    return species, nspecies, nstates  
    
def getStates(specie, sids):
    statescomponent = django_models.Level.objects.filter( pk__in = sids )
    allStates = []
    for component in statescomponent : 
        starkState = util_models.State()
        starkState.id = component.id
        starkState.parity = component.get_int_parity()
        starkState.totalAngularMomentum = component.j_asFloat()
        starkState.Components.append(component)
        allStates.append(starkState)
    specie.States = allStates

    return specie
    
        
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
        environments = django_models.TemperatureCollider.objects.filter(temperature__pk = trans.temperatureid)

        for environment in environments : 
            collider = environment.species
            environment.Species = []             
            environment.Species.append(collider)       
            # note : 
            # generators.py do not create broadening element when broadening.value is empty
            br = getBroadening(environment)
            if br is not None : 
                broadenings.append(br) 
                #getFitBroadening(environment)           
            # shifting to be added later
            sh = getShifting(environment)
            if sh is not None : 
                shiftings.append(sh)
            allenvironments.append(environment)
        trans.Broadenings = broadenings
        trans.Sources = getDatasetSources(trans.dataset.pk)
        trans.Shiftings = shiftings  

        # check if this transitions already exists and extract informations if it is the case
        if trans.id not in uniquetransitions :
            uniquetransitions[trans.id] = trans
        else :
            uniquetransitions[trans.id] .Broadenings.extend(trans.Broadenings)
            uniquetransitions[trans.id] .Shiftings.extend(trans.Shiftings)

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
	datasetcolliders = django_models.DatasetCollider.objects.filter(dataset__in = datasets)
	colliderids = datasetcolliders.values_list('species', flat=True).distinct()
    # exclude meanion from list of species
	return django_models.Species.objects.filter(pk__in = colliderids).filter(particle = None).exclude(ion__name="meanion")
    
def getBroadening(environment):
    """
        extract broadening data from environment
        @type  environment: TemperatureCollider
        @param environment: broadening data container
        @rtype: LineshapeParameter
        @return:  LineshapeParameter
    """
    if environment.w is not None :
        param = util_models.LineshapeParameter()
        param.environment = environment.id
        param.value = environment.w    
        param.accurracy = 0
        param.comment = getValidity(environment.w, environment.n_w)
        return param
    return None
    
def getFitCoefficients(environment):
    fits = django_models.FitCoefficient.objects.filter(transitiondata=environment.temperature.transitiondata, species=environment.species)
    broad = [fits.a0, fits.a1, fits.a2]
    
def getShifting(environment):
    """
        extract shifting data from environment
        @type  environment: TemperatureCollider
        @param environment: shifting data container
        @rtype: ShiftingParameter
        @return:  ShiftingParameter
    """    
    if environment.d is not None :
        shifting = util_models.Shifting()
        shifting.environment = environment.id
        shiftingParameter = util_models.ShiftingParameter()
        shiftingParameter.value = environment.d
        shiftingParameter.accurracy = 0
        shiftingParameter.comment = getValidity(environment.d, environment.n_d)
        shifting.ShiftingParams.append(shiftingParameter)
        return shifting
    return None
    
def getParticles(ntranss):
	"""
		returns list of particle perturbers (only electron for now)
		@type  ntranss: int
		@param transs: number of transitions found
		@rtype: list
		@return:  list of Species        
	"""
	if ntranss > 0 :
		return django_models.Species.objects.filter(particle__isnull=False)
	return []
	
def getSpecies():
	"""
		returns list of particle perturbers (only electron for now)
		@type  ntranss: int
		@param transs: number of transitions found
		@rtype: list
		@return:  list of Species        
	"""
	ids = django_models.Dataset.objects.values_list('target', flat = True).distinct()
	species = django_models.Species.objects.filter(pk__in = ids)
	return species
	    
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
            

def getFunctions():
    functions = []
    functions.append(util_models.FunctionBuilder.widthCalculation())
    functions.append(util_models.FunctionBuilder.shiftCalculation())
    return functions
