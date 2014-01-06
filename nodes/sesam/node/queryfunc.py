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
from itertools import chain
from vamdctap.sqlparse import sql2Q
from django.db.models import Q
from dictionaries import *
from django.core.exceptions import ObjectDoesNotExist

import models as models
import util_models as util_models # utility classes
import logging

log = logging.getLogger("vamdc.node.queryfu")

LIMIT = 1000

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
	result.addDataField('Molecules',species)	
	return result
	
def setupVssRequest(sql, limit=2000):
    """		
        Execute a vss request
        @type  sql: string
        @param sql: vss request
        @rtype:   util_models.Result
        @return:  Result object		
    """

    result = util_models.Result()
    q = sql2Q(sql)    
    log.debug(q)
    #select transitions : combination of density/temperature
    transs = models.Radiativetransition.objects.filter(q)
    ntranss=transs.count()
    methods = util_models.Methods()

    if limit < ntranss :
        transs, percentage = truncateTransitions(transs, q, limit)
    else:
        percentage=None 
        
    log.debug("number of transitions : "+str(ntranss))
    # Through the transition-matches, use our helper functions to extract 
    # all the relevant database data for our query. 
    if ntranss > 0 :	
        species, nspecies, nstates = getSpeciesWithStates(transs)      
        transitions = transs        
        sources =  getSources(transs)  
        nsources = len(sources)

        # Create the header with some useful info. The key names here are
        # standardized and shouldn't be changed.
        result.addHeaderField('TRUNCATED',percentage)
        result.addHeaderField('COUNT-SPECIES',nspecies)
        result.addHeaderField('COUNT-STATES',nstates)
        result.addHeaderField('COUNT-SOURCES',nsources)	
        result.addHeaderField('COUNT-RADIATIVE',len(transitions))	
       
        result.addDataField('RadTrans',transitions)        
        result.addDataField('Molecules',species)
        result.addDataField('Methods',methods.getMethodsAsList())
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
	return models.Radiativetransition.objects.filter(request,Q(wavelength__lt=newmax)), percentage
    
def getSpecies():
	"""
		returns list of particle perturbers (only electron for now)
		@type  ntranss: int
		@param transs: number of transitions found
		@rtype: list
		@return:  list of Species        
	"""
	return models.Molecule.objects.all()
    
def getSources(transs):
    sourceids = transs.values_list('source', flat=True).distinct()
    return models.Source.objects.filter(pk__in=sourceids)  
    
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
    moleculeids = transs.values_list('molecule', flat=True).distinct()
    species = models.Molecule.objects.filter(pk__in=moleculeids)   
        
    # get all states.    
    nstates = 0
    
    for specie in species:
        try :  
            # get all transitions in linked to this particular species 
            spec_transitions = transs.filter(molecule__pk = specie.pk)   
            # extract reference ids for the states from the transion, combining both
            # upper and lower unique states together
            up = spec_transitions.values_list('upperstate',flat=True)
            lo = spec_transitions.values_list('lowerstate',flat=True)
            sids = set(chain(up, lo))
            getStates(specie, sids)            
            nstates += len(specie.States)
        except ObjectDoesNotExist as e:
            log.debug(str(e)) 
    
    nspecies = len(species) # get some statistics 
    return species, nspecies, nstates  
    
def getStates(specie, sids):
    states = models.Molecularstate.objects.filter(pk__in = sids)
    datasets = states.values_list('dataset__pk',flat=True).distinct()
    #energy origin
    origin = models.Molecularstate.objects.filter(dataset__in = datasets, energy=0)[0]
    
    for state in states:        
        state.Case = models.Case.objects.get( molecularstate = state.id)
        state.SubCase = state.Case.getSubCase()
        state.origin = origin.pk
        
    origin.Case = models.Case.objects.get( molecularstate = origin.id)
    origin.SubCase = origin.Case.getSubCase()
    origin.origin = origin.pk       
        
    result_list = list(chain(states, [origin]))
        
    specie.States = result_list

    
