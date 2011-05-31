# -*- coding: utf-8 -*-
#
# This module (which must have the name queryfunc.py) is responsible
# for converting incoming queries to a database query understood by
# this particular node's database schema.
# 

# library imports 

import sys
from itertools import chain
from django.conf import settings
from vamdctap.sqlparse import where2q

import dictionaries
import models # this imports models.py from the same directory as this file

import logging
log = logging.getLogger('vamdc.node.queryfu')

def setupResults(sql):
    """
    This function is always called by the software.
    """
    # log the incoming query
    log.debug('sql input: %s'%sql)

    # convert the incoming sql to a correct django query syntax object 
    # based on the RESTRICTABLES dictionary in dictionaries.py
    # (where2q is a helper function to do this for us).
    #q = where2q(sql.where, dictionaries.RESTRICTABLES)
    #try: 
    #    q = eval(q) # test queryset syntax validity
    #except: 
    #    return {}

    # We build a queryset of database matches on the Transision model
    # since through this model (in our example) we are be able to
    # reach all other models. Note that a queryset is actually not yet
    # hitting the database, making it very efficient.

    # UMIST database code

    react_ds = models.RxnData.objects.all()[:10]
    #react_ds = models.RxnData.objects.filter(q)

    # count the number of matches, make a simple trunkation if there are
    # too many (record the coverage in the returned header)
    nreacts=react_ds.count()
    log.debug('number of reaction data: %s'%nreacts)

    sources = Source.objects.filter(pk__in=set(react_ds.values_list('ref_id', flat=True))) 
    nsources = sources.count()

    reacts = Reaction.objects.filter(pk__in=set(react_ds.values_list('reaction_id', flat=True)))
    species = Species.objects.filter(pk__in=reacts.values_list('species'))
    atoms = species.filter(type=1)
    molecules = species.filter(type=2)
    particle = species.filter(type=3)

    # Create the header with some useful info. The key names here are
    # standardized and shouldn't be changed.
    headerinfo=CaselessDict({\
            'COUNT-ATOMS':atoms.count(),
            'COUNT-MOLECULES':molecules.count(),
            'COUNT-COLLISIONS':nreact,
            })
    # Return the data. The keynames are standardized. 
    return {\
            'CollTrans':react_ds,
            'Atoms':atoms,
            'Molecules':molecules,
            'Particles':particles,
            'Sources':sources,
            'HeaderInfo':headerinfo,
            #'Methods':methods
            #'Functions':functions
           }
