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
from vamdctap.sqlparse import where2q

import dictionaries
from models import *

import logging
log = logging.getLogger('vamdc.node.queryfu')


class EmptyClass:
    """Empty class to add attributes dynamically to"""

def setupResults(sql):
    """
    This function is always called by the software.
    """
    # log the incoming query
    log.debug('sql input: %s'%sql)

    # convert the incoming sql to a correct django query syntax object 
    # based on the RESTRICTABLES dictionary in dictionaries.py
    # (where2q is a helper function to do this for us).
    q = where2q(sql.where, dictionaries.RESTRICTABLES)
    try: 
        q = eval(q) # test queryset syntax validity
    except: 
        return {}

    #react_ds = RxnData.objects.filter(pk__in=(2,4,3862,3863,7975,7976))
    react_ds = RxnData.objects.filter(q, network_id=3)

    # count the number of matches, make a simple trunkation if there are
    # too many (record the coverage in the returned header)
    nreacts=react_ds.count()
    log.debug('number of reaction data: %s'%nreacts)

    #sources = Source.objects.filter(pk__in=set(react_ds.values_list('ref_id', flat=True))) 
    sources = SourceAll.objects.filter(abbr__in=set(react_ds.values_list('ref_id', flat=True))) 
    #for source in sources:
    #    if source.authors:
    #        source.authorlist = source.authors.split('|')
    #    else:
    #        source.authorlist = []

    nsources = sources.count()

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

        # Add the rate coefficient at 10K as a data table
        #data = []
        rea.DataSets = []
        dataset = EmptyClass()
        #dataRow = EmptyClass()
        #dataRow.xdata = '10'
        #dataRow.ydata = str(rea.r10kr)

        #dataRow.xdataunit = 'K'
        #dataRow.ydataunit = 'cm3/sec'
        #dataRow.datadescription = 'Rate Coefficient at 10K'
        #data.append(dataRow)


        # Fit Function data
        #fitdata = []
        #fitDataRow = EmptyClass()
        #fitDataRow.fitfunctionref = '12345' # Hard wired for the time being to non-existent function.
        #                                    # We need to use the reaction type to generate the correct
        #                                    # formula.  And we may need to add the formulae to the db.
        #fitdata.append(fitDataRow)

        fitDataClass = EmptyClass()

        fitDataArgument = EmptyClass()
        fitDataArguments = []

        fitDataArgument.tmin = rea.tmin
        fitDataArgument.tmax = rea.tmax
        fitDataArgument.description = 'Temperature'
        fitDataArguments.append(fitDataArgument)

        fitDataParameter = EmptyClass()
        fitDataParameters = []

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


        #fitDataClass.fitdata = fitdata
        fitDataClass.Arguments = fitDataArguments
        fitDataClass.Parameters = fitDataParameters
        fitDataClass.functionref = rea.rt.function_id
        fitDataClass.clem = rea.clem

        fitDataClass.sourceref = sources.filter(abbr=rea.ref.abbr).values_list('id', flat=True)

        fitDataClass.acc = rea.accuracy

        #dataset.TabData = data
        dataset.FitData = [fitDataClass]
        #dataset.Description = dataRow.datadescription
        #dataset.Ref = rea.ref.abbr
        dataset.Ref = sources.filter(abbr=rea.ref.abbr).values_list('id', flat=True)


        rea.DataSets.append(dataset)





    log.debug('done setting up the QuerySets')
    # Create the header with some useful info. The key names here are
    # standardized and shouldn't be changed.
    headerinfo={\
            'COUNT-ATOMS':atoms.count(),
            'COUNT-MOLECULES':molecules.count(),
            'COUNT-COLLISIONS':nreacts,
            }

    # Return the data. The keynames are standardized. 
    # 2012-02-14 KWS As per Guy's message - return an empty dict if there is no data.
    if nreacts > 0:
        return {\
                'CollTrans':react_ds,
                'Atoms':atoms,
                'Molecules':molecules,
                'Particles':particles,
                'Sources':sources,
                'HeaderInfo':headerinfo,
                'Functions':functions,
                'Methods':methods
               }
    else:
        return {}
