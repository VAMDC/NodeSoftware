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
import time

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
        if iso.molecule.molecID == 36:
            # XXX for now, hard-code the molecular charge for NO+
            iso.molecule.charge = 1
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

def bad_ref(refID):
    """
    Create a 'virtual' reference indicating that the database returned a
    reference object that couldn't be turned into valid XSAMS.

    """

    return Ref(refID=refID, ref_type='private communication',
               authors='C. Hill, M.-L. Dubernet', note='The reference'
               ' identified by %s cannot be resolved into valid XSAMS'
                    % refID, year=2011)

def get_sources(ref_ids):
    refs = []
    for ref_id in ref_ids:
        try:
            ref = Ref.objects.get(pk=ref_id)
        except Ref.DoesNotExist:
            continue
        # filter out references we can't represent in XSAMS, and rename
        # 'article' as 'journal' and 'thesis' and 'theses' (sic)
        if ref.ref_type == 'article':
            ref.ref_type = 'journal'
        elif ref.ref_type not in ('private communication', 'proceedings',
                                  'database'):
            # this ref won't resolve to valid XSAMS
            ref = bad_ref(ref.refID)
        # <Year> is compulsory in XSAMS, so if it's missing in the
        # database, return a bad_ref:
        if ref.year is None:
            ref = bad_ref(ref.refID)
        refs.append(ref)
    return refs

def attach_prms(transitions):
    """
    Attach the parameters for each transition to its Trans object as
    prm.val, prm.err, and prm.ref

    """
    ref_ids = set()
    for trans in transitions:
        for prm in trans.prm_set.all():
            exec('trans.%s = prm' % prm.name)
            ref_ids.add(prm.ref_id)
    return ref_ids

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
    inchikeys = isos.values_list('InChIKey', flat=True)
    q = ['InchiKey', 'in', '(']
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

def Pascals2Torr(op, foo):
    """ Replace foo in Pascals with foo in Torr """
    try:
        foop = float(foo[0])
    except (ValueError, TypeError):
        print 'failed to convert %s to float' % foo
        return None
    foop = foop * 0.007500616827041697
    q = ['Pressure', op, str(foop)]
    return q
        
def setupResults(sql):
    # rather than use the sql2Q method:
    #q = sqlparse.sql2Q(sql)

    start_time = time.time()

    # ... we parse the query into its restrictables and logic:
    if not sql.where:
        return {}
    logic, rs, count = sqlparse.splitWhere(sql.where)
    # and replace any restrictions on ChemicalName or StoichiometricFormula
    # with the equivalent on MoleculeInchiKey. Also convert wavelength
    # (in Angstroms) to wavenumber:
    for i in rs:
        r, op, foo = rs[i][0], rs[i][1], rs[i][2:]
        if r == 'MoleculeChemicalName':
            rs[i] = ChemicalName2MoleculeInchiKey(op, foo)
        if r == 'MoleculeStoichiometricFormula':
            rs[i] = StoichiometricFormula2MoleculeInchiKey(op, foo)
        if r == 'RadTransWavelength':
            rs[i] = Wavelength2Wavenumber(op, foo)
        if r == 'Pressure':
            rs[i] = Pascals2Torr(op, foo)
    # now rebuild the query as a dictionary of QTypes ...
    qdict = {}
    for i, r in rs.items():
        q = sqlparse.restriction2Q(r)
        qdict[i] = q
    # ... and merge them to a single query object
    q = sqlparse.mergeQwithLogic(qdict, logic)

    if 'radiativecrosssections' in sql.requestables:
        return setupXsecResults(q)
    
    transitions = Trans.objects.filter(q).order_by('nu')
    ntrans = transitions.count()
    if settings.TRANSLIM is not None and ntrans > settings.TRANSLIM:
        # we need to filter transitions again later, so can't take a slice
        #transitions = transitions[:settings.TRANSLIM]
        # so do this:
        numax = transitions[settings.TRANSLIM].nu
        transitions = Trans.objects.filter(q, Q(nu__lte=numax))
        percentage = '%.1f' % (float(settings.TRANSLIM)/ntrans * 100)
        ntrans = transitions.count()
        print 'Results truncated to %s %%' % percentage
    else:
        percentage = '100'
        print 'Results not truncated'
    print 'TRANSLIM is', settings.TRANSLIM
    print 'ntrans =',ntrans

    ts = time.time()
    ref_ids = attach_prms(transitions)
    te = time.time()
    print 'time to attach parameters = %.1f secs' % (te-ts)

    ts = time.time()
    sources = get_sources(ref_ids)
    te = time.time()
    print 'time to get sources = %.1f secs' % (te-ts)
    # extract the state quantum numbers in a form that generators.py can use:
    ts = time.time()
    species, nspecies, nstates = get_species(transitions)
    te = time.time()
    print 'time to get species = %.1f secs' % (te-ts)
    LOG('%s transitions retrieved from HITRAN database' % ntrans)
    LOG('%s states retrieved from HITRAN database' % nstates)
    LOG('%s species retrieved from HITRAN database' % nspecies)

    nsources = 0
    if sources is not None:
        # sources is a Python list, not a queryset, so we can't use count()
        nsources = len(sources)
    print 'nsources =', nsources
    print 'nspecies =', nspecies
    print 'nstates =', nstates
    print 'ntrans =', ntrans

    headerinfo = {
        'Truncated': '%s %%' % percentage,
        'count-sources': nsources,
        'count-species': nspecies,
        'count-molecules': nspecies,
        'count-states': nstates,
        'count-radiative': ntrans
    }

    methods = [Method('MEXP', 'experiment', 'experiment'),
               Method('MTHEORY', 'theory', 'theory')]

    end_time = time.time()
    print 'timed at %.1f secs' % (end_time - start_time)

   # return the dictionary as described above
    return {'HeaderInfo': headerinfo,
            'Methods': methods,
            'RadTrans': transitions,
            'Sources': sources,
            'Molecules': species,
            'Environments': HITRANenvs,
            'Functions': HITRANfuncs}

def get_xsec_envs(xsecs):
    xsec_envs = []
    for xsec in xsecs:
        xsec_envs.append(Environment(xsec.id, xsec.T, xsec.p,
                                     [EnvSpecies(xsec.broadener),]))
    return xsec_envs

def setupXsecResults(q):

    # quick and dirty hack to replace the iso__InChIKey__<relation> with
    # molecule_InChIKey__<relation> in the query, appropriate for cross
    # section search (yuk yuk yuk):
    for i, children in enumerate(q.children):
        if children[0].startswith('iso'):
            new_restrictable = children[0].replace('iso', 'molecule', 1)
            new_child = (new_restrictable, children[1])
            q.children[i] = new_child

    xsecs = Xsc.objects.filter(q)
    nxsecs = xsecs.count()

    # XXX
    nsources = 0; sources = None;

    # hack this: the generator expects Species to be Isos (since the dictionary
    # resolves them this way (appropriate for the line-by-line transitions);       # however, for cross sections, Species are Molecules...
    species = []
    for m in Molecule.objects.filter(pk__in=xsecs.values_list('molecule')
                .distinct()):
        xsec_species = Iso(molecule=m)
        xsec_species.InChIKey = m.InChIKey
        xsec_species.InChI = m.InChI
        xsec_species.iso_name = m.ordinary_formula
        #xsec_species.XML() = m.XML()
        species.append(xsec_species)
    nspecies = len(species)

    xsec_envs = get_xsec_envs(xsecs)

    headerinfo = {
        'Truncated': '100 %',
        'count-sources': nsources,
        'count-species': nspecies,
        'count-molecules': nspecies,
        'count-radiative': nxsecs
    }

    methods = [Method('MEXP', 'experiment', 'experiment'),
              ]

   # return the dictionary as described above
    return {'HeaderInfo': headerinfo,
            'Methods': methods,
            'RadCross': xsecs,
            'Sources': sources,
            'Molecules': species,
            'Environments': xsec_envs,
           }

def returnResults(tap):
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
    if settings.TRANSLIM is not None and ntrans > settings.TRANSLIM:
        # we need to filter transitions again later, so can't take a slice
        #transitions = transitions[:settings.TRANSLIM]
        # so do this:
        numax = transitions[settings.TRANSLIM].nu
        transitions = Trans.objects.filter(q, Q(nu__lte=numax))
        percentage = '%.1f' % (float(settings.TRANSLIM)/ntrans * 100)
        print 'Results truncated to %s %%' % percentage
    else:
        percentage = '100'
        print 'Results not truncated'
    print 'settings.TRANSLIM is', settings.TRANSLIM
    print 'ntrans =',ntrans
    
    par_generator = Par(transitions)
    response = HttpResponse(par_generator, mimetype='text/plain')
    return response

def Par(transitions):
    for trans in transitions:
        yield '%s\n' % trans.hitranline
