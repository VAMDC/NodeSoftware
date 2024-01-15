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
import logging
from itertools import chain
from django.conf import settings
from django.db.models import Q 
from vamdctap.sqlparse import sql2Q

from . import dictionaries
from . import models

log = logging.getLogger('tignanello_queryfunc')

#------------------------------------------------------------
# Helper functions (called from setupResults)
#------------------------------------------------------------

def getSpeciesWithStates(transs, sql):
    """
    Use the Transition matches to obtain the related Species (only atoms in this example)
    and the states related to each transition. 
    
    We also return some statistics of the result 
    """

    # get the reference ids for the 'species' ForeignKey field 
    # (see getRefs comment for more info)
    spids = set( transs.values_list('finalstateindex__species',flat=True) )
    # use the reference ids to query the Species database table 
    species = models.Species.objects.filter(pk__in=spids)
    nspecies = species.count() # get some statistics 

    # List the IDs (i.e. keys from the states table) of all the states 
    # connected with all the selected transitions.
    stateIds = set().union(transs.values_list('initialstateindex', flat=True), transs.values_list('finalstateindex', flat=True))

    # get all states. Note that when building a queryset like this,
    # (using objects.filter() etc) will usually not hit the database
    # until it's really necessary, making this very efficient. 
    log.debug("Getting states")
    nstates = 0
    if statesRequired(sql):
        for spec in species:
            # use the found reference ids to search the State database table 
            # Note that we store a new queryset called 'States' on the species queryset. 
            # This is important and a requirement looked for by the node 
            # software (all RETURNABLES AtomState* will try to loop over this
            # nested queryset). 
            spec.States = models.States.objects.filter(species=spec).filter(pk__in=stateIds)

    return species, nspecies, nstates


def everythingRequired(sql):
    return len(sql.requestables) == 0


def transitionsRequired(sql):
    return 'radiativetransitions' in sql.requestables or everythingRequired(sql)


def statesRequired(sql):
    return 'atomstates' in sql.requestables or everythingRequired(sql)

def constraintsPresent(sql):
    return len(sql.where) > 0



#------------------------------------------------------------
# Main function 
#------------------------------------------------------------

def setupResults(sql, limit=100000):
    log.warning('queryfunc')
    try:
        return query(sql, limit)
    except Exception as oops:
        log.error(oops)
        raise oops


def query(sql, limit):

    # log the incoming query
    log.debug(sql)

    # convert the incoming sql to a correct django query syntax object 
    # based on the RESTRICTABLES dictionary in dictionaries.py
    q = sql2Q(sql)

    if constraintsPresent(sql) or transitionsRequired(sql) or statesRequired(sql):
        species, nstates, transs, percentage = genericQuery(sql, q, limit)
        nspecies = species.count()
        ntranss = transs.count()
    else:
        species = allSpeciesQuery(sql, q, limit)
        nspecies = species.count()
        nstates = 0
        ntranss = 0
        transs = {}
        percentage = None
    
    # Adjust the counts of things returned according to the requestables.
    # The caller will choose what actually to return, but we have to set
    # the counts in the header ourselves.
    if not transitionsRequired(sql):
        ntranss = 0
    if not statesRequired(sql):
        nstates = 0


    # Create the header with some useful info. The key names here are
    # standardized and shouldn't be changed.
    headerinfo={\
            'Truncated':percentage,
            'COUNT-species':nspecies,
            'count-states':nstates,
            'count-radiative':ntranss,
            'last-modified' : '2013-08-31T21:30:00+00:00'
            }
    log.info(headerinfo)
            
    # Return the data. The keynames are standardized.
    if (nspecies > 0 or nstates > 0 or ntranss > 0):
        return {'RadTrans'  : transs,
                'Atoms'     : species,
                'HeaderInfo': headerinfo,
               }

    # As a special case, if there are no data, return an empty structure.
    # This causes the node software to send a 204 "No content" response.
    else:
        return {}

def genericQuery(sql, q, limit):
    """
    When query constraints are present, this for mof query is used.
    The query initially selects the transitions and then builds matching
    sets of species and states. It has to be done this way because the
    retrictables dictionary contains object references from the Transitions
    table; the query sets cannot work on directly on the other tables.
    """

    log.debug("Generic query")

    # We build a queryset of database matches on the Transision model
    # since through this model (in our example) we are be able to
    # reach all other models. Note that a queryset is actually not yet
    # hitting the database, making it very efficient.
    log.debug("getting transitions")
    transs = models.Transitions.objects.select_related().filter(q)

    # count the number of matches, make a simple truncation if there are
    # too many (record the coverage in the returned header)
    # If we are constraining by transitions but not returning them,
    # do not truncate.
    ntranss=transs.count()    
    if limit < ntranss and transitionsRequired(sql):
        transs = transs[:limit]
        percentage='%.1f' % (float(limit) / ntranss * 100)
    else: 
        percentage=None

    # Through the transition-matches, use our helper functions to extract 
    # all the relevant database data for our query. 
    #sources = getRefs(transs)
    log.debug("Getting species")
    species, nspecies, nstates = getSpeciesWithStates(transs, sql)
    log.debug(species)

    return species, nstates, transs, percentage

def allSpeciesQuery(sql, q, limit):
    log.debug("All-species query")
    return models.Species.objects.all()
