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
log=logging.getLogger('vamdc.tap')

import dictionaries
import models as django_models
import util_models as util_models

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
        Execute a vss request
        @type  sql: string
        @param sql: vss request
        @rtype:   util_models.Result
        @return:  Result object		
    """
    # convert the incoming sql to a correct django query syntax object 
    # based on the RESTRICTABLES dictionary in dictionaries.py
    q = sql2Q(sql)   

    transs = django_models.Collisionaltransition.objects.filter(q)
    # count the number of matches, make a simple trunkation if there are
    # too many (record the coverage in the returned header)
    ncoll=transs.count()
    if limit < ncoll :
        transs, percentage = truncateTransitions(transs, q, limit)
    else:
        percentage=None

    species, nstates, sourceids = getSpeciesWithStates(transs)
    # electron collider
    particles = getParticles()

    # cross sections
    states = []
    for specie in species:
        states.extend(specie.States)
    nspecies = species.count()

    nspecies = species.count()
    sources = getSources(sourceids)
    nsources = sources.count()

    # Create the result object
    result = util_models.Result()
    result.addHeaderField('TRUNCATED', percentage)
    result.addHeaderField('COUNT-STATES',nstates)
    result.addHeaderField('COUNT-COLLISIONS',ncoll)
    result.addHeaderField('COUNT-SPECIES',nspecies)
    result.addHeaderField('COUNT-SOURCES',nsources)
    
    if ncoll > 0 :
        result.addDataField('CollTrans',transs)
        result.addDataField('Particles',particles)
    result.addDataField('Atoms',species)
    result.addDataField('Sources',sources)
    

    return result
    
def setupSpecies():
	"""		
		Return all target species
		@rtype:   util_models.Result
		@return:  Result object		
	"""
	result = util_models.Result()
	ids = django_models.Collisionaltransition.objects.all().values_list('version', flat=True)
	versions = django_models.Version.objects.filter(pk__in = ids)
	result.addHeaderField('COUNT-SPECIES',len(versions))
	result.addDataField('Atoms',versions)	
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
	transitions = transitions.order_by('initialatomicstate__stateenergy')
	newmax = transitions[maxTransitionNumber].initialatomicstate.stateenergy
	return django_models.Collisionaltransition.objects.filter(request,Q(initialatomicstate__stateenergy__lt=newmax)), percentage


def getSpeciesWithStates(transs):
    """
    Use the Transition matches to obtain the related Species (only atoms in this example)
    and the states related to each transition.

    We also return some statistics of the result
    """
    # get ions according to selected transitions
    ionids = transs.values_list('version', flat=True).distinct()
    species = django_models.Version.objects.filter(id__in=ionids)
    # get all states.
    nstates = 0
    sourceids = []

    for trans in transs :
        setSpecies(trans)
        # get tabulated data and their references
        setDataset(trans, sourceids)

    for specie in species:
        # get all transitions in linked to this particular species
        spec_transitions = transs.filter(version=specie.id)
        # extract reference ids for the states from the transion, combining both
        # upper and lower unique states together
        up = spec_transitions.values_list('initialatomicstate',flat=True)
        lo = spec_transitions.values_list('finalatomicstate',flat=True)
        sids = set(chain(up, lo))

        # use the found reference ids to search the State database table
        specie.States = django_models.Atomicstate.objects.filter( pk__in = sids )
        for state in specie.States :
            state.Components = []
            state.Components.append(getCoupling(state))
            state.Sources = getStateSources(state)
            sourceids.extend(state.Sources)            
        nstates += specie.States.count()
    return species, nstates, sourceids
    
    
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

def getTabdataSources(tabdata):
    """
        get source ids of tabdata 
    """
    sourceids = []
    relatedsources = django_models.Tabulateddatasource.objects.filter(pk=tabdata.pk)    
    for relatedsource in relatedsources :
        sourceids.append(relatedsource.source.pk)
    return sourceids    
    
def setDataset(trans, sourceids):
    """
     create Dataset with Tabulated data
     trans : a given transition
     sourceids : a list of all references for the current request
    """
    tabulateddata = django_models.Tabulateddata.objects.filter(collisionaltransition = trans.id)
    sources = []
    trans.DataSets = []
    
    # get tabulated data
    for data in tabulateddata : 
        datasources = getTabdataSources(data) 
        # add reference to list global list of references for this query  
        for source in datasources : 
            if source not in sourceids :
                sourceids.append(source)
        dataset = util_models.XsamsDataset()
        dataset.TabData = []
        dataset.TabData.append(data)
        data.Sources = datasources
        dataset.dataDescription = data.datadescription.value
        trans.DataSets.append(dataset)  

def setSpecies(trans):
    """
    add product and reactant states
    """
    setReactants(trans)
    setProducts(trans)

def setReactants(trans):
    """
    add reactants
    """
    trans.Reactants = []
    trans.Reactants.append(trans.initialatomicstate)
    particle = django_models.Particle.objects.filter(name='electron') # second reactant is always an electron for now
    if(len(particle) == 1 ):    
        trans.Reactants.append(particle[0])

def setProducts(trans):
    """
    add product
    """
    trans.Products = []
    trans.Products.append(trans.finalatomicstate)


def getCoupling(state):
    """
    Get coupling for the given state
    """
    components = django_models.Atomiccomponent.objects.filter(atomicstate=state)
    for component in components:
        component.Lscoupling = django_models.Lscoupling.objects.get(atomiccomponent=component)
    return components[0]
    
def getParticles():    
    return django_models.Particle.objects.all()   


