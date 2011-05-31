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

#------------------------------------------------------------
# Helper functions (called from setupResults)
#------------------------------------------------------------

def getSpeciesWithStates(transs):
    """
    Use the Transition matches to obtain the related Species (only atoms in this example)
    and the states related to each transition. 
    We also return some statistics of the result 
    """

    # get the reference ids for the 'species' ForeignKey field 
    # (see getRefs comment for more info)
    spids = set( transs.values_list('species_id',flat=True) )
    # use the reference ids to query the Species database table 
    species = models.Species.objects.filter(pk__in=spids)
    nspecies = species.count() # get some statistics 

    # get all states. Note that when building a queryset like this,
    # (using objects.filter() etc) will usually not hit the database
    # until it's really necessary, making this very efficient. 
    nstates = 0
    for spec in species:
        # get all transitions in linked to this particular species 
        spec_transitions = transs.filter(species=spec)
        # extract reference ids for the states from the transion, combining both
        # upper and lower unique states together
        up = spec_transitions.values_list('upstate_id',flat=True)
        lo = spec_transitions.values_list('lostate_id',flat=True)
        sids = set(chain(up, lo))

        # use the found reference ids to search the State database table 
        # Note that we store a new queryset called 'States' on the species queryset. 
        # This is important and a requirement looked for by the node 
        # software (all RETURNABLES AtomState* will try to loop over this
        # nested queryset). 
        spec.States = models.State.objects.filter( pk__in = sids )    
        nstates += spec.States.count()
    return species, nspecies, nstates

def getFunctions(transs):
    """
    Obtain function expressions for correcting/adjusting certain transitions
    In this example, such expressions are stored on the form e.g.  y = a * x + b * z
    where we have max 3 arguments and 3 parameters
    We assume all arguments (x,y,z ...) and all parameters (a,b,c) are unitless. 
    """
    import re # regular expressions 
    funcs = transs.values_list("function", flat=True)
    for func in funcs: 
        func = re.sub(r"\s", "", func) # remove all whitespace in the expresion
        fy, rest = func.split('=', 1)
        fargs = re.findall(r"a|b|c", func)
        fpars = re.findall(r"x|y|z", func)
        func.id = func
        func.name = "Correction"
        func.expression = func
        func.y = fy
        func.yunit = "unitless"
        for arg in fargs: 
            func.Arguments.name = arg
            func.Arguments.lower_limit = 0.0
            func.Arguments.upper_limit = 1.0
        for par in fpars:
            func.Parameters.name = par
    return funcs



#------------------------------------------------------------
# Main function 
#------------------------------------------------------------

def setupResults(sql):
    """
    This function is always called by the software.
    """
    # log the incoming query
    log('sql input: %s'%sql)

    # convert the incoming sql to a correct django query syntax object 
    # based on the RESTRICTABLES dictionary in dictionaries.py
    # (where2q is a helper function to do this for us).
    q = where2q(sql.where, dictionaries.RESTRICTABLES)
    try: 
        q = eval(q) # test queryset syntax validity
    except: 
        return {}

    # We build a queryset of database matches on the Transision model
    # since through this model (in our example) we are be able to
    # reach all other models. Note that a queryset is actually not yet
    # hitting the database, making it very efficient.

    # UMIST database code

    react_ds = models.RxnData.objects.filter(q)

    # count the number of matches, make a simple trunkation if there are
    # too many (record the coverage in the returned header)
    nreacts=reacts.count()

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
            'COUNT-ATOMS':nsources,
            'COUNT-MOLECULES':nspecies,
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
