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
import models # this imports models.py from the same directory as this file




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
    species = models.Version.objects.filter(id__in=ionids)
    # get all states.
    nstates = 0

    for trans in transs :
        setSpecies(trans)
        setDataset(trans)

    for specie in species:
        # get all transitions in linked to this particular species
        spec_transitions = transs.filter(version=specie.id)
        # extract reference ids for the states from the transion, combining both
        # upper and lower unique states together
        up = spec_transitions.values_list('initialatomicstate',flat=True)
        lo = spec_transitions.values_list('finalatomicstate',flat=True)
        sids = set(chain(up, lo))

        # use the found reference ids to search the State database table
        specie.States = models.Atomicstate.objects.filter( pk__in = sids )
        for state in specie.States :
            state.Component = getCoupling(state)
        nstates += specie.States.count()
    return species, nstates

    
def setDataset(trans):
    """
     create Dataset with Tabulated data
    """
    data = models.Tabulateddata.objects.filter(collisionaltransition = trans.id)
    if data[0].xdata is not None : 
        trans.DataSets = []
        dataset = models.Dataset()
        dataset.TabData = data
        dataset.Description = data[0].datadescription.value
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
    particle = models.Particle.objects.filter(name='electron') # second reactant is always an electron for now
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
    components = models.Atomiccomponent.objects.filter(atomicstate=state)
    for component in components:
        component.Lscoupling = models.Lscoupling.objects.get(atomiccomponent=component)
    return components[0]
    
def getParticles():    
    return models.Particle.objects.all()
    
    
def truncateTransitions(transitions, request, maxTransitionNumber):
    """
    Limit the number of transitions when it is too high
    """
    percentage='%.1f' % (float(maxTransitionNumber) / transitions.count() * 100)
    transitions = transitions.order_by('initialatomicstate__stateenergy')
    newmax = transitions[maxTransitionNumber].initialatomicstate.stateenergy
    return models.Collisionaltransition.objects.filter(request,Q(initialatomicstate__stateenergy__lt=newmax)), percentage

    

#------------------------------------------------------------
# Main function 
#------------------------------------------------------------
def setupResults(sql, limit=1000):
    """
    This function is always called by the software.
    """
    # log the incoming query
    log.debug(sql)

    # convert the incoming sql to a correct django query syntax object 
    # based on the RESTRICTABLES dictionary in dictionaries.py
    q = sql2Q(sql)   
    
    transs = models.Collisionaltransition.objects.filter(q)
    # count the number of matches, make a simple trunkation if there are
    # too many (record the coverage in the returned header)
    ncoll=transs.count()
    if limit < ncoll :
        transs, percentage = truncateTransitions(transs, q, limit)
    else:
        percentage=None

    # Through the transition-matches, use our helper functions to extract
    # all the relevant database data for our query.
    #sources = getRefs(transs)
    #nsources = sources.count()
    species, nstates = getSpeciesWithStates(transs)
    # electron collider
    particles = getParticles()

    # cross sections
    states = []
    for specie in species:
        states.extend(specie.States)
    
    # Create the header with some useful info. The key names here are
    # standardized and shouldn't be changed.
    headerinfo={\
            'Truncated':percentage,
            #'COUNT-SOURCES':nsources,
            'count-states':nstates,
            'count-collisions':ncoll
            }

    # Return the data. The keynames are standardized.
    return {'CollTrans':transs,
            'Atoms':species,
            'Particles' : particles,
            #'Sources':sources,
            'HeaderInfo':headerinfo,
            #'Methods':methods
            #'Functions':functions
           }
