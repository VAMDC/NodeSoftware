# -*- coding: utf-8 -*-
from django.db.models import Q
from django.conf import settings
import sys
def LOG(s):
    if settings.DEBUG: print >> sys.stderr, s

from dictionaries import *
from itertools import chain
from copy import deepcopy

from models import *
from vamdctap.sqlparse import *

if hasattr(settings,'TRANSLIM'):
    TRANSLIM = settings.TRANSLIM
else: TRANSLIM = 5000

#def getRefs(transs):
#    llids=set()
#    for t in transs.values_list('wave_ref_id','loggf_ref_id','lande_ref_id','gammarad_ref_id','gammastark_ref_id','waals_ref'):
#        llids = llids.union(t)
#    lls=LineList.objects.filter(pk__in=llids)
#    rids=set()
#    for ll in lls:
#        rids=rids.union(ll.references.values_list('pk',flat=True))
#    return Reference.objects.filter(pk__in=rids)

def attach_state_qns(states):
    for state in states:
        state.parsed_qns = []
        qns = MolecularQuantumNumbers.objects.filter(statesmolecules=state.stateid)
#        for qn in qns.order_by('id'):
        for qn in qns:
            if qn.attribute:
                # put quotes around the value of the attribute
                attr_name, attr_val = qn.attribute.split('=')
                qn.attribute = '%s="%s"' % (attr_name, attr_val)
 #           if qn.spinref:
                # add spinRef to attribute if it exists
#                qn.attribute += ' spinRef="%s"' % qn.spinref
            state.parsed_qns.append(MolecularQuantumNumbers(qn.stateid, qn.case, qn.label, qn.value, qn.attribute)) #, qn.xml))


def getSpeciesWithStates(transs):
    spids = set( transs.values_list('speciesid',flat=True) )
#    atoms = Species.objects.filter(pk__in=spids,ncomp=1)
    molecules = Molecules.objects.filter(pk__in=spids) #,ncomp__gt=1)
#    nspecies = atoms.count() + molecules.count()
    nspecies = molecules.count()
    nstates = 0
#    for species in [atoms,molecules]:
    for species in [molecules]:
        for specie in species:
            subtranss = transs.filter(species=specie)
            up=subtranss.values_list('finalstateref',flat=True)
            lo=subtranss.values_list('initialstateref',flat=True)
            sids = set(chain(up,lo))
            specie.States = StatesMolecules.objects.filter( pk__in = sids)
            nstates += len(sids)
            attach_state_qns(specie.States)
#            for state in specie.States:
#                 q=Q(statesmolecules__in=specie.States.stateid)
#                 specie.States.MolQN=MolecularQuantumNumbers.objects.filter(q)

#    return atoms,molecules,nspecies,nstates
    return molecules,nspecies,nstates


def getCDMSstates2(transs):
    stateids=set([])
    for trans in transs:
       stateids=stateids.union(set([trans.initialstateref, trans.finalstateref]))
    q=Q(stateid__in=stateids)
    return StatesMolecules.objects.order_by('isotopomer').filter(q).distinct()


def getCDMSqns(states):
    sids=set([])
    LOG('Loop States')
    for state in states:
       s=set([state.stateid])
       sids=sids.union(s)
    q=Q(statesmolecules__in=sids)
    return MolecularQuantumNumbers.objects.filter(q)


def setupResults(sql):
    LOG(sql)
    q=where2q(sql.where,RESTRICTABLES)
    try: q=eval(q)
    except: return {}

    LOG(q)
    #transs = Transition.objects.filter(q).order_by('vacwave')
    transs = RadiativeTransitions.objects.select_related(depth=2).filter(q)
    
#    ntranss=transs.count()
  #  if TRANSLIM < ntranss :
  #      percentage='%.1f'%(float(TRANSLIM)/ntranss *100)
  #      newmax=transs = transs[TRANSLIM].vacwave
  #      transs=Transition.objects.filter(q,Q(vacwave__lt=newmax))
  #  else: percentage=None
    percentage=None
    ntranss=transs.count()
    LOG(ntranss)
#    sources = getRefs(transs)
#    nsources = sources.count()
#    atoms,molecules,nspecies,nstates = getSpeciesWithStates(transs)
    molecules,nspecies,nstates = getSpeciesWithStates(transs)
    LOG(ntranss)

    headerinfo=CaselessDict({\
            'Truncated':percentage,
 #           'COUNT-SOURCES':nsources,
            'COUNT-species':nspecies,
            'count-states':nstates,
            'count-radiative':ntranss
            })

    return {'RadTrans':transs,
  #          'Atoms':atoms,
            'Molecules':molecules,
  #          'Sources':sources,
            'HeaderInfo':headerinfo,
  #          'Environments':Environments #this is set up statically in models.py
           }

