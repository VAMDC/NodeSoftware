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

#LIMIT =  100
LIMIT = 100000

#def attach_state_qns(states):
#    for state in states:
#        state.parsed_qns = []
#        qns = MolecularQuantumNumbers.objects.filter(statesmolecules=state.stateid)
#        for qn in qns:
#            if qn.attribute:
#               attr_name, attr_val = qn.attribute.split('=')
#               qn.attribute = '%s=%s' % (attr_name, attr_val)
#            state.parsed_qns.append(MolecularQuantumNumbers(qn.stateid, qn.case, qn.label, qn.value, qn.attribute))

def getRefs(transs):
    refset = set()
    for t in transs.values_list('wavenumber_sourceid', 'intensity_sourceid',
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

def getMethods(transs):
    mids = set( transs.values_list('typeid',flat=True) )
    methods = TransitionTypes.objects.filter(pk__in=mids)
    return methods

def getStates(transs,addMoleStates):
    spids = set( transs.values_list('isotopeid',flat=True) )
    isotopes = MoleculesIsotopes.objects.filter(pk__in=spids)
    nisotopes = isotopes.count()
    nstates = 0

    if addMoleStates:
      for isotope in isotopes:
        subtranss = transs.filter(isotopeid=isotope)
        up=subtranss.values_list('upstateid',flat=True)
        lo=subtranss.values_list('lowstateid',flat=True)
        sids = set(chain(up,lo))
        isotope.States = MolecularStates.objects.filter(stateid__in = sids)
        nstates += len(sids)

    return isotopes,nisotopes,nstates

def setupResults(sql):
    """
      This function is always called by the software.
    """
    log.debug('sql.where: %s'%sql.where)
    q = sql2Q(sql)

    #e_transs = Transitions.objects.filter(q, Q(multipoleid__exact=1)).order_by('wavenumber')
    #non_transs = Transitions.objects.filter(q, Q(multipoleid__exact=2)).order_by('wavenumber')
    #transs = e_transs or non_transs

    transs = Transitions.objects.filter(q).order_by('wavenumber')
    ntranss = transs.count()

    if ntranss > LIMIT:
        percentage = '%.1f'%(float(LIMIT)/ntranss *100)
        limitwave = transs[LIMIT].wavenumber
        transs = Transitions.objects.filter(q,Q(wavenumber__lt=limitwave))
    else: percentage=None

    sources= getRefs(transs)
    nsources = sources.count()
    addMoleStates = (not sql.requestables or 'moleculestates' in sql.requestables)
    isotopes,nisotopes,nstates= getStates(transs,addMoleStates)
    methods = getMethods(transs)

    if ntranss:
        size_estimate='%.2f'%(nstates*0.000312+ntranss*0.000714)
    else: size_estimate='0.00'

    headerinfo=CaselessDict({\
            'TRUNCATED':percentage,
            'COUNT-SOURCES':nsources,
            'COUNT-SPECIES':nisotopes,
            'COUNT-MOLECULES':nisotopes,
            'COUNT-STATES':nstates,
            'COUNT-RADIATIVE':ntranss,
            'APPROX-SIZE':size_estimate
            })

    if (ntranss > 0):
        return {'RadTrans':transs,
                #'NonRadTrans':non_transs,
                'Molecules':isotopes,
                'Sources':sources,
                'Methods':methods,
                'HeaderInfo':headerinfo
               }
    else:
        return {}

