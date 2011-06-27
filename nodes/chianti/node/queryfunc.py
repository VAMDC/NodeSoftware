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
from django.db.models import Q 
from vamdctap.sqlparse import where2q

import dictionaries
import models # this imports models.py from the same directory as this file

def LOG(s):
    "Simple logger function"
    if settings.DEBUG: print >> sys.stderr, s

#------------------------------------------------------------
# Helper functions (called from setupResults)
#------------------------------------------------------------

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

def getSpeciesWithStates(transs):
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

    # get all states. Note that when building a queryset like this,
    # (using objects.filter() etc) will usually not hit the database
    # until it's really necessary, making this very efficient. 
    nstates = 0
    for spec in species:
        # get all transitions in linked to this particular species 
        spec_transitions = transs.filter(finalstateindex__species=spec)
        # extract reference ids for the states from the transion, combining both
        # upper and lower unique states together
        up = spec_transitions.values_list('finalstateindex',flat=True)
        lo = spec_transitions.values_list('initialstateindex',flat=True)
        sids = set(chain(up, lo))

        # use the found reference ids to search the State database table 
        # Note that we store a new queryset called 'States' on the species queryset. 
        # This is important and a requirement looked for by the node 
        # software (all RETURNABLES AtomState* will try to loop over this
        # nested queryset). 
        spec.States = models.States.objects.filter( pk__in = sids )    
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


def getLifetimeMethods():    
    """
    In the example we are storing both experimental and theoretical
    data for some quantities, such as in the case of experimental or
    theoretical state lifetimes. A selector method on the model
    selects between these two, but need to then be able to tell us
    which was chosen. To differentiate between the two types, we
    create a "Method" class that we can reference from the model (and
    which will go into the XSAMS return). This is a simple python
    object with properties 'id' and 'category'.
     'id' - any string you want, but has to start with M.
     'category' - this is a valid Method.category as defined 
                  in the xsams definition online                
    """
    class Method(object):
        # simple dummy object to define a Method 
        def __init__(self, mid, category):
            self.id = mid
            self.category = category

    # we will only be needing two methods
    m1 = Method("MtauEXP", "experiment")
    m2 = Method("MtauTHEO", "compilation")
    return m1, m2


#------------------------------------------------------------
# Main function 
#------------------------------------------------------------

def setupResults(sql, limit=1000):
    """
    This function is always called by the software.
    """
    # log the incoming query
    LOG(sql)

    # convert the incoming sql to a correct django query syntax object 
    # based on the RESTRICTABLES dictionary in dictionaries.py
    # (where2q is a helper function to do this for us).
    q = where2q(sql.where, dictionaries.RESTRICTABLES)
    try: 
        q = eval(q) # test queryset syntax validity
    except Exception as e:
        LOG(e)
        return {}

    # We build a queryset of database matches on the Transision model
    # since through this model (in our example) we are be able to
    # reach all other models. Note that a queryset is actually not yet
    # hitting the database, making it very efficient.
    LOG("getting transitions")
    transs = models.Transitions.objects.select_related(depth=2).filter(q)
    LOG(transs.count())

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
    sources = {}
    nsources = 0
    LOG("Getting species")
    species, nspecies, nstates = getSpeciesWithStates(transs)
    #methods = getLifetimeMethods()
    methods = {}
    functions = {}
    LOG(species)

    # Create the header with some useful info. The key names here are
    # standardized and shouldn't be changed.
    headerinfo={\
            'Truncated':percentage,
            'COUNT-SOURCES':nsources,
            'COUNT-species':nspecies,
            'count-states':nstates,
            'count-radiative':ntranss
            }
    LOG(headerinfo)
            
    # Return the data. The keynames are standardized. 
    return {'RadTrans':transs,
            'Atoms':species,
            'Sources':sources,
            'HeaderInfo':headerinfo,
            'Methods':methods,
            'Functions':functions
           }
