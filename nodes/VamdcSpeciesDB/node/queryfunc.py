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

import logging
from itertools import chain

from vamdctap.sqlparse import sql2Q
from dictionaries import *

import models

log = logging.getLogger("vamdc.node.queryfu")

LIMIT = 1000

#------------------------------------------------------------
# Helper functions (called from setupResults)
#------------------------------------------------------------



#------------------------------------------------------------
# Main function
#------------------------------------------------------------

def setupResults(sql):
    """
    This function is always called by the NodeSoftware.
    """
    # log the incoming query
    log.debug(sql)

    # convert the incoming sql to a correct django query syntax object
    # (sql2Q is a helper function to do this for us).
    q = sql2Q(sql)
    import sys
    log.debug( "QQQQQ"+str(q) )
    # We build a queryset of database matches on the Transision model
    # since through this model (in our example) we are be able to
    # reach all other models. Note that a queryset is actually not yet
    # hitting the database, making it very efficient.
    species = models.VamdcSpecies.objects.select_related(depth=2).filter(q)

    # count the number of matches, make a simple trunkation if there are
    # too many (record the coverage in the returned header)
##    ntranss=transs.count()
##    if LIMIT < ntranss :
##        transs = transs[:limit]
##        percentage='%.1f' % (float(limit) / ntranss * 100)
##    else:
##        percentage=None
    
    # Through the transition-matches, use our helper functions to extract
    # all the relevant database data for our query.
#    sources = getRefs(transs)
#    nsources = sources.count()
#    species, nspecies, nstates = getSpeciesWithStates(transs)
#    methods = getLifetimeMethods()

    percentage = 100
    nsources = 0
    nspecies = species.count()
    nstates = 0
    ntranss = 0
    molecules = species.filter(species_type__name='Molecule')
    atoms = species.filter(species_type__name='Atom')
    
    # Create the header with some useful info. The key names here are
    # standardized and shouldn't be changed.
    headerinfo = {'TRUNCATED':percentage,
                  'COUNT-SOURCES':nsources,
                  'COUNT-SPECIES':nspecies,
                  'COUNT-STATES':nstates,
                  'COUNT_RADIATIVE':ntranss,
                  'APPROX-SIZE':nspecies*0.001 }

    # Return the data. The keynames are standardized.
    return {'Atoms':atoms,
            'Molecules':molecules,
            #'Sources':sources,
            'HeaderInfo':headerinfo,
            #'Methods':methods
            }
