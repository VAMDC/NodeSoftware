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
import time
from itertools import chain
from django.conf import settings
from vamdctap.sqlparse import sql2Q
from django.db.models import Q
from django.db import connection
import logging
import dictionaries
import models as django_models
import util_models as util_models


log=logging.getLogger('vamdc.tap')
l = logging.getLogger('django.db.backends')
l.setLevel(logging.DEBUG)
l.addHandler(logging.FileHandler('/home/nicolas/out'))

#------------------------------------------------------------
# Helper functions (called from setupResults)
#------------------------------------------------------------
def getSpeciesWithStates(transs):
    """
    Use the Transition matches to obtain the related Species (only atoms in this example)
    and the states related to each transition.

    We also return some statistics of the result
    """    
    # get ions according to selected transitions
    ionids = transs.values_list('version', flat=True).distinct()
    species = [] #django_models.Version.objects.filter(id__in=ionids)
    sourceids = []
    nstates = 0
    #sourceids = getTransitionSources(transs)
    for trans in transs:
        trans.Sources = getTransitionSources(trans)
        sourceids.extend(trans.Sources)
    
    for ionid in ionids:
        new_specie = django_models.Version.objects.get(pk=ionid)
        # get all transitions in linked to this particular species
        spec_transitions = transs.filter(version=ionid)
        
        # extract reference ids for the states from the transion, combining both
        # upper and lower unique states together
        lower = spec_transitions.values_list('loweratomicstate',flat=True)
        upper = spec_transitions.values_list('upperatomicstate',flat=True)
        sids = set(chain(upper, lower))

        # use the found reference ids to search the State database table
        new_specie.States = django_models.Atomicstate.objects.filter( pk__in = sids )
        
        for state in new_specie.States :
            state.Components = []
            state.Components.append(getCoupling(state))
            state.Sources = getStateSources(state)
            sourceids.extend(state.Sources)
        nstates += new_specie.States.count()
        species.append(new_specie)
                
    return species, nstates, sourceids
    
    
def getTransitionSources(trans):
    """
        get ids of sources related to a transition
    """
    sourceids = []
    relatedsources = django_models.Radiativetransitionsource.objects.filter(radiativetransition=trans)    
    for relatedsource in relatedsources :
        sourceids.append(relatedsource.source.pk)
    return sourceids    
    '''
    transids = transs.values_list('id', flat=True)  
    relatedsources = django_models.Radiativetransitionsource.objects.filter(id__in=transids)  
    ids = relatedsources.values_list('source', flat=True).distinct() 
    return list(ids)
    '''

    
    
def getStateSources(state):
    """
        get ids of sources related to an atomic state
    """
    sourceids = []
    relatedsources = django_models.Atomicstatesource.objects.filter(atomicstate=state)    
    for relatedsource in relatedsources :
        sourceids.append(relatedsource.source.pk)
    return sourceids
    
    

def getSources(ids):
    """
        get a list of source objects from their ids    
    """
    sources = django_models.Source.objects.filter(pk__in=ids)    
    for source in sources : 
        names=[]
        adresses=[]
        relatedauthors = django_models.Authorsource.objects.filter(source=source).order_by('rank')
        #build a list of authors
        for relatedauthor in relatedauthors:
            names.append(relatedauthor.author.name)
        source.Authors = names
    return sources
        
    

def getCoupling(state):
    """
    Get coupling for the given state
    """
    components = django_models.Atomiccomponent.objects.filter(atomicstate=state)
    for component in components:
        component.Lscoupling = django_models.Lscoupling.objects.get(atomiccomponent=component)
    return components[0]
    
def truncateTransitions(transitions, request, maxTransitionNumber):
    """
    Limit the number of transitions when it is too high
    """
    percentage='%.1f' % (float(maxTransitionNumber) / transitions.count() * 100)
    transitions = transitions.order_by('wavelength')
    newmax = transitions[maxTransitionNumber].wavelength
    return django_models.Radiativetransition.objects.filter(request,Q(wavelength__lt=newmax)), percentage
    
'''def toLowerUpperStates(transitions):
    for transition in transitions:
        if(transition.initialatomicstate.stateenergy > transition.finalatomicstate.stateenergy):
            transition.upperatomicstate = transition.initialatomicstate
            transition.loweratomicstate = transition.finalatomicstate
        else:
            transition.upperatomicstate = transition.finalatomicstate
            transition.loweratomicstate = transition.initialatomicstate    
    return transitions
'''

#------------------------------------------------------------
# Main function
#------------------------------------------------------------
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
	if str(sql).strip() == 'select species': 
		result = setupSpecies()
	# all other requests
	else:		
		result = setupVssRequest(sql)			

	if isinstance(result, util_models.Result) :
		return result.getResult()
	else:
		raise Exception('error while generating result')


def setupVssRequest(sql, limit=3000):
    """
    This function is always called by the software.
    """
    # log the incoming query
    log.debug(sql)

    # convert the incoming sql to a correct django query syntax object
    q = sql2Q(sql)

    start = time.clock()
    transs = django_models.Radiativetransition.objects.filter(q)
    ntranss=transs.count()

    if limit < ntranss :
        transs, percentage = truncateTransitions(transs, q, limit)
    else:
        percentage=None

    species, nstates, sourceids = getSpeciesWithStates(transs)

    # cross sections
    states = []
    
    nspecies = len(species)
    for specie in species:        
        for state in specie.States : 
            if state.xdata is not None : # do not add state without xdata/ydata
                states.append(state)
                
    #transs = toLowerUpperStates(transs)
    sources = getSources(sourceids)
    nsources = sources.count()

    # Create the result object
    result = util_models.Result()

    result.addHeaderField('TRUNCATED', percentage)
    result.addHeaderField('COUNT-STATES',nstates)
    result.addHeaderField('COUNT-RADIATIVE',ntranss)
    result.addHeaderField('COUNT-SPECIES',nspecies)
    result.addHeaderField('COUNT-SOURCES',nsources)  
    
    if(nstates == 0 and nspecies == 0):
        result.addHeaderField('APPROX-SIZE', 0)

    result.addDataField('RadTrans',transs)
    result.addDataField('Atoms',species)
    result.addDataField('RadCross',states)
    result.addDataField('Sources', sources)
    
    end = time.clock()-start
    log.debug("1 "+str(end)+  "s")
    return result
    
def setupSpecies():
	"""		
		Return all target species
		@rtype:   util_models.Result
		@return:  Result object		
	"""
	result = util_models.Result()
	ids = django_models.Radiativetransition.objects.all().values_list('version', flat=True)
	versions = django_models.Version.objects.filter(pk__in = ids)
	result.addHeaderField('COUNT-SPECIES',len(versions))
	result.addDataField('Atoms',versions)	
	return result
	
	
    

