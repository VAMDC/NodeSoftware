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
    log.debug("species with states")
    # get ions according to selected transitions
    ionids = transs.values_list('version', flat=True).distinct()
    species = models.Version.objects.filter(id__in=ionids)
    #nspecies = species.count() # get some statistics
    log.debug(connection.queries)
    # get all states.
    nstates = 0

    for specie in species:
        log.debug("test 1")
        # get all transitions in linked to this particular species
        spec_transitions = transs.filter(version=specie.id)
        log.debug('test 2')
        # extract reference ids for the states from the transion, combining both
        # upper and lower unique states together
        up = spec_transitions.values_list('initialatomicstate',flat=True)
        lo = spec_transitions.values_list('finalatomicstate',flat=True)
        sids = set(chain(up, lo))

        # use the found reference ids to search the State database table
        # Note that we store a new queryset called 'States' on the species queryset.
        # This is important and a requirement looked for by the node
        # software
        specie.States = models.Atomicstate.objects.filter( pk__in = sids )
        for state in specie.States :
            state.Component = getCoupling(state)
        nstates += specie.States.count()
    return species, nstates

def getCoupling(state):
    """
    Get coupling for the given state
    """
    components = models.Atomiccomponent.objects.filter(atomicstate=state)
    for component in components:
        component.Lscoupling = models.Lscoupling.objects.get(atomiccomponent=component)
    return components[0]


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

    # We build a queryset of database matches on the Transision model
    # since through this model (in our example) we are be able to
    # reach all other models.
    transs = models.Radiativetransition.objects.filter(q)

    # count the number of matches, make a simple trunkation if there are
    # too many (record the coverage in the returned header)
    ntranss=transs.count()

    if limit < ntranss :
        #transs = transs[:limit]
        percentage='%.1f' % (float(limit) / ntranss * 100)
        transs = transs.order_by('wavelength')
        newmax = transs[limit].wavelength
        transs = models.Radiativetransition.objects.filter(q,Q(wavelength__lt=newmax))
        log.debug('Truncated results to %s, i.e %s A.'%(limit,newmax))
    else:
        percentage=None

    # Through the transition-matches, use our helper functions to extract
    # all the relevant database data for our query.
    #sources = getRefs(transs)
    #nsources = sources.count()
    species, nstates = getSpeciesWithStates(transs)


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
            'count-radiative':ntranss
            }

    # Return the data. The keynames are standardized.
    return {'RadTrans':transs,
            'Atoms':species,
            'RadCross' : states,
            #'Sources':sources,
            'HeaderInfo':headerinfo,
            #'Methods':methods
            #'Functions':functions
           }
