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
import node.dictionaries
import node.models as django_models

if hasattr(settings,'TRANSLIM'):
  TRANSLIM = settings.TRANSLIM
else: TRANSLIM = 1000

if hasattr(settings,'LAST_MODIFIED'):
  LAST_MODIFIED = settings.LAST_MODIFIED
else: LAST_MODIFIED = None

log=logging.getLogger('vamdc.tap')

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
    #~ start_time = time.time()
    #~ ionids = transs.values_list('version', flat=True).distinct()
    species = [] #django_models.Version.objects.filter(id__in=ionids)
    sourceids = []
    species_map = {}
    states_map = {}
    states = []
    
    #get sources, speed ok
    allsources = django_models.Versionsource.objects.all()
    #sources for each species version
    version_sources = {}
    for source in allsources :
      if source.version_id not in version_sources :
        version_sources[source.version_id] = [source.source_id]        
      else : 
        version_sources[source.version_id].append(source.source_id)

    
    for trans in transs:      
      trans.Sources = version_sources[trans.version_id]        
      for source in version_sources[trans.version_id]:      
        if source not in sourceids :
          sourceids.append(source)
          
      if trans.version_id not in species_map : 
          trans.version.States = []
          species_map[trans.version_id] = trans.version
        
      if trans.upperatomicstate_id not in states_map : 
        states_map[trans.upperatomicstate_id] = trans.upperatomicstate_id
        trans.upperatomicstate.Sources = version_sources[trans.version_id]
        trans.upperatomicstate.Components = []
        trans.upperatomicstate.Components.append(getCoupling(trans.upperatomicstate))
        species_map[trans.version_id].States.append(trans.upperatomicstate)
        states.append(trans.upperatomicstate)
        
        
      if trans.loweratomicstate_id not in states_map : 
        states_map[trans.loweratomicstate_id] = trans.loweratomicstate_id
        trans.loweratomicstate.Sources = version_sources[trans.version_id]
        trans.loweratomicstate.Components = []
        trans.loweratomicstate.Components.append(getCoupling(trans.loweratomicstate))        
        species_map[trans.version_id].States.append(trans.loweratomicstate)
        states.append(trans.loweratomicstate)
    
    for key, value in species_map.items():
      species.append(value)  

    #~ print("--- %s seconds ---" % (time.time() - start_time))
    return species, states, sourceids 
    

   

def getSources(ids):
    """
        get a list of source objects from their ids    

        Returns all sources if ids == None
    """
    if ids is None : 
      sources = django_models.Source.objects.all()
    else : 
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
  if str(sql).strip().lower() == 'select species': 
    return setupSpecies()
  # return all sources
  elif str(sql).strip().lower() == 'select sources': 
    return setupSources()
    
  # all other requests
  else : 
    q = sql2Q(sql)
    transs = django_models.Radiativetransition.objects.filter(q)

    if sql.HTTPmethod == 'HEAD':
      return {'HeaderInfo':returnHeaders(transs)}
    else : 
      return setupVssRequest(transs, q)			

    
def returnHeaders(transs):

  ntranss=transs.count()
  headers={'COUNT-RADIATIVE': ntranss}
  
  if ntranss:
      headers['APPROX-SIZE']='%.2f'%(ntranss*0.0014 + 0.01)
  else:
      headers['APPROX-SIZE']='0.00'
    
  if TRANSLIM < ntranss:
    headers['TRUNCATED'] = '%.1f'%(float(TRANSLIM)/ntranss *100)

  sp_ids = transs.values_list('version').distinct()
  headers['COUNT-SPECIES'] = len(sp_ids)

  sids = transs.values_list('upperatomicstate','loweratomicstate')
  sids = set(item for s in sids for item in s)
  headers['COUNT-STATES'] = len(sids)
  
  if LAST_MODIFIED is not None : 
    headers['LAST-MODIFIED'] = LAST_MODIFIED

  return headers


def setupVssRequest(transs, q):
  """
  This function is always called by the software.
  """
  ntranss=transs.count() 
  percentage=None

  if ntranss > TRANSLIM :
    transs, percentage = truncateTransitions(transs, q, TRANSLIM)    

  species, states, sourceids = getSpeciesWithStates(transs)
  nstates = len(states)
  
  radcross = []  
  for state in states :
    if state.xdata is not None : 
      radcross.append(state)
      
  nspecies = len(species)              
  sources = getSources(sourceids)
  nsources = sources.count()
  nstates = len(states)

  headerinfo = {
    'COUNT-RADIATIVE': ntranss,
    'COUNT-SPECIES' : nspecies,
    'COUNT-STATES' : nstates,
  }
  
  if percentage is not None : 
    headerinfo['TRUNCATED'] = percentage
    
  if LAST_MODIFIED is not None : 
    headerinfo['LAST-MODIFIED'] = LAST_MODIFIED
    
  return {
    'HeaderInfo' : headerinfo,
    'RadTrans':transs,
    'Atoms':species, 
    'RadCross':radcross,     
    'Sources':sources,        
  }


  return result
    
def setupSpecies():
  """		
    Return all target species
    @rtype:  dict
    @return:  Result object		
  """
  ids = django_models.Radiativetransition.objects.all().values_list('version', flat=True)
  versions = django_models.Version.objects.filter(pk__in = ids)
  result = {'HeaderInfo':{'COUNT-SPECIES': len(versions), },
            'Atoms':versions,  
          }
  return result    


def setupSources():
  """		
    Return all sources
    @rtype:   util_models.Result
    @return:  Result object		
  """
  
  # get  all sources
  sources = getSources(None)
  result = {'HeaderInfo':{'COUNT-SOURCES': len(sources), },
            'Sources':sources,  
          }
  return result    

	

