# -*- coding: utf-8 -*-

from django.db.models import Q
from django.conf import settings
from dictionaries import *
from models import *
from vamdctap import sqlparse

import sys
def LOG(s):
    print >> sys.stderr, s


case_prefixes = {}
case_prefixes[1] = 'dcs'
case_prefixes[2] = 'hunda'
case_prefixes[4] = 'ltcs'
case_prefixes[5] = 'nltcs'
case_prefixes[6] = 'stcs'
case_prefixes[9] = 'asymos'

def getHITRANstates(transs):
    stateIDs = set([])
    for trans in transs:
        stateIDs = stateIDs.union([trans.initialstateref,
                                   trans.finalstateref])

    return AllStates.objects.filter(pk__in=stateIDs)

def getHITRANmolecules(transs):
    molecIDs = set([])
    for trans in transs:
        molecIDs = molecIDs.union([trans.molecid])
    return Molecules.objects.filter(pk__in=molecIDs)

def getHITRANsources(transs):
    sourceIDs = set([])
    for trans in transs:
        s = set([trans.nu_ref, trans.a_ref])
        sourceIDs = sourceIDs.union(s)
    return Refs.objects.filter(pk__in=sourceIDs)

def parseHITRANstates(states):
    qns = []
    sids=set([])
    for state in states:
        s=set([state.stateid])
        sids=sids.union(s)

    for qn in AllQns.objects.filter(stateid__in=sids):
        label, value = qn.qn.split('=')
        if qn.qn_attr:
            # put quotes around the value of the attribute
            attr_name, attr_val = qn.qn_attr.split('=')
            qn.qn_attr = '%s="%s"' % (attr_name, attr_val)
        qns.append(MolQN(qn.stateid, case_prefixes[qn.caseid], label,
                         value, qn.qn_attr, qn.xml))

    LOG('%d state quantum numbers obtained' % len(qns))
    #sys.exit(0)
    return qns

def setupResults(sql):
    q = sqlparse.where2q(sql.where,RESTRICTABLES)
    try:
        q=eval(q)
    except Exception,e:
        LOG('Exception in setupResults():')
        LOG(e)
        return {}

    transs = Trans.objects.filter(q) 
    sources = getHITRANsources(transs)
    states = getHITRANstates(transs)
    # extract the state quantum numbers in a form that generators.py can use:
    qns = parseHITRANstates(states)
    molecules = getHITRANmolecules(transs)
    LOG('%s transitions retrieved from HITRAN database' % transs.count())
    LOG('%s states retrieved from HITRAN database' % states.count())

   # return the dictionary as described above
    return {'RadTrans': transs,
            'Sources': sources,
            'MoleStates': states,
            'MoleQNs': qns,
            'Molecules': molecules}

