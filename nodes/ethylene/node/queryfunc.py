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

from django.db.models import Q
from vamdctap.sqlparse import *
from dictionaries import *
from models import *
from itertools import chain

import logging
log=logging.getLogger('vamdc.node.queryfu')

LIMIT = 100000

def getRefs(transitions):
    refset = set()
    for t in transitions.values_list('wavenumber_sourceid', 'intensity_sourceid',
                                     'gamma1_sourceid','delta1_sourceid','nexp1_sourceid',
                                     'gamma2_sourceid','delta2_sourceid','nexp2_sourceid',
                                     'gamma3_sourceid','delta3_sourceid','nexp3_sourceid',
                                     'gamma4_sourceid','delta4_sourceid','nexp4_sourceid',
                                     'gamma5_sourceid','delta5_sourceid','nexp5_sourceid',
                                     'gamma6_sourceid','delta6_sourceid','nexp6_sourceid',
                                     'gamma7_sourceid','delta7_sourceid','nexp7_sourceid',
                                     'gamma8_sourceid','delta8_sourceid','nexp8_sourceid',
                                     'gamma9_sourceid','delta9_sourceid','nexp9_sourceid'):
        refset = refset.union(t)

    # Use the found reference keys to extract the correct references from the References table.
    refmatches = Sources.objects.filter(pk__in=refset) # only match primary keys in refset
    return refmatches

def getMethods(transitions):
    mids = set( transitions.values_list('typeid',flat=True) )
    methods = TransitionTypes.objects.filter(pk__in=mids)
    return methods

def getMolecules(transitions):
    spids = set( transitions.values_list('isotopeid',flat=True) )
    isotopes = MoleculesIsotopes.objects.filter(pk__in=spids)
    nisotopes = isotopes.count()
    return isotopes,nisotopes

def getStates(transitions,isotopes,addStates,addBStates):
    nstates = 0

    if addStates:
        for isotope in isotopes:
            # States
            subtransitions = transitions.filter(isotopeid=isotope)
            up = subtransitions.values_list('upstateid',flat=True)
            lo = subtransitions.values_list('lowstateid',flat=True)
            eos = (isotope.eostateid,)
            sids = set(chain(up,lo,eos))
            isotope.States = MolecularStates.objects.filter(stateid__in = sids)
            if addBStates:
                # BasisStates
                sublevids = set()
                for MS in isotope.States:
                    sublevids = sublevids.union( (MS.sublevid1_id, MS.sublevid2_id, MS.sublevid3_id, MS.sublevid4_id)[:MS.nbcoefn0] )
                isotope.BasisStates = VibrationalSublevels.objects.filter(pk__in=sublevids)
            #
            nstates += len(sids)

    return nstates

####################################################################################################

def setupResults(sql):
    """
      This function is always called by the software.
    """
    log.debug('sql.where: %s'%sql.where)
    q = sql2Q(sql)

    # RadTrans
    transitions = Transitions.objects.filter(q).order_by('wavenumber')
    ntransitions = transitions.count()

    # LIMIT
    if ntransitions > LIMIT:
        percentage = '%.1f'%(float(LIMIT)/ntransitions *100)
        limitwave = transitions[LIMIT].wavenumber
        transitions = Transitions.objects.filter(q,Q(wavenumber__lt=limitwave))
    else: percentage=None

    # Molecules
    isotopes,nisotopes = getMolecules(transitions)

    # States and BasisStates
    addStates  = ( not sql.requestables or 'moleculestates' in sql.requestables )
    addBStates = ( not sql.requestables or ('moleculebasisstates' in sql.requestables) or ('moleculequantumnumbers' in sql.requestables) )
    nstates = getStates(transitions,isotopes,addStates,addBStates)

    # Sources
    sources = getRefs(transitions)
    nsources = sources.count()

    # Methods
    methods = getMethods(transitions)

    # APPROX-SIZE
    if ntransitions:
        size = 0
        if( not sql.requestables or 'radiativetransitions' in sql.requestables ):
            size += ntransitions*0.000825
        if( not sql.requestables or 'moleculestates' in sql.requestables ):
            size += nstates*0.000310
        if( not sql.requestables or 'moleculequantumnumbers' in sql.requestables ):
            size += nstates*0.000493
        size_estimate='%.2f'%(size)
    else: size_estimate='0.00'

    # HEADERINFO
    headerinfo=CaselessDict({\
            'TRUNCATED':percentage,
            'COUNT-SOURCES':nsources,
            'COUNT-SPECIES':nisotopes,
            'COUNT-MOLECULES':nisotopes,
            'COUNT-STATES':nstates,
            'COUNT-RADIATIVE':ntransitions,
            'APPROX-SIZE':size_estimate
            })

    if (ntransitions > 0):
        return {'RadTrans':transitions,
                'Molecules':isotopes,
                'Sources':sources,
                'Methods':methods,
                'Environments': [1],
                'HeaderInfo':headerinfo
               }
    else:
        return {}

