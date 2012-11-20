# -*- coding: utf-8 -*-
#
# This module (which must have the name queryfunc.py) is responsible
# for converting incoming queries to a database query understood by
# this particular node's database schema.
# 

# library imports 

import sys
from django.db.models import Q
from django.conf import settings
from vamdctap.sqlparse import where2q, sql2Q

import dictionaries
from models import *

import logging
log = logging.getLogger('vamdc.node.queryfu')


class EmptyClass:
    """Empty class to add attributes dynamically to"""

def constrainedResults(sql, q, limit):
    """Return constrained results"""

    #react_ds = RxnData.objects.filter(pk__in=(2,4,3862,3863,7975,7976))
    # network_id=3 (UMIST RATE06 data only)
    react_ds = RxnData.objects.filter(q, network_id=3)

    log.debug('Number of reaction data rows: %s' % react_ds.count())

    sources = SourceAll.objects.filter(abbr__in=set(react_ds.values_list('ref_id', flat=True))) 

    # Get only the relevant reactions
    reacts = Reaction.objects.filter(pk__in=set(react_ds.values_list('reaction_id', flat=True)))

    # Get only the relevant species
    species = Species.objects.filter(pk__in=reacts.values_list('species'))

    atoms = species.filter(type=1)
    molecules = species.filter(type=2)
    particles = species.filter(type=3)

    # Grab the functions from the database
    functions = Functions.objects.all()
    functionparams = FunctionParamsArgs.objects.all()

    for func in functions:
        func.Arguments = FunctionParamsArgs.objects.filter(function_id=func.id, param_or_arg = 'A')
        func.Parameters = FunctionParamsArgs.objects.filter(function_id=func.id, param_or_arg = 'P')

    # Grab the methods from the database
    methods = Methods.objects.all()

    for rea in react_ds:
        rea.Reactants = rea.reaction.reactants.all()
        rea.Products = rea.reaction.products.all()

        rea.DataSets = []
        dataset = EmptyClass()

        # Add the rate coefficient at 10K as a data table
        # Commented this table out for the time being
        #data = []
        #dataRow = EmptyClass()
        #dataRow.xdata = '10'
        #dataRow.ydata = str(rea.r10kr)
        #dataRow.xdataunit = 'K'
        #dataRow.ydataunit = 'cm3/sec'
        #dataRow.datadescription = 'Rate Coefficient at 10K'
        #data.append(dataRow)

        fitDataClass = EmptyClass()

        fitDataArgument = EmptyClass()
        fitDataArguments = []

        fitDataArgument.tmin = rea.tmin
        fitDataArgument.tmax = rea.tmax
        fitDataArgument.description = 'Temperature'
        fitDataArguments.append(fitDataArgument)

        fitDataParameter = EmptyClass()
        fitDataParameters = []

        # Commented out example shows hard wired data. Below is data generated on the fly.
        #fitDataParameter.parameter = [rea.alpha, rea.beta, rea.gamma]
        #fitDataParameter.names = ['alpha', 'beta', 'gamma']
        #fitDataParameter.units = ['cm3/s', 'unitless', 'unitless']

        parameterNames = functionparams.filter(function_id=rea.rt.function_id, param_or_arg='P').values_list('name', flat=True)
        params = []
        for param in parameterNames:
            params.append(eval('rea.'+param))

        fitDataParameter.parameter = params
        fitDataParameter.names = parameterNames
        fitDataParameter.units = functionparams.filter(function_id=rea.rt.function_id, param_or_arg='P').values_list('units', flat=True)

        fitDataParameters.append(fitDataParameter)

        fitDataClass.Arguments = fitDataArguments
        fitDataClass.Parameters = fitDataParameters
        fitDataClass.functionref = rea.rt.function_id
        fitDataClass.clem = rea.clem

        fitDataClass.sourceref = sources.filter(abbr=rea.ref.abbr).values_list('id', flat=True)

        fitDataClass.acc = rea.accuracy

        #dataset.TabData = data
        dataset.FitData = [fitDataClass]
        #dataset.Description = dataRow.datadescription

        rea.DataSets.append(dataset)

    return react_ds, atoms, molecules, particles, sources, functions, methods



def speciesOnlyResults(sql, q, limit):

    """
    Get ALL the species.  Don't need the Q object for the time being.
    The code currently returns ONLY species for which we have an
    inchikey (more precisely, vamdc_species_id).
    The code is also required to return all Particles.
    """

    species = Species.objects.filter(Q(vamdc_species_id__isnull=False) | Q(type=3))

    atoms = species.filter(type=1)
    molecules = species.filter(type=2)
    particles = species.filter(type=3)

    return atoms, molecules, particles


def query(sql, limit):
    """
    Do the query.  Pass to the appropriate function depending on the type of query.
    """

    # log the incoming query
    log.debug('SQL input: %s' % sql)

    q = sql2Q(sql)

    #log.debug('Q: %s' % q)

    if len(sql.where) > 0:
        # It's a constrained query
        react_ds, atoms, molecules, particles, sources, functions, methods = constrainedResults(sql, q, limit)
        nsources = sources.count()
        nreacts = react_ds.count()
        nmolecules = molecules.count()
        natoms = atoms.count()
        nparticles = particles.count()
    elif ('%s' % sql).upper() == 'SELECT SPECIES':
        # Assume it's a species only query
        atoms, molecules, particles = speciesOnlyResults(sql, q, limit)
        methods = {}
        react_ds = {}
        sources = {}
        functions = {}
        methods = {}
        nreacts = 0
        nmolecules = molecules.count()
        natoms = atoms.count()
        nparticles = particles.count()
    else:
        return {}


    log.debug('Done setting up the QuerySets')
    # Create the header with some useful info. The key names here are
    # standardized and shouldn't be changed.
    headerinfo={\
            'COUNT-ATOMS':natoms,
            'COUNT-MOLECULES':nmolecules,
            'COUNT-SPECIES':nmolecules+natoms+nparticles,
            }

    # Return the data. The keynames are standardized. 
    # 2012-02-14 KWS As per Guy's message - return an empty dict if there is no data.
    if nreacts > 0:
        headerinfo['COUNT-COLLISIONS'] = nreacts
        return {\
                'HeaderInfo':headerinfo,
                'CollTrans':react_ds,
                'Atoms':atoms,
                'Molecules':molecules,
                'Particles':particles,
                'Sources':sources,
                'Functions':functions,
                'Methods':methods
               }
    elif nreacts == 0 and (nmolecules > 0 or natoms > 0 or nparticles > 0):
        return {\
                'HeaderInfo':headerinfo,
                'Atoms':atoms,
                'Molecules':molecules,
                'Particles':particles,
               }
    else:
        return {}


def setupResults(sql, limit = 100000):
    """
    This function is always called by the software.
    """

    try:
        return query(sql, limit)
    except Exception, e:
        log.debug(e)
        raise e


