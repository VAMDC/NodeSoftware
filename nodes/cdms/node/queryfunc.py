# -*- coding: utf-8 -*-
from django.db.models import Q
from models import *
from dictionaries import *
from vamdctap.sqlparse import *

import sys
def LOG(s):
    print >> sys.stderr, s

def getCDMSsources(transs):
    return # no sources yet for CDMS, afaik
    #return Source.objects.filter(pk__in=sids)

def getCDMSstates(transs):
#    q1,q2=Q(isupperstate_trans__in=transs),Q(islowerstate_trans__in=transs)
    q1,q2=Q(isinitialstate__in=transs),Q(isfinalstate__in=transs)
    return StatesMolecules.objects.order_by('isotopomer').filter(q1|q2).distinct()
   
def getCDMSstates2(transs):
    stateids=set([])
    for trans in transs:
       stateids=stateids.union(set([trans.initialstateref, trans.finalstateref]))
    q=Q(stateid__in=stateids)
    return StatesMolecules.objects.order_by('isotopomer').filter(q).distinct()
       
def getCDMSqns(states):
    sids=set([])
    LOG('Loop States')
#    LOG(states)
    for state in states:
#       LOG(state.stateid)
       s=set([state.stateid])
       sids=sids.union(s)
#       LOG(state.stateid)

#    q = Q(statesmolecules__in=states)
#    LOG(sids)
#    sids=set([])
    q=Q(statesmolecules__in=sids)
    return MolecularQuantumNumbers.objects.filter(q)


def getCDMSqns2(states):
    qns=set([])
    LOG('Loop States')
    for state in states:
       q=Q(statesmolecules__exact=state.stateid)
       qn=set([MolecularQuantumNumbers.objects.filter(q)])
       qns=qns.union(qn)

    return qns


def setupResults(sql):
#    LOG("SQL:")
#    LOG(sql.where)
    q=where2q(sql.where,RESTRICTABLES)
#    LOG("Q:"+q)
    try: q=eval(q)
#    q=eval(q)
#    LOG(q)
#    q='frequencyvalue=50000'
    except: return {}
#    q='molecularchemicalspecies="CO"'
    LOG('Start Query Transitions')
    transs = RadiativeTransitions.objects.select_related(depth=2).filter(q)
#    transs = RadiativeTransitions.objects.filter(molecularchemicalspecies__exact='NH3').filter(frequencyvalue__gt=29500).filter(frequencyvalue__lt=130000)
#    transs = RadiativeTransitions.objects.select_related(depth=2).filter(molecularchemicalspecies__exact='CO') #, frequencyvalue>29500, frequencyvalue<130000)
#    LOG(transs)
    LOG('Start Query Sources')
#    transs = transs[:50]
    sources = getCDMSsources(transs)
    LOG('Start Query States')
    states = getCDMSstates2(transs)
    LOG('Start Query QN')
    quantumnumbers = getCDMSqns(states)
    LOG('Queries done')
#    qn= states[0].molecularquantumnumbers_set.all()
#    qn = states[0].quantumnumbers.all()
    return {'RadTrans':transs,
            'MoleStates':states,
            'Sources':sources,
            'MoleQNs':quantumnumbers,
            }


