# -*- coding: utf-8 -*-

from django.db.models import Q
from django.conf import settings
from dictionaries import *
from models import *
from vamdctap import sqlparse
from itertools import chain
from HITRANfuncsenvs import * 
import formula_parser
import sys

def LOG(s):
    print >> sys.stderr, s

def get_species(transitions):
    """
    Return a list of the species with transitions matching the search
    parameters and attach the relevant states to them.

    """

    nstates = 0
    species = Iso.objects.filter(pk__in=transitions.values_list('iso')
                                 .distinct())
    nspecies = species.count()
    for iso in species:
        # all the transitions for this species:
        sptransitions = transitions.filter(iso=iso)
        # sids is all the stateIDs involved in these transitions:
        stateps = sptransitions.values_list('statep', flat=True)
        statepps = sptransitions.values_list('statepp', flat=True)
        sids = set(chain(stateps, statepps))
        # attach the corresponding states to the species:
        iso.States = State.objects.filter(pk__in = sids)
        nstates += len(sids)
    return species, nspecies, nstates

def get_sources(transitions):
    return None
    refIDs = set()
    for trans in transitions:
        refIDs.add(trans.nu.ref)
        refIDs.add(trans.A.ref)
    return Ref.objects.filter(pk__in=refIDs)

def attach_prms(transitions):
    """
    Attach the parameters for each transition to its Trans object as
    prm.val, prm.err, and prm.ref

    """
    for trans in transitions:
        for prm in trans.prm_set.all():
            exec('trans.%s = prm' % prm.name)

def ChemicalName2MoleculeInchiKey(op, foo):
    """
    Replace the query clause 'MoleculeChemicalName =|IN XXX' with the
    corresponding query 'MoleculeInchiKey IN ZZZ' by resolving the chemical
    names into one or more InChIKeys corresponding to matching isotopologues
    in the database.

    """

    if op == 'in' or op == '=':
        name_list = []
        # strip the open and closing parentheses from the foo list:
        for name in foo:
            if name =='(' or name ==')':
                continue
            name_list.append(name.replace('"','').replace("'",''))
        moleculename_ids = MoleculeName.objects.filter(name__in=name_list)\
                            .values_list('molecule', flat=True)
    else:
        print 'I only understand IN and = queries on ChemicalName, but I'
        print 'got', op
        return None
    molecules = Molecule.objects.filter(pk__in=moleculename_ids)
    isos = Iso.objects.filter(molecule__in=molecules)
    inchikeys = isos.values_list('InChIKey_explicit', flat=True)
    q = ['MoleculeInchiKey', 'in', '(']
    for inchikey in inchikeys:
        q.append(inchikey)
    q.append(')')
    return q

def StoichiometricFormula2MoleculeInchiKey(op, foo):
    """
    Replace the query clause 'MoleculeStoichiometricFormula IN|= XXX' with the
    corresponding query 'MoleculeInchiKey IN ZZZ' by resolving the
    stoichiometric formulae into one or more InChIKeys corresponding to
    matching isotopologues in the database.

    """

    if op == 'in' or op == '=':
        stoich_formula_list = []
        # strip the open and closing parentheses from the foo list:
        for stoich_formula in foo:
            if stoich_formula == '(' or stoich_formula == ')':
                continue
            stoich_formula = stoich_formula.replace('"','').replace("'",'')
            try:
                # put the stoichiometric formula into canonical form:
                stoich_formula = formula_parser.get_stoichiometric_formula(
                                stoich_formula)
            except formula_parser.FormulaError as e:
                # Oops - couldn't make sense of the stoichiometric formula:
                print 'Failed to parse stoichiometric formula: %s' % e
                continue
            stoich_formula_list.append(stoich_formula)
        molecules = Molecule.objects.filter(
                stoichiometric_formula__in = stoich_formula_list)
    else:
        print 'I only understand IN and = queries on StoichiometricFormula,'
        print ' but I got', op
        return None
    isos = Iso.objects.filter(molecule__in=molecules)
    inchikeys = isos.values_list('InChIKey', flat=True)
    q = ['MoleculeInchiKey', 'in', '(']
    for inchikey in inchikeys:
        q.append(inchikey)
    q.append(')')
    return q

def Wavelength2Wavenumber(op, foo):
    """
    Replace the query clause "Wavelength <op> <foo>" with
    "Wavenumber <op'> <foo'>", making the conversion from Angstroms to
    cm-1.

    """

    if op == 'in':
        print 'Sorry - "in" queries not yet implemented for RadTransWavelength'
        return None

    opp = op
    if op == '<':
        opp = '>'
    if op == '<=' or op == '=<':
        opp = '>='
    if op == '>':
        opp = '<'
    if op == '>=' or op == '=>':
        opp = '<='
    try:
        foop = float(foo[0])
    except (ValueError, TypeError):
        print 'failed to convert %s to float' % foo
        return None
    except (IndexError):
        print 'no argument to Wavelength restrictable'
        return None
    if foop != 0.:
        # Angstroms -> cm-1
        foop = 1.e8 / foop
    else:
        # zero wavelength requested, so set wavenumber to something huge
        foop = 1.e20
    q = ['RadTransWavenumber', opp, str(foop)]
    return q
        
def setupResults(sql, LIMIT=1000):
    # rather than use the sql2Q method:
    #q = sqlparse.sql2Q(sql)
    # we parse the query into its restrictables and logic:
    if not sql.where:
        return {}
    logic, rs, count = sqlparse.splitWhere(sql.where)
    # and replace any restrictions on ChemicalName or StoichiometricFormula
    # with the equivalent on MoleculeInchiKey. Also convert wavelength
    # (in A) to wavenumber:
    #print 'rs was',rs
    for i in rs:
        r, op, foo = rs[i][0], rs[i][1], rs[i][2:]
        if r == 'MoleculeChemicalName':
            rs[i] = ChemicalName2MoleculeInchiKey(op, foo)
        if r == 'MoleculeStoichiometricFormula':
            rs[i] = StoichiometricFormula2MoleculeInchiKey(op, foo)
        if r == 'RadTransWavelength':
            rs[i] = Wavelength2Wavenumber(op, foo)
    print 'rs is',rs
    qdict = sqlparse.restriction2Q(rs)
    q = sqlparse.mergeQwithLogic(qdict, logic)
    
    transitions = Trans.objects.filter(q) 
    ntrans = transitions.count()
    if LIMIT is not None and ntrans > LIMIT:
        # we need to filter transitions again later, so can't take a slice
        #transitions = transitions[:LIMIT]
        # so do this:
        numax = transitions[LIMIT].nu
        transitions = Trans.objects.filter(q, Q(nu__lte=numax))
        percentage = '%.1f' % (float(LIMIT)/ntrans * 100)
    else:
        percentage = '100'
    print 'Truncated to %s %%' % percentage

    attach_prms(transitions)

    sources = get_sources(transitions)
    # extract the state quantum numbers in a form that generators.py can use:
    species, nspecies, nstates = get_species(transitions)
    LOG('%s transitions retrieved from HITRAN database' % ntrans)
    LOG('%s states retrieved from HITRAN database' % nstates)
    LOG('%s species retrieved from HITRAN database' % nspecies)

    print 'nspecies =', nspecies
    print 'nstates =', nstates
    print 'ntrans =', ntrans
    if sources is not None:
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
            'RadTrans': transitions,
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

    transitions = Trans.objects.filter(q) 
    ntrans = transitions.count()
    if LIMIT is not None and ntrans > LIMIT:
        # we need to filter transitions again later, so can't take a slice
        #transitions = transitions[:LIMIT]
        # so do this:
        numax = transitions[LIMIT].nu
        transitions = Trans.objects.filter(q, Q(nu__lte=numax))
        percentage = '%.1f' % (float(LIMIT)/ntrans * 100)
    else:
        percentage = '100'
    print 'Truncated to %s %%' % percentage
    print 'ntrans =',ntrans
    
    par_generator = Par(transitions)
    response = HttpResponse(par_generator, mimetype='text/plain')
    return response

def Par(transitions):
    for trans in transitions:
        yield '%s\n' % trans.hitranline
