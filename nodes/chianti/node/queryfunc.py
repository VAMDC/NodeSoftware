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
from vamdctap.sqlparse import sql2Q

import dictionaries
import models # this imports models.py from the same directory as this file

def LOG(s):
    "Simple logger function"
    print >> sys.stderr, s

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

def getSpeciesWithStates(transs, sql):
    """
    Use the Transition matches to obtain the related Species (only atoms in this example)
    and the states related to each transition. 
    
    We also return some statistics of the result 
    """

    # get the reference ids for the 'species' ForeignKey field 
    # (see getRefs comment for more info)
    spids = set( transs.values_list('finalstateindex__species',flat=True) )
    #print spids
    # use the reference ids to query the Species database table 
    species = models.Species.objects.filter(pk__in=spids)
    nspecies = species.count() # get some statistics 
    #print 'nspecies = %d\n'%nspecies

    # List the IDs (i.e. keys from the states table) of all the states 
    # connected with all the selected transitions.
    stateIds = set().union(transs.values_list('initialstateindex', flat=True), transs.values_list('finalstateindex', flat=True))

    # get all states. Note that when building a queryset like this,
    # (using objects.filter() etc) will usually not hit the database
    # until it's really necessary, making this very efficient. 
    #LOG("Getting states")
    nstates = 0
    if statesRequired(sql):
        for spec in species:
            # use the found reference ids to search the State database table 
            # Note that we store a new queryset called 'States' on the species queryset. 
            # This is important and a requirement looked for by the node 
            # software (all RETURNABLES AtomState* will try to loop over this
            # nested queryset). 
            spec.States = models.States.objects.filter(species=spec).filter(pk__in=stateIds)
            #for state in spec.States:
            #     state.Components = models.Components.objects.filter(pk=state.id)
            #     for comp in state.Components:
            #         comp.Shells = models.Subshells.objects.filter(state=state.id)
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


def getMethods():    
    """
    Chianti has a mix of theor
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
    m1 = Method("EXP", "experiment")
    m2 = Method("THEO", "theory")
    return m1, m2


def everythingRequired(sql):
    return len(sql.requestables) == 0


def transitionsRequired(sql):
    return 'radiativetransitions' in sql.requestables or everythingRequired(sql)


def statesRequired(sql):
    return 'atomstates' in sql.requestables or everythingRequired(sql)

def constraintsPresent(sql):
    return len(sql.where) > 0


def getSources(species):
    speciesIds = species.values_list('id', flat=True)
    return models.Sources.objects.filter(species__in=speciesIds)


#------------------------------------------------------------
# Main function 
#------------------------------------------------------------

def setupResults(sql, limit=100000):
    LOG('setupResults()')
    try:
        return query(sql, limit)
    except Exception as oops:
        LOG(oops)
        raise oops


def query(sql, limit):

    # log the incoming query
    LOG(sql)

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
    
    sources = getSources(species)
    #sources = models.Sources.objects.all()
    #sources = None;

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
            'count-radiative':ntranss
            }
    LOG(headerinfo)
            
    # Return the data. The keynames are standardized.
    if (nspecies > 0 or nstates > 0 or ntranss > 0):
        return {'RadTrans'  : transs,
                'Atoms'     : species,
                'HeaderInfo': headerinfo,
                'Methods'   : getMethods(),
                'Sources'   : sources
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

    #LOG("Generic query")

    # We build a queryset of database matches on the Transision model
    # since through this model (in our example) we are be able to
    # reach all other models. Note that a queryset is actually not yet
    # hitting the database, making it very efficient.
    #LOG("getting transitions")
    transs = models.Transitions.objects.filter(q)

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
    #LOG("Getting species")
    species, nspecies, nstates = getSpeciesWithStates(transs, sql)
    #LOG(species)

    return species, nstates, transs, percentage

def allSpeciesQuery(sql, q, limit):
    #LOG("All-species query")
    return models.Species.objects.all()
