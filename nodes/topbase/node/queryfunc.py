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
from django.db import connection
import logging
import dictionaries
import models as django_models
import util_models as util_models

log=logging.getLogger('vamdc.tap')

#------------------------------------------------------------
# Helper functions (called from setupResults)
#------------------------------------------------------------
'''
def getRefs(transs):
    """
    From the transition-matches, use ForeignKeys to extract all relevant references
    """
    # extract a unique set of reference keys from the given ForeignKey
    # fields on the Transition model (e.g. Transition.loggf_ref).
    # Note: Using *_id on the ForeignKey (e.g. loggf_ref_id)
    # will extract the identifier rather than go to the referenced
    # object (it's the same as loggf_ref.id, but more efficient).  In
    # our example, refset will hold strings "REF1" or "REF2" after
    # this.
    refset = []
    for t in transs.values_list('wave_ref_id', 'loggf_ref_id', 'lande_ref_id',
                                'gammarad_ref_id', 'gammastark_ref_id', 'waals_ref_id'):
        refset.append(t)
    refset = set(refset) # a set always holds only unique keys

    # Use the found reference keys to extract the correct references from the References table.
    refmatches = models.Reference.objects.filter(pk__in=refset) # only match primary keys in refset
    return refmatches
'''

def getSpeciesWithStates(transs):
    """
    Use the Transition matches to obtain the related Species (only atoms in this example)
    and the states related to each transition.

    We also return some statistics of the result
    """
    # get ions according to selected transitions
    ionids = transs.values_list('version', flat=True).distinct()
    species = django_models.Version.objects.filter(id__in=ionids)
    nstates = 0

    for specie in species:
        # get all transitions in linked to this particular species
        spec_transitions = transs.filter(version=specie.id)
        
        # extract reference ids for the states from the transion, combining both
        # upper and lower unique states together
        ini = spec_transitions.values_list('initialatomicstate',flat=True)
        fin = spec_transitions.values_list('finalatomicstate',flat=True)
        sids = set(chain(ini, fin))

        # use the found reference ids to search the State database table
        specie.States = django_models.Atomicstate.objects.filter( pk__in = sids )
        
        for state in specie.States :
            state.Components = []
            state.Components.append(getCoupling(state))
        nstates += specie.States.count()
        
        
    return species, nstates

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
    
def toLowerUpperStates(transitions):
    for transition in transitions:
        if(transition.initialatomicstate.stateenergy > transition.finalatomicstate.stateenergy):
            transition.upperatomicstate = transition.initialatomicstate
            transition.loweratomicstate = transition.finalatomicstate
        else:
            transition.upperatomicstate = transition.finalatomicstate
            transition.loweratomicstate = transition.initialatomicstate    
    return transitions
    

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
	if str(sql) == 'select species': 
		result = setupSpecies()
	# all other requests
	else:		
		result = setupVssRequest(sql)			

	if isinstance(result, util_models.Result) :
		return result.getResult()
	else:
		raise Exception('error while generating result')


def setupVssRequest(sql, limit=1000):
    """
    This function is always called by the software.
    """
    # log the incoming query
    log.debug(sql)

    # convert the incoming sql to a correct django query syntax object
    q = sql2Q(sql)

    transs = django_models.Radiativetransition.objects.filter(q)
    ntranss=transs.count()

    if limit < ntranss :
        transs, percentage = truncateTransitions(transs, q, limit)
    else:
        percentage=None


    #sources = getRefs(transs)
    #nsources = sources.count()

    species, nstates = getSpeciesWithStates(transs)

    # cross sections
    states = []
    nspecies = species.count()
    for specie in species:        
        for state in specie.States : 
            if state.xdata is not None : # do not add state without xdata/ydata
                states.append(state)
    transs = toLowerUpperStates(transs)

    # Create the result object
    result = util_models.Result()

    result.addHeaderField('TRUNCATED', percentage)
    result.addHeaderField('COUNT-STATES',nstates)
    result.addHeaderField('COUNT-RADIATIVE',ntranss)
    result.addHeaderField('COUNT-SPECIES',nspecies)

    result.addDataField('RadTrans',transs)
    result.addDataField('Atoms',species)
    result.addDataField('RadCross',states)
    
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
	
	
    

