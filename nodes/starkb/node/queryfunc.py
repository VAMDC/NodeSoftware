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
from vamdctap.sqlparse import where2q
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import logging
log=logging.getLogger('vamdc.tap')

import dictionaries
import models # this imports models.py from the same directory as this file

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
            nstates += specie.States.count() 
        except ObjectDoesNotExist as e:
            log.debug(str(e)) # this species is a collider

    nspecies = len(species) # get some statistics 
    return species, nspecies, nstates
    
        
def getEnvironments(transs):
    """
        Returns all the environments corresponding to the list of transitions
        @type  transs: list
        @param transs: a list of Transition
        @rtype:   list
        @return:  a list of TemperatureCollider
    """
    allenvironments = []
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
        #trans.ShiftingParams = shiftings        
    
    return allenvironments

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
            
 

def setupResults(sql, limit=1000):
    """
    This function is always called by the software.
    """
    # convert the incoming sql to a correct django query syntax object 
    # based on the RESTRICTABLES dictionary in dictionaries.py
    # (where2q is a helper function to do this for us).
    q = where2q(sql.where, dictionaries.RESTRICTABLES)    
    try:         
        q = eval(q) # test queryset syntax validity        
    except Exception as e: 
        return {}

    # We build a queryset of database matches on the Transision model
    # since through this model (in our example) we are be able to
    # reach all other models.
    transs = models.Transition.objects.filter(q)
    
    # count the number of matches, make a simple trunkation if there are
    # too many (record the coverage in the returned header)
    ntranss=transs.count()       
    if limit < ntranss :
        transs = transs[:limit]
        percentage='%.1f' % (float(limit) / ntranss * 100)
    else: 
        percentage=None
        
    # Through the transition-matches, use our helper functions to extract 
    # all the relevant database data for our query. 
    #sources = getRefs(transs)
    #nsources = sources.count()
    
    #if ntranss > 0 :
    species, nspecies, nstates = getSpeciesWithStates(transs)           
    environments = getEnvironments(transs)    
    particles = getParticles(ntranss) 

    # Create the header with some useful info. The key names here are
    # standardized and shouldn't be changed.
    headerinfo={\
            'Truncated':percentage,
            #'COUNT-SOURCES':nsources,
            'COUNT-species':nspecies,
            'count-states':nstates,
            'count-radiative':ntranss
            }
            
    # Return the data. The keynames are standardized. 
    return {'RadTrans':transs,
            'Atoms':species,
            'Environments':environments,
            'Particles' : particles,
            #'Sources':sources,
            'HeaderInfo':headerinfo,
            #'Methods':methods
            #'Functions':functions
           }   
    

