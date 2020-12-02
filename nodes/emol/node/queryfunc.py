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


    #collisions = models.Collision.objects.filter(q)

    #reactantids = set(collisions.values_list('reactant', flat=True))
    #productids  = set(collisions.values_list('product',  flat=True))
    #molids = chain(reactantids, productids)   
    #molecules = models.Species.objects.filter(pk__in=molids)
    molecules = models.Molspecies.objects.filter(q)
    nspecies = molecules.count
    nstates  = 0

    #for coll in collisions:
    #    coll.Reactants = models.Species.objects.filter(pk=coll.reactant.id)
    #    coll.Products  = models.Species.objects.filter(pk=coll.product.id)
    #    coll.DataSets  = models.DataSet.objects.filter(pk=coll.id)
    #    for dataset in coll.DataSets:
    #       dataset.TabData = models.TabData.objects.filter(dataset_id=coll.id)
    #ncoll = collisions.count
    ntrans = 0;

    nsources = 0

    # standardized and shouldn't be changed.
    headerinfo = {'COUNT-SOURCES':nsources,
                  'COUNT-SPECIES':nspecies,
                  'COUNT-STATES':nstates,
                  'COUNT_RADIATIVE':ntrans}

    # Return the data. The keynames are standardized.
    return {#'CollTrans'  : collisions,
            'Molecules'  : molecules}
