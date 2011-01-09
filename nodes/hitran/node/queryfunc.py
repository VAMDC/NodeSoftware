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
case_prefixes[3] = 'hundb'
case_prefixes[4] = 'ltcs'
case_prefixes[5] = 'nltcs'
case_prefixes[6] = 'stcs'
case_prefixes[7] = 'lpcs'
case_prefixes[8] = 'asymcs'
case_prefixes[9] = 'asymos'
case_prefixes[10] = 'sphcs'
case_prefixes[11] = 'sphos'

def getHITRANbroadening(transs):
    for trans in transs:
        prms = Prms.objects.filter(transid=trans.id)
        prm_dict = {}
        for prm in prms:
            prm_dict[prm.prm_name] = prm
        broadenings = []
        if 'g_air' in prm_dict.keys() and 'n_air' in prm_dict.keys():
            g_air_val = str(prm_dict['g_air'].prm_val)
            g_air_err = str(prm_dict['g_air'].prm_err)
            n_air_val = str(prm_dict['n_air'].prm_val)
            n_air_err = str(prm_dict['n_air'].prm_err)
            lineshape = '<ucl:Lineshape name="Lorentzian">\n'\
                '<ucl:Comments>The temperature-dependent pressure broadening'\
                ' Lorentzian lineshape</ucl:Comments>\n'\
                '<ucl:LineshapeParameter name="gammaL" units="1/cm">\n'\
                '<ucl:FitParameters functionRef="FgammaL">\n'\
                '<ucl:FitArgument lowerLimit="240" upperLimit="350"'\
                ' units="K">T</ucl:FitArgument>\n'\
                '<ucl:FitArgument lowerLimit="0." upperLimit="1.2"'\
                ' units="atm">p</ucl:FitArgument>\n'\
                '<ucl:FitParameter name="gammaL_ref" units="1/cm">\n'\
                '<ucl:Value>%s</ucl:Value>\n'\
                '<ucl:Accuracy>%s</ucl:Accuracy>\n'\
                '</ucl:FitParameter>\n'\
                '<ucl:FitParameter name="n" units="unitless">\n'\
                '<ucl:Value>%s</ucl:Value>\n'\
                '<ucl:Accuracy>%s</ucl:Accuracy>\n'\
                '</ucl:FitParameter>\n</ucl:FitParameters>\n'\
                '</ucl:LineshapeParameter>\n</ucl:Lineshape>\n' \
                    % (g_air_val, g_air_err, n_air_val, n_air_err)
            broadening = '<ucl:Broadening name="van-der-waals"'\
                ' envRef="air-broadening-ref-env">\n'\
                '%s'\
                '</ucl:Broadening>\n' % lineshape
            broadenings.append(broadening)
        if 'g_self' in prm_dict.keys():
            g_self_val = str(prm_dict['g_self'].prm_val)
            g_self_err = str(prm_dict['g_self'].prm_err)
            lineshape = '<ucl:Lorentzian>\n'\
                '<ucl:gammaL units="1/cm">\n'\
                '<ucl:Value>%s</ucl:Value>\n'\
                '<ucl:Accuracy>%s</ucl:Accuracy>\n'\
                '</ucl:gammaL>\n'\
                '</ucl:Lorentzian>' % (g_self_val, g_self_err)
            broadening = '<ucl:Broadening name="van-der-waals"'\
                ' envRef="%s-broadening-ref-env">\n'\
                '%s'\
                '</ucl:Broadening>\n' % ('self', lineshape)
            broadenings.append(broadening)
        trans.broadening_xml = ''.join(broadenings)

def getHITRANstates(transs):
    stateIDs = set([])
    for trans in transs:
        stateIDs = stateIDs.union([trans.initialstateref,
                                   trans.finalstateref])
    return States.objects.filter(pk__in=stateIDs)

#def getHITRANmolecules(transs):
#    molecIDs = set([])
#    for trans in transs:
#        molecIDs = molecIDs.union([trans.molecid])
#    return Molecules.objects.filter(pk__in=molecIDs)

def getHITRANmolecules(transs):
    InChIKeys = set([])
    for trans in transs:
        InChIKeys.add(trans.inchikey)
    species = []
    for isotopologue in Isotopologues.objects.filter(pk__in=InChIKeys):
        molecules = Molecules.objects.filter(pk=isotopologue.molecid)
        molecule = molecules[0]
        species.append(Species(isotopologue.molecid, isotopologue.isoid,
                isotopologue.inchikey, molecule.molec_name,
                isotopologue.iso_name, molecule.chemical_names,
                molecule.stoichiometric_formula,
                molecule.stoichiometric_formula))
    return species

def getHITRANsources(transs):
    sourceIDs = set([])
    for trans in transs:
        s = set([trans.nu_ref, trans.a_ref])
        sourceIDs = sourceIDs.union(s)
    return Refs.objects.filter(pk__in=sourceIDs)

def parseHITRANstates(states):
    sids = set([])
    for state in states:
        #s = set([state.id])
        #sids = sids.union(s)
        sids.add(state.id)

    qns = []
    for qn in Qns.objects.filter(stateid__in=sids).order_by('id'):
        if qn.qn_attr:
            # put quotes around the value of the attribute
            attr_name, attr_val = qn.qn_attr.split('=')
            qn.qn_attr = '%s="%s"' % (attr_name, attr_val)
        qns.append(MolQN(qn.stateid, case_prefixes[qn.caseid], qn.qn_name,
                         qn.qn_val, qn.qn_attr, qn.xml))

    LOG('%d state quantum numbers obtained' % len(qns))
    #sys.exit(0)
    return qns

def setupResults(sql, LIMIT=10):
    q = sqlparse.where2q(sql.where,RESTRICTABLES)
    try:
        q=eval(q)
    except Exception,e:
        LOG('Exception in setupResults():')
        LOG(e)
        return {}

    transs = Trans.objects.filter(q) 
    ntrans = transs.count()
    if ntrans > LIMIT:
        transs = transs[:LIMIT]
        percentage = '%.1f' % (float(LIMIT)/ntrans * 100)
    else:
        percentage = None

    getHITRANbroadening(transs)
    sources = getHITRANsources(transs)
    states = getHITRANstates(transs)
    nstates = states.count()
    # extract the state quantum numbers in a form that generators.py can use:
    qns = parseHITRANstates(states)
    species = getHITRANmolecules(transs)
    nspecies = states.count()
    LOG('%s transitions retrieved from HITRAN database' % ntrans)
    LOG('%s states retrieved from HITRAN database' % nstates)
    LOG('%s species retrieved from HITRAN database' % nspecies)

    headerinfo = CaselessDict({
        'Truncated': '%s %%' % percentage,
        'count-species': nspecies,
        'count-states': nstates,
        'count-radiative': ntrans
    })

   # return the dictionary as described above
    return {'HeaderInfo': headerinfo,
            'RadTrans': transs,
            'Sources': sources,
            'MoleStates': states,
            'MoleQNs': qns,
            'Molecules': species}

