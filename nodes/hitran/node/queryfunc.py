# -*- coding: utf-8 -*-

from django.db.models import Q
from django.conf import settings
from dictionaries import *
from models import *
from vamdctap import sqlparse
from itertools import chain
from HITRANfuncsenvs import * 

# This turns a 500 "internal server error" into a TAP error-document
# XXX this is duplicated from vamdctap/views.py - some time, tidy this up.
from django.template import Context, loader
from django.http import HttpResponse
def tapServerError(request=None, status=500, errmsg=''):
    text = 'Error in TAP service: %s' % errmsg
    # XXX I've had to copy TAP-error-document.xml into my node's
    # template directory to get access to it, as well...
    document = loader.get_template('TAP-error-document.xml').render(
            Context({"error_message_text" : text}))
    return HttpResponse(document, status=status, mimetype='text/xml');

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
    InChIKeys = set(transs.values_list('inchikey', flat=True))
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
        #attach_state_qns(this_species.States)
        nstates += len(sids)
        # add this species object to the list:
        species.append(this_species)
    nspecies = len(species)
    return species, nspecies, nstates

def getHITRANsources(transs):
    # for now, we set all the references to HITRAN2008
    #sourceIDs = set([])
    sourceIDs = ['B_HITRAN2008',]
    #for trans in transs:
        #s = set([trans.nu_ref, trans.a_ref])
    #    trans.nu_ref = 'B_HITRAN2008'
    #    trans.a_ref = 'B_HITRAN2008'
    #    trans.s_ref = 'B_HITRAN2008'
        #sourceIDs = sourceIDs.union(s)

    sources = []
    for source in Refs.objects.filter(pk__in=sourceIDs):
        sources.append(Source(source.sourceid, source.type, source.author,
                    source.title, source.journal, source.volume,
                    source.pages, source.year, source.institution,
                    source.note, source.doi))
    return sources

def setupResults(sql, LIMIT=None):
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
        percentage = '100'
    print 'Truncated to %s %%' % percentage

    sources = getHITRANsources(transs)
    # extract the state quantum numbers in a form that generators.py can use:
    species, nspecies, nstates = getHITRANmolecules(transs)
    LOG('%s transitions retrieved from HITRAN database' % ntrans)
    LOG('%s states retrieved from HITRAN database' % nstates)
    LOG('%s species retrieved from HITRAN database' % nspecies)

    print 'nspecies =', nspecies
    print 'nstates =', nstates
    print 'ntrans =', ntrans
    print 'nsources =', len(sources)

    headerinfo = {
        'Truncated': '%s %%' % percentage,
        'count-species': nspecies,
        'count-molecules': nspecies,
        'count-states': nstates,
        'count-radiative': ntrans
    }

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

def returnResults(tap, LIMIT=None):
    """
    Return this node's response to the TAP query, tap, where
    the requested return format is something other than XSAMS.
    The TAP object has been validated upstream of this method,
    so we're good to go.

    """

    if tap.format != 'par':
        emsg = 'Currently, only FORMATs PAR and XSAMS are supported.\n'
        return tapServerError(status=400, errmsg=emsg)

    # XXX more duplication of code from setupResults():
    # which uses sql = tap.parsedSQL
    q = sqlparse.where2q(tap.parsedSQL.where, RESTRICTABLES)
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
        percentage = '100'
    print 'Truncated to %s %%' % percentage
    print 'ntrans =',ntrans
    
    par_generator = Par(transs)
    response = HttpResponse(par_generator, mimetype='text/plain')
    return response

def Par(transs):
    for trans in transs:
        yield '%s\n' % trans.hitranline
