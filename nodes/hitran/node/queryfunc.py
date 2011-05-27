# -*- coding: utf-8 -*-

from django.db.models import Q
from django.conf import settings
from dictionaries import *
from models import *
from vamdctap import sqlparse
from itertools import chain
from HITRANfuncsenvs import * 

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
case_prefixes[12] = 'ltos'
case_prefixes[13] = 'lpos'
case_prefixes[14] = 'nltos'

def getHITRANbroadening(transs, XSAMSvariant):
    if XSAMSvariant == 'vamdc':
        # for vamdc-XSAMS, there's no broadening:
        for trans in transs:
            trans.broadening_xml = '<!-- Broadening --> '
        return

    if XSAMSvariant == 'ucl':
        print 'the XSAMS variant ucl is no longer supported on this branch'\
              ' of the node software'
        return

    if XSAMSvariant == 'working':
        # for vamdc-working branch, write the broadening XML:
        for trans in transs:
            prms = Prms.objects.filter(transid=trans.id)
            prm_dict = {}
            for prm in prms:
                prm_dict[prm.prm_name] = prm
                # XXX for now, replace reference with the generic HITRAN08 ref
                prm_dict[prm.prm_name].prm_ref = 'BHIT-B_HITRAN2008'
            broadenings = []
            if 'g_air' in prm_dict.keys() and 'n_air' in prm_dict.keys():
                g_air_val = str(prm_dict['g_air'].prm_val)
                g_air_err = str(prm_dict['g_air'].prm_err)
                g_air_ref = str(prm_dict['g_air'].prm_ref)
                n_air_val = str(prm_dict['n_air'].prm_val)
                n_air_err = str(prm_dict['n_air'].prm_err)
                n_air_ref = str(prm_dict['n_air'].prm_ref)
                lineshape = '      <Lineshape name="Lorentzian">\n'\
                '      <Comments>The temperature-dependent pressure'\
                ' broadening Lorentzian lineshape</Comments>\n'\
                '      <LineshapeParameter>\n'\
                '        <Name>gammaL</Name>\n'\
                '        <FitParameters functionRef="FgammaL">\n'\
                '          <FitArgument units="K">\n'\
                '            <Name>T</Name>\n'\
                '            <LowerLimit units="K">240</LowerLimit>\n'\
                '            <UpperLimit units="K">350</UpperLimit>\n'\
                '          </FitArgument>\n'\
                '          <FitArgument units="K">\n'\
                '            <Name>p</Name>\n'\
                '            <LowerLimit units="atm">0.</LowerLimit>\n'\
                '            <UpperLimit units="atm">1.2</UpperLimit>\n'\
                '          </FitArgument>\n'\
                '          <FitParameter>\n'\
                '            <Name>gammaL_ref</Name>\n'\
                '            <SourceRef>%s</SourceRef>\n'\
                '            <Value units="1/cm">%s</Value>\n'\
                '            <Accuracy>%s</Accuracy>\n'\
                '          </FitParameter>\n'\
                '          <FitParameter>\n'\
                '            <Name>n</Name>\n'\
                '            <SourceRef>%s</SourceRef>\n'\
                '            <Value units="unitless">%s</Value>\n'\
                '            <Accuracy>%s</Accuracy>\n'\
                '          </FitParameter>\n'\
                '        </FitParameters>\n'\
                '      </LineshapeParameter>\n</Lineshape>\n' \
                        % (g_air_ref, g_air_val, g_air_err, n_air_ref,
                           n_air_val, n_air_err)
                broadening = '    <PressureBroadening'\
                    ' envRef="Eair-broadening-ref-env">\n'\
                    '%s'\
                    '    </PressureBroadening>\n' % lineshape
                broadenings.append(broadening)
            if 'g_self' in prm_dict.keys():
                g_self_val = str(prm_dict['g_self'].prm_val)
                g_self_err = str(prm_dict['g_self'].prm_err)
                g_self_ref = str(prm_dict['g_self'].prm_ref)
                lineshape = '      <Lineshape name="Lorentzian">\n'\
                    '        <LineshapeParameter>\n'\
                    '        <Name>gammaL</Name>\n'\
                    '          <SourceRef>%s</SourceRef>\n'\
                    '          <Value units="1/cm">%s</Value>\n'\
                    '          <Accuracy>%s</Accuracy>\n'\
                    '        </LineshapeParameter>\n'\
                    '      </Lineshape>' % (g_self_ref, g_self_val,
                                                 g_self_err)
                broadening = '    <PressureBroadening'\
                    ' envRef="E%s-broadening-ref-env">\n'\
                    '%s'\
                    '    </PressureBroadening>\n' % ('self', lineshape)
                broadenings.append(broadening)
            shiftings = []
            if 'delta_air' in prm_dict.keys():
                delta_air_val = str(prm_dict['delta_air'].prm_val)
                delta_air_err = str(prm_dict['delta_air'].prm_err)
                delta_air_ref = str(prm_dict['delta_air'].prm_ref)
                shifting = '    <Shifting envRef="Eair-broadening-ref-env">\n'\
                    '      <ShiftingParameter>\n'\
                    '        <Name>delta</Name>\n'\
                    '        <FitParameters functionRef="Fdelta">\n'\
                    '          <FitArgument units="K">\n'\
                    '            <Name>p</Name>\n'\
                    '            <LowerLimit units="atm">0.</LowerLimit>\n'\
                    '            <UpperLimit units="atm">1.2</UpperLimit>\n'\
                    '          </FitArgument>\n'\
                    '          <FitParameter>'\
                    '            <Name>delta_ref</Name>\n'\
                    '            <SourceRef>%s</SourceRef>\n'\
                    '            <Value units="unitless">%s</Value>\n'\
                    '            <Accuracy>%s</Accuracy>\n'\
                    '          </FitParameter>\n'\
                    '        </FitParameters>\n'\
                    '      </ShiftingParameter>\n'\
                    '    </Shifting>\n' % (delta_air_ref, delta_air_val,
                                           delta_air_err)
                shiftings.append(shifting)
            
            # treat shifting as a sort of broadening(!) for now
            trans.broadening_xml = '   <Broadenings>\n%s    </Broadenings>\n'\
                    '    <Shiftings>\n%s</Shiftings>' % (''.join(broadenings),
                                                         ''.join(shiftings))

def attach_state_qns(states):
    for state in states:
        state.parsed_qns = []
        qns = Qns.objects.filter(stateid=state.id)
        for qn in qns.order_by('id'):
            if qn.qn_attr:
                # put quotes around the value of the attribute
                attr_name, attr_val = qn.qn_attr.split('=')
                qn.qn_attr = '%s="%s"' % (attr_name, attr_val)
            state.parsed_qns.append(MolQN(qn.stateid, case_prefixes[qn.caseid],
                               qn.qn_name, qn.qn_val, qn.qn_attr, qn.xml))

def getHITRANmolecules(transs):
    InChIKeys = set([])
    for trans in transs:
        InChIKeys.add(trans.inchikey)
    nstates = 0
    species = []
    for isotopologue in Isotopologues.objects.filter(pk__in=InChIKeys):
        molecules = Molecules.objects.filter(pk=isotopologue.molecid)
        molecule = molecules[0]
        this_species = Species(isotopologue.molecid, isotopologue.isoid,
                isotopologue.inchikey, molecule.molec_name,
                isotopologue.iso_name, molecule.chemical_names,
                molecule.stoichiometric_formula,
                molecule.stoichiometric_formula)
        this_species.inchi = isotopologue.inchi
        states = []
        # all the transitions for this species:
        sptranss = transs.filter(inchikey=isotopologue.inchikey)
        # sids is all the stateIDs involved in these transitions:
        stateps = sptranss.values_list('finalstateref', flat=True)
        statepps = sptranss.values_list('initialstateref', flat=True)
        sids = set(chain(stateps, statepps))
        # attach the corresponding states to the molecule:
        this_species.States = States.objects.filter( pk__in = sids)
        attach_state_qns(this_species.States)
        nstates += len(sids)
        # add this species object to the list:
        species.append(this_species)
    nspecies = len(species)
    return species, nspecies, nstates

def getHITRANsources(transs):
    # for now, we set all the references to HITRAN2008
    #sourceIDs = set([])
    sourceIDs = ['B_HITRAN2008',]
    for trans in transs:
        #s = set([trans.nu_ref, trans.a_ref])
        trans.nu_ref = 'B_HITRAN2008'
        trans.a_ref = 'B_HITRAN2008'
        trans.s_ref = 'B_HITRAN2008'
        #sourceIDs = sourceIDs.union(s)

    sources = []
    for source in Refs.objects.filter(pk__in=sourceIDs):
        sources.append(Source(source.sourceid, source.type, source.author,
                    source.title, source.journal, source.volume,
                    source.pages, source.year, source.institution,
                    source.note, source.doi))

    return sources

def setupResults(sql, LIMIT=None, XSAMSvariant='working'):
    q = sqlparse.where2q(sql.where,RESTRICTABLES)
    try:
        q=eval(q)
    except Exception,e:
        LOG('Exception in setupResults():')
        LOG(e)
        return {}

    transs = Trans.objects.filter(q) 
    ntrans = transs.count()
    if LIMIT is not None and ntrans > LIMIT:
        # we need to filter transs again later, so can't take a slice
        #transs = transs[:LIMIT]
        # so do this:
        numax = transs[LIMIT].nu
        transs = Trans.objects.filter(q, Q(nu__lte=numax))
        percentage = '%.1f' % (float(LIMIT)/ntrans * 100)
    else:
        percentage = None

    getHITRANbroadening(transs, XSAMSvariant)
    sources = getHITRANsources(transs)
    # extract the state quantum numbers in a form that generators.py can use:
    species, nspecies, nstates = getHITRANmolecules(transs)
    LOG('%s transitions retrieved from HITRAN database' % ntrans)
    LOG('%s states retrieved from HITRAN database' % nstates)
    LOG('%s species retrieved from HITRAN database' % nspecies)

    headerinfo = CaselessDict({
        'Truncated': '%s %%' % percentage,
        'count-species': nspecies,
        'count-states': nstates,
        'count-radiative': ntrans
    })

    methods = [Method('MEXP', 'experiment', 'experiment'),
               Method('MTHEORY', 'theory', 'theory')]

   # return the dictionary as described above
    return {'HeaderInfo': headerinfo,
            'Methods': methods,
            'RadTrans': transs,
            'Sources': sources,
            'Molecules': species,
            'Environments': HITRANenvs,
            'Functions': HITRANfuncs}

