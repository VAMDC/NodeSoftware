 # -*- coding: utf-8 -*-
from django.db.models import Q
from django.db import connection
from django.conf import settings
import sys
import datetime

def LOG(s):
    if settings.DEBUG: print >> sys.stderr, s

from dictionaries import *
from itertools import chain
from copy import deepcopy

from models import *
from vamdctap.sqlparse import *

from django.template import Context, loader
from django.http import HttpResponse
def tapServerError(request=None, status=500, errmsg=''):
    text = 'Error in TAP service: %s' % errmsg
    # XXX I've had to copy TAP-error-document.xml into my node's
    # template directory to get access to it, as well...
    document = loader.get_template('tap/TAP-error-document.xml').render(
                     Context({"error_message_text" : text}))
    return HttpResponse(document, status=status, content_type='text/xml');
                                

if hasattr(settings,'TRANSLIM'):
    TRANSLIM = settings.TRANSLIM
else: TRANSLIM = 5000


def attach_partionfunc(molecules):
    """
    Attaches partition functions to each specie.
    """
    for molecule in molecules:
        molecule.pfT = []
        molecule.pfQ = []
        molecule.pfnsiname = [] #nuclearspinisomer',
        molecule.pflowestrovibstateid = []
        molecule.pfsymmetrygroup = []
        molecule.pfnsilowestrovibsym = []

        #pfs = Partitionfunctions.objects.filter(specie = molecule, state="All")
        pfs = PartitionfunctionsDetailed.objects.filter(specie = molecule) 

        # Get List of all nuclear spin isomers "None" should be included and gives
        # partition functions which do not distinguish between nuclear spin isomers.
        nsilist = pfs.values_list('nsi_id', flat=True).distinct()

        for nsi in nsilist:
            temp_pf_list = pfs.filter(nsi_id=nsi).values('temperature').annotate(p=Sum('partitionfunc')).order_by('temperature')
            
            #temp=pfs.filter(nsi_id=nsi).values_list('temperature',flat=True)
            #pf = pfs.filter(nsi_id=nsi).values_list('partitionfunc',flat=True)
            temp =temp_pf_list.values_list('temperature',flat=True)
            pf =temp_pf_list.values_list('p',flat=True)

            # Get information on nuclear spin isomers or Null
            try:
                nsi = NuclearSpinIsomers.objects.get(pk=nsi)
                nsiname = nsi.name
                nsilowestrovibstateid = nsi.lowestrovibstate
                nsisymmetrygroup = nsi.symmetrygroup
                nsilowestrovibsym = nsi.lowestrovibsym
            except:
                nsiname = ''
                nsilowestrovibstateid = ''
                nsisymmetrygroup = ''
                nsilowestrovibsym = '' 
                
            molecule.pfT.append(temp)
            molecule.pfQ.append(pf)
            molecule.pfnsiname.append(nsiname)
            molecule.pflowestrovibstateid.append(nsilowestrovibstateid)
            molecule.pfsymmetrygroup.append(nsisymmetrygroup)
            molecule.pfnsilowestrovibsym.append(nsilowestrovibsym)
         

def remap_species(datasets):
    idxlist = []
    species = []

    for i in datasets:
        specieid = '%s-hyp%s' % (i.specie.id,i.hfsflag)
        if specieid not in idxlist:
            idxlist.append(specieid)
            i.specie.hfs = i.hfsflag
            i.specie.specieid = specieid
            species.append(i.specie)

    return species

def get_species_and_states(transs, addStates = True, filteronatoms = False):
    """
    Returns list of species including all states which occur in the list
    of transitions.
    Returns:
    - Atoms
    - Molecules
    - Number of species
    - Number of states
    """

    # Get list of specie-ids which occur in transitions
    if filteronatoms:
        spids = set( transs.values_list('specie_id',flat=True).distinct() )
    else:
        spids = transs.values_list('specie_id',flat=True)

    # Species object for CDMS includes Atoms AND Molecules. Both can only
    # be distinguished through numberofatoms-field
    atoms = Species.objects.filter(pk__in=spids, molecule__numberofatoms__exact='Atomic', origin=0, archiveflag=0)
    molecules = Species.objects.filter(pk__in=spids, origin=0, archiveflag=0).exclude(molecule__numberofatoms__exact='Atomic') #,ncomp__gt=1)

    # Calculate number of species in total
    nspecies = atoms.count() + molecules.count()

    # Intialize state-counter
    nstates = 0

    if addStates:
        up = transs.values_list('upperstateref',flat=True)
        low = transs.values_list('lowerstateref',flat=True)
        for m in molecules:
            states = m.states_set.filter(Q(pk__in= up) | Q(pk__in= low))
            # get state origins and nuclear spin origins
            state_origin = m.originstates_set.all()
            nsi_origins = m.originstates_set(manager = 'nsi_objects').all()
            origins = state_origin | nsi_origins
            # modify the id to avioid dublication with regular states
            for s in origins:
                s.id = s.id_alias()
                s.aux = True
            # attach states to molecule object
            m.States = chain(origins, states)

        for a in atoms:
            states = a.atomstates_set.filter(Q(pk__in= up) | Q(pk__in= low))
            origins = a.atomstates_set(manager = 'energy_origin').all()
            for s in origins:
                s.id = s.id_alias()
                s.aux = True
            m.States = chain(origins, states)

        # determine the number of states
        nstates = States.objects.filter(pk__in=chain(up,low)).count()

    return atoms,molecules,nspecies,nstates

def get_species_and_states_old(transs, addStates=True, filteronatoms=False):
    """
    Returns list of species including all states which occur in the list
    of transitions.
    Returns:
    - Atoms
    - Molecules
    - Number of species
    - Number of states
    """

    # Get list of specie-ids which occur in transitions
    if filteronatoms:
        spids = set( transs.values_list('specie_id',flat=True).distinct() )
    else:
        spids = transs.values_list('specie_id',flat=True)

    # Species object for CDMS includes Atoms AND Molecules. Both can only
    # be distinguished through numberofatoms-field
    atoms = Species.objects.filter(pk__in=spids, molecule__numberofatoms__exact='Atomic', origin=0, archiveflag=0)
    molecules = Species.objects.filter(pk__in=spids, origin=0, archiveflag=0).exclude(molecule__numberofatoms__exact='Atomic') #,ncomp__gt=1)

    # Calculate number of species in total
    nspecies = atoms.count() + molecules.count()

    # Intialize state-counter
    nstates = 0

    if addStates:
        # Loop through list of species and attach states
        for specie in chain( molecules):
            #dds=Datasets.objects.filter(specie=specie, archiveflag=0, hfsflag=specie.hfs).values_list('id',flat=True)
            #dds=set(dds)

            # Get distinct list of States which
            # occur as lower or upper state in transitions
            subtranss = transs.filter(specie=specie, dataset__archiveflag=0)
            up=subtranss.values_list('upperstateref',flat=True)
            lo=subtranss.values_list('lowerstateref',flat=True)
            sids = set(chain(up,lo))
            states = States.objects.filter( pk__in = sids)
            # Get energy origins
            origin_ids = states.values_list('energyorigin',flat=True).distinct()
            nsi_origin_ids = NuclearSpinIsomers.objects.filter(pk__in=states.values_list('nsi',flat=True)).values_list('lowestrovibstate',flat=True)
            # nsi_origin_ids = States.objects.filter(pk__in = sids).values_list('nsioriginid',flat=True).distinct()
            origin_ids = set(chain(origin_ids,nsi_origin_ids))
            origins = States.objects.filter(pk__in = origin_ids)

            # Create new ID for 'origin'-states
            # These states occur twice in the output
            # species-id is used to make id unique (origin-state could be a state of another specie if v>0)
            for state in origins:
                state.id = "%s-origin-%s" % (state.id, specie.id)
                state.aux = True

            # Attach states to species object            
            specie.States = chain(origins, states)
            # Add number of attached states to state-counter
            nstates += states.count()

                
        for specie in chain(atoms ):
            #dds=Datasets.objects.filter(specie=specie, archiveflag=0, hfsflag=specie.hfs).values_list('id',flat=True)
            #dds=set(dds)
            # Get distinct list of States which
            # occur as lower or upper state in transitions
            subtranss = transs.filter(specie=specie, dataset__archiveflag=0)
            up=subtranss.values_list('upperstateref',flat=True)
            lo=subtranss.values_list('lowerstateref',flat=True)
            sids = set(chain(up,lo))
            # Attach states to species object
            specie.States = AtomStates.objects.filter( pk__in = sids)
            # Add number of attached states to state-counter
            nstates += specie.States.count()

                
    return atoms,molecules,nspecies,nstates


def get_sources(atoms, molecules, methods = []):
    """
    Get a complete list of sources and methods for the set of
    predicted transitions. Methods compiled for observed
    transitions have to be transfered via input variable method in
    order to be included in the output.
    """

    # Get the list of species (entries). One method is generated for each specie
    #ids = set( transs.values_list('specie_id',flat=True) )
    ids=[]
    
    for i in chain(molecules,atoms):
        ids.append(i.id)

    slist = SourcesIDRefs.objects.filter(specie__in=ids)

    sexplist = slist.filter(transitionexp__gt=0)

    # Loop over species list and get sources
#    for src in ids: #slist.values_list('specie',flat=True):
#        mesrc=SourcesIDRefs.objects.filter(Q(specie=src)).distinct().values_list('source',flat=True)
#        this_method = Method(src,src,'derived','derived with Herb Pickett\'s spfit / spcat fitting routines, based on experimental data',mesrc)
#        methods.append(this_method)

    datasets = Datasets.objects.filter(specie__in=ids, type__in=['egy','cat','mrg','lin'], archiveflag=0)
    for dat in datasets:
        mesrc=SourcesIDRefs.objects.filter(Q(specie=dat.specie_id)).distinct().values_list('source',flat=True)
        if dat.type == 'lin':
            description = 'experimental transition frequencies: %s' % dat.comment
            category = 'observed'
        else:
            description = 'derived with Herb Pickett\'s spfit / spcat fitting routines, based on experimental data: %s' % dat.comment
            category='derived'
        this_method = Method(dat.id, dat.id,category,description,mesrc)
        methods.append(this_method)
        
    # Loop over species list and get sources
    for src in sexplist.values_list('source',flat=True).distinct():
        this_method =  Method('EXP'+str(src),src,'experiment','experiment',src)
        methods.append(this_method)
        
    sourceids = set(slist.values_list('source',flat=True))
    sourceids = sourceids.union(DATABASE_REFERENCES)
    return Sources.objects.filter(pk__in = sourceids), methods
    


def attach_exp_frequencies(transs):
    """
    Create lists of frequencies, units, sources, ... for each transition.
    The calculated frequency is given anyway followed by experimental
    frequencies (db-table: Frequencies). In addition a unique list of
    methods for the experimental data is created and returned.
    Returns:
    - modified transitions (frequencies, ... attached as lists)
    - methods for experimental data
    
    """
    methodrefs = []
    methods = []
    
    # Loop over calculated transitions (Predictions)
    # and attach Experimental Frequencies
    for trans in transs:
        
        # Attach the calculated frequency first
        trans.frequencies=[trans.frequency]
        trans.units=[trans.unit]
        trans.uncertainties=[trans.uncertainty]
        trans.refs=[""]
        trans.methods=[trans.specie.id]
        
        exptranss = TransitionsExp.objects.filter(species=trans.species,
                                                  qnup1=trans.qnup1,
                                                  qnlow1=trans.qnlow1,
                                                  qnup2=trans.qnup2,
                                                  qnlow2=trans.qnlow2,
                                                  qnup3=trans.qnup3,
                                                  qnlow3=trans.qnlow3,
                                                  qnup4=trans.qnup4,
                                                  qnlow4=trans.qnlow4,
                                                  qnup5=trans.qnup5,
                                                  qnlow5=trans.qnlow5,
                                                  qnup6=trans.qnup6,
                                                  qnlow6=trans.qnlow6)
        
        for exptrans in exptranss:
            trans.frequencies.append(exptrans.frequency)
            trans.units.append(exptrans.unit)
            trans.uncertainties.append(exptrans.uncertainty)
            # get sources
            s= exptrans.sources.all().values_list('source',flat=True)
            trans.refs.append(s)

            method = "EXP" + "-".join(str(source) for source in s)
            trans.methods.append(method)
            methodrefs.append(method)

    # Create a distinct list of methods
    methodrefs = list(set(methodrefs))

    for ref in methodrefs:
        this_method =  Method(ref,None,'experiment','experiment',ref[3:].split("-"))
        methods.append(this_method)
        
    return transs, methods

def setupResults(sql):
    """
    This method queries the database with respect to the sql-query
    and compiles everything together for the vamdctap.generator function
    which is used to generate XSAMS - output.
    """

    # Modify where-clause:
    # Ensure that filters on AtomMassNumber only return atoms and not also molecules
    sql.parsedSQL=SQL.parseString(sql.query.replace("AtomIonCharge","AtomSymbol>0 and AtomIonCharge"),parseAll=True)
    sql.where = sql.parsedSQL.where

    # Determines wether there is a restriction on a field in the species table
    # This distinction is needed for speed optimization (to many subqueries are extremely slow in mysql)
    filteronatoms = "Atom" in sql.query
    filteroninchi = "Inchi" in sql.query
    filteronmols = "Molecule" in sql.query
    filteronspecieid = "SpeciesID" in sql.query
    filteronspecies = ("Ion" in sql.query) | filteronmols | filteroninchi | filteronatoms | filteronspecieid
    q = sql2Q(sql)

    temperature = 300.0
    if not sql.parsedSQL.where:
        q = Q()
    else:
        logic, restriction, count = splitWhere(sql.parsedSQL.where)
        q_dict = {}
        for i, r in restriction.items():
           r = applyRestrictFu(r)
           if r[0].lower() == 'environmenttemperature':
               if r[1] in ('=', '=='):
                   temperature = r[2]
                   q_dict[i] = Q(pk__isnull = False)
               else:
                   q_dict[i] = QFalse
           else:
               q_dict[i] = restriction2Q(r)
        q = mergeQwithLogic(q_dict, logic)
#    q = sql2Q(sql)
#    LOG(q)
    addStates = (not sql.requestables or 'atomstates' in sql.requestables or 'moleculestates' in sql.requestables)
    addTrans = (not sql.requestables or 'RadiativeTransitions' in sql.requestables)
    #datasets = Datasets.objects.filter(archiveflag=0)

    # Query the database and get calculated transitions (TransitionsCalc)
#    transs = RadiativeTransitions.objects.filter(q #specie__origin=0,
#                                            #specie__archiveflag=0,
#                                            #dataset__in=datasets,
#                                            #dataset__archiveflag=0
#                                            ) #.order_by('frequency')
    if temperature == 300.0:
        transs = RadiativeTransitions.objects.filter(q) 
    else:
        transs = RadiativeTransitionsT.objects.filter(q, temperature = temperature, intensity__gt= -99.9)
     # modify filter for transitions:
    transs = transs.filter(specie__origin=0, specie__archiveflag=0, dataset__archiveflag=0)

    # get atoms and molecules with states which occur in transition-block
    atoms, molecules,nspecies,nstates = get_species_and_states(transs, addStates, filteronspecies)
   # Attach experimental transitions (TransitionsExp) to transitions
    # and obtain their methods. Do it only if transitions will be returned
    if addTrans:
        transs = transs.order_by('frequency')
        #transs, methods = attach_exp_frequencies(transs)
        methods=[]
    else:
        methods=[]

    # get sources and methods which have been used
    # to derive predicted transitions
    if addTrans:
        sources, methods = get_sources(atoms, molecules, methods)
    else:
        sources=Sources.objects.none()
    nsources = sources.count()
    nmolecules = len(molecules)#molecules.count()
    natoms = len(atoms) #atoms.count()
    ntranss = transs.count()

    lastmodified = datetime.datetime(2009,12,1)
    for specie in chain(atoms, molecules):        
        if specie.changedate>lastmodified:
            lastmodified = specie.changedate
    if lastmodified ==  datetime.datetime(2009,12,1):
        lastmodified = datetime.datetime.now()
    # Calculate estimated size of xsams-file
    if ntranss+nmolecules+natoms+nstates>0:
        size_estimate='%.2f' % (nstates*0.0008755624 +ntranss*0.000561003 +nmolecules*0.001910 +nsources * 0.0005+0.01)
    else: size_estimate='0.0'

    # this header info is used in xsams-header-info (html-request)
    headerinfo={\
        'Truncated':"100", # CDMS will not truncate data (at least for now)
        'count-sources':nsources, 
        'count-species':nspecies,
        'count-molecules':nmolecules,
        'count-atoms':natoms,
        'count-states':nstates,
        'count-radiative':ntranss,
        'APPROX-SIZE':size_estimate,
        'last-modified':lastmodified,
    }

    if hasattr(sql, 'XRequestMethod') and sql.XRequestMethod == 'HEAD':
        return {'HeaderInfo': headerinfo}
    # attach partition functions to each specie and return the result
    attach_partionfunc(molecules)
    return {'RadTrans':transs,
            'Atoms':atoms,
            'Molecules':molecules,
            'Sources':sources,
            'Methods':methods,
            'HeaderInfo':headerinfo,
            }



def returnResults(tap, LIMIT=None):
    """
    Return this node's response to the TAP query, tap, where
    the requested return format is something other than XSAMS.
    The TAP object has been validated upstream of this method,
    so we're good to go.

    """

    # ADD additional restricables for this output method which are
    # only meaningful for CDMS
    RESTRICTABLES.update(CDMSONLYRESTRICTABLES)

    SUPPORTED_FORMATS=['spcat','png','list','xspcat','mrg','species']
    print_einsteina = False

    if tap.format not in SUPPORTED_FORMATS:
        emsg = 'Currently, only FORMATs PNG, SPCAT and XSAMS are supported.\n'
        return tapServerError(status=400, errmsg=emsg)

    if tap.format == 'list':
        speclist=specieslist()
        response = HttpResponse(speclist, content_type='text/plain')
        return response

    if tap.format == 'species':
        speclist=plain_specieslist()
        response = HttpResponse(speclist, content_type='text/plain')
        return response


    # Create filter manually, because temperature and intensity information
    # has to be obtained separately in order to prepare the partition functions
    # accordingly.
    temperature = 300.0
    if not tap.parsedSQL.where:
        q = Q()
    else:
        logic, restriction, count = splitWhere(tap.parsedSQL.where)
        q_dict = {}
        # filter where intensity restriction has been removed to assure that
        # all species will be obtained for retrieving all partitionfunctions
        q_noint_dict = {}
        for i, r in restriction.items():
            r = applyRestrictFu(r)
            if r[0].lower() == 'environmenttemperature':
                if r[1] in ('=', '=='):
                    temperature = r[2]
                    q_dict[i] = Q(pk__isnull = False)
                    q_noint_dict[i] = Q(pk__isnull = False)
                else:
                    q_dict[i] = QFalse
                    q_noint_dict[i] = QFalse
            elif r[0].lower() == 'radtransprobabilityidealisedintensity':
                    q_dict[i] = restriction2Q(r)
                    q_noint_dict[i] = Q(pk__isnull = False)
            else:
                q_dict[i] = restriction2Q(r)
                q_noint_dict[i] = restriction2Q(r)
        q = mergeQwithLogic(q_dict, logic)
        q_noint = mergeQwithLogic(q_noint_dict, logic)

    # use tap.parsedSQL.columns instead of tap.requestables
    # because only the selected columns should be returned and no additional ones
    col = tap.parsedSQL.columns #.asList()
    if temperature == 300.0:
        transs = RadiativeTransitions.objects.filter(q,specie__archiveflag=0,dataset__archiveflag=0) #,energylower__gt=0) 
    else:
        transs = RadiativeTransitionsT.objects.filter(q, specie__archiveflag = 0, dataset__archiveflag = 0, temperature = temperature, intensity__gt= -99.9)
    ntrans = transs.count()

#    if LIMIT is not None and ntrans > LIMIT:
        # we need to filter transs again later, so can't take a slice
        #transs = transs[:LIMIT]
        # so do this:
#        numax = transs[LIMIT].nu
#        transs = TransitionsCalc.objects.filter(q, Q(nu__lte=numax))
#        percentage = '%.1f' % (float(LIMIT)/ntrans * 100)
#    else:
    percentage = '100'
#    print 'Truncated to %s %%' % percentage


    # Prepare Transitions
    if (col=='ALL' or 'radiativetransitions' in [x.lower() for x in col]):
        LOG('TRANSITIONS')
        orderby = tap.request.get('ORDERBY','frequency')
        if tap.request.get('IntUnit', 'T') == 'A':
            print_einsteina = True
         
        if ',' in orderby:
            orderby=orderby.split(',')
            transitions = transs.order_by(*orderby) 
        else:            
            transitions = transs.order_by(orderby)
        # get the partinotion functions if temperature != 300K        
        if temperature != 300.0:
            species = RadiativeTransitions.objects.filter(q_noint).values_list('specie_id', flat = True).distinct()
            LOG(species)
            # Get partitinofunctions for all species for specific temperature
            q300 = {}
            qrs = {}
            cursor = connection.cursor()
            for s in species:
                try:
                    q300[s] = Partitionfunctions.objects.get(specie = s, temperature = 300.0, state = 'All', nsi__isnull = True)
                except:
                    q300[s] = None
                try:
                    cursor.execute('SELECT F_GetPartitionfunctionDetailed(300, %s)', s)
                    qrs[s] = cursor.fetchone()[0]
                except:
                    qrs[s] = None
            cursor.close()



    else:
        LOG('NO TRANSITIONS')
        transitions = []


    # Prepare States if requested
    if (col=='ALL' or 'states' in [x.lower() for x in col] ):
        LOG('STATES')
        orderby = tap.request.get('ORDERBY','energy')
        #states = States.objects.filter(q,specie__origin=0,dataset__archiveflag=0).order_by(orderby)
        states = States.objects.filter(q,dataset__archiveflag=0).order_by(orderby)
    else:
        LOG('NO STATES')
        states = []


    if tap.format in ('spcat','xspcat','mrg'):
        generator = gener(transitions, states, format=tap.format, print_einsteina = print_einsteina)
        response = HttpResponse(generator, content_type='text/plain')
    else:
        if 'states' in tap.requestables:
            response = plotLevelDiagram(states)
        else:
            response = plotStickSpec(transitions)
        
    return response


def GetStringValue(value):
    if value == None: 
        return ''
    else:
        return value

def GetNumericValue(value):
    if value == None: 
        return 0
    else:
        return value
    
def formatqn(value):
    if value == None:
        return ''
    elif value > 99 and value < 360:
        return chr(55+value/10)+ "%01d" % ( value % 10)
    elif value < -9 and value > -260:
        return chr(95-(value-1)/10)+ "%01d" % -( value % -10)
    else:
        return str(value)

def gener(transs=None, states=None, format='spcat', print_einsteina = False):

    if format=='xspcat':
        for trans in xCat(transs):
            yield trans
    elif format == 'mrg':
        for trans in Mrg(transs, print_einsteina = print_einsteina):
            yield trans
    else:
        for trans in Cat(transs):
            yield trans
        for state in Egy(states):
            yield state
        

def Cat(transs):
    for trans in transs:
        yield '%13.4lf' % trans.frequency
        yield '%8.4lf' % trans.uncertainty
        yield '%8.4lf' % trans.intensity
        yield '%2d' % trans.degreeoffreedom
        yield '%10.4lf' % trans.energylower

        yield '%3d' % trans.upperstatedegeneracy
        yield '%7d' % trans.speciestag
        
        yield '%4d' % trans.qntag
        yield '%2s' % formatqn(trans.qnup1)
        yield '%2s' % formatqn(trans.qnup2)
        yield '%2s' % formatqn(trans.qnup3)
        yield '%2s' % formatqn(trans.qnup4)
        yield '%2s' % formatqn(trans.qnup5)
        yield '%2s' % formatqn(trans.qnup6)

        yield '%2s' % formatqn(trans.qnlow1)
        yield '%2s' % formatqn(trans.qnlow2)
        yield '%2s' % formatqn(trans.qnlow3)
        yield '%2s' % formatqn(trans.qnlow4)
        yield '%2s' % formatqn(trans.qnlow5)
        yield '%2s' % formatqn(trans.qnlow6)

        yield '%s' % trans.specie.name
        yield '\n'


def Mrg(transs, print_einsteina = False):
    """
    """
    
    for trans in transs:
        yield '%s ' % trans.spfitstr(print_einsteina = print_einsteina)
##        trans.attach_exp_frequencies()

##        speciestag = trans.speciestag

##        if len(trans.frequencies)>1:
##            speciestag=-speciestag
##            frequency = trans.frequencies[1]
##            uncertainty = trans.uncertainties[1]
##        else:
##            frequency = trans.frequency
##            uncertainty = trans.uncertainty
            
##        yield '%13.4lf' % frequency
##        yield '%8.4lf' % uncertainty
##        yield '%8.4lf' % trans.intensity
        
##        yield '%2d' % trans.degreeoffreedom
##        yield '%10.4lf' % trans.energylower

##        yield '%3d' % trans.upperstatedegeneracy
##        yield '%7d' % speciestag
        
##        yield '%4d' % trans.qntag
##        yield '%2s' % formatqn(trans.qnup1)
##        yield '%2s' % formatqn(trans.qnup2)
##        yield '%2s' % formatqn(trans.qnup3)
##        yield '%2s' % formatqn(trans.qnup4)
##        yield '%2s' % formatqn(trans.qnup5)
##        yield '%2s' % formatqn(trans.qnup6)

##        yield '%2s' % formatqn(trans.qnlow1)
##        yield '%2s' % formatqn(trans.qnlow2)
##        yield '%2s' % formatqn(trans.qnlow3)
##        yield '%2s' % formatqn(trans.qnlow4)
##        yield '%2s' % formatqn(trans.qnlow5)
##        yield '%2s' % formatqn(trans.qnlow6)

        yield '%s' % trans.specie.name
        yield '\n'



def xCat(transs):
    # qnlabels = ["J","N","Ka","Kc","v"]
    qnlabels = []
    tagarray = transs.values_list('specie','qntag').distinct()
    for specie, qntag in tagarray:
        filter = QuantumNumbersFilter.objects.filter(specie= specie, qntag=qntag).order_by('order')
        qnlabels = chain(qnlabels, filter.values_list('label','order'))
    
#    qnlabels = set(qnlabels)
    qnlabels = sorted(set(qnlabels),key=lambda x:x[1])

#    statess = set( transs.values_list('upperstateref',flat=True) )

#    qns = MolecularQuantumNumbers.objects.filter(pk__in=statess).distinct()
#    dictqns = {}
#          
#          for qn in qns:
#               if qn.attribute:
#                    # put quotes around the value of the attribute
#                    attr_name, attr_val = qn.attribute.split('=')
#                    qn.attribute = ' %s="%s"' % (attr_name, attr_val)
#               else:
#                    qn.attribute = ''
#                    
#               if qn.spinref:
#                    # add spinRef to attribute if it exists
#                    qn.attribute += ' nuclearSpinRef="%s"' % qn.spinref

#               dictqns.update({qn.label : qn.value})


    # Header
    yield '%13s' % "Frequency"
    yield '%8s' % "Unc."
    yield '%8s' % "Intens."
    yield '%4s' % "DOF"
    yield '%12s' % "l. Energy."
    
    yield '%5s ' % "Gup"

    for qnlabel in qnlabels:
        yield '%4s' % qnlabel[0][:4]

    yield ' - '
    for qnlabel in qnlabels:
        yield '%4s' % qnlabel[0][:4]


    yield ' Specie'
    yield '\n'
    
    for trans in transs:
        yield '%13.4lf' % trans.frequency
        yield '%8.4lf' % trans.uncertainty
        yield '%8.4lf' % trans.intensity
        yield '%4d' % trans.degreeoffreedom
        yield '%12.4lf' % trans.energylower

        yield '%5d ' % trans.upperstatedegeneracy
#        yield '%7d' % trans.speciestag
        

        # Create quantum number output
        upperqns = trans.upperstateref.qns_dict()
        lowerqns = trans.lowerstateref.qns_dict()

#        yield '<div class="qn label">(%s) = </div>' % ",".join(upperqns)

        for label in qnlabels:
            if label[0]=='ElecStateLabel':
                val = str(upperqns.get(label[0]))[:1]
            else:
                val = str(upperqns.get(label[0]))

            if val=="None":
                val=""
                
            yield '<div class="qn %s">%4s</div>' % (label[0], val)

#        yield " <- "
        yield '   '

        for label in qnlabels:
            if label[0]=='ElecStateLabel':
                val = str(lowerqns.get(label[0]))[:1]
            else:
                val = str(lowerqns.get(label[0]))

            if  val=="None":
                val=""
                
            yield '<div class="qn %s">%4s</div>' % (label[0], val)
            

        yield ' %s' % trans.specie.name

        
        yield '\n'

        # QUERY and Display Experimental values
        exptranss = TransitionsExp.objects.filter(specie=trans.specie,
                                            qnup1=trans.qnup1,
                                            qnlow1=trans.qnlow1,
                                            qnup2=trans.qnup2,
                                            qnlow2=trans.qnlow2,
                                            qnup3=trans.qnup3,
                                            qnlow4=trans.qnlow4,
                                            qnup5=trans.qnup5,
                                            qnlow6=trans.qnlow6)
        for exptrans in exptranss:
            yield '<small style="color:blue">'
            yield '    %16.4lf' % exptrans.frequency
            yield '    %10.4lf' % exptrans.uncertainty
#            if exptrans.comment:
#            yield '    %20s' % (exptrans.comment if exptrans.comment else "")

            yield '   '
            sources = SourcesIDRefs.objects.filter(transitionexp=exptrans.id)
            for source in sources:
                yield '[%s] ' % source.referenceid.id

            yield '</small>\n'
            



def Egy(states):
    for state in states:
        yield '%5s' % GetStringValue(state.block)
        yield '%5s' % GetStringValue(state.index)                
        yield '%18.6lf' % GetNumericValue(state.energy)
        yield '%18.6lf' % GetNumericValue(state.mixingcoeff)
        yield '%18.6lf' % GetNumericValue(state.uncertainty)

        yield '%3s' % GetStringValue(state.qn1)
        yield '%3s' % GetStringValue(state.qn2)
        yield '%3s' % GetStringValue(state.qn3)
        yield '%3s' % GetStringValue(state.qn4)
        yield '%3s' % GetStringValue(state.qn5)
        yield '%3s' % GetStringValue(state.qn6)

        yield '%s' % GetStringValue(state.specie.name)
        yield '%3s' % GetStringValue(state.degeneracy)          
        yield '%4s' % GetStringValue(state.nuclearspinisomer)
        yield '%7s' % GetStringValue(state.nuclearstatisticalweight)
        yield '%4s ' % GetStringValue(state.qntag)

        yield '\n'


def plotStickSpec(transs):
    import os
    os.environ['HOME']='/tmp'

    
    import matplotlib
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter
    fig = Figure(facecolor='#eeefff',figsize=(15, 10), dpi=80,edgecolor='w')
    
    ax=fig.add_subplot(1,1,1)
    # bx=fig.add_subplot(2,1,1)


    spids = set( transs.values_list('specie_id',flat=True) )

    if (len(spids)>0): 
            
        spidsname = []
        species = Species.objects.filter(pk__in=spids) #,ncomp__gt=1)
        i=0
        bars=[]
        for specie in species:
            spidsname.append(specie.name)
            subtranss = transs.filter(specie=specie)
            intensities = [10.0**trans.intensity for trans in subtranss]
            frequencies = [trans.frequency for trans in subtranss]
            #bars.append( ax.bar(frequencies, intensities, color=cm.jet(1.*i/len(spids)))[0] )
            bars.append( ax.bar(frequencies, intensities, linewidth=1,edgecolor=matplotlib.cm.jet(1.*i/len(spids)), color=matplotlib.cm.jet(1.*i/len(spids)))[0] )
            i=i+1
        
 
        ax.legend(bars,spidsname,loc=0)
        #    intensities = [10.0**trans.intensity for trans in transs]
        #    frequencies = [trans.frequency for trans in transs]
        # #   #IDs = [trans.species for trans in transs]
        
        #    ax.bar(frequencies, intensities) #, color=cols)
        
    ax.set_xlabel("Frequency [MHz]")
    ax.set_ylabel("Intensity [nm^2MHz]")

    title = u"Dynamically Generated Stick Spectrum "
    ax.set_title(title)


    ax.grid(True)
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    
    canvas.print_png(response)
    return response



def plotLevelDiagram(states):
    import os
    os.environ['HOME']='/tmp'

    
    import matplotlib
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter
    fig = Figure(facecolor='#eeefff',figsize=(15, 10), dpi=80,edgecolor='w')
    
    ax=fig.add_subplot(1,1,1)
    # bx=fig.add_subplot(2,1,1)
        
    ax.set_xlabel("J")
    ax.set_ylabel("Energy [cm-1]")


    spids = set( states.values_list('specie_id',flat=True) )
    count_species = len(spids)
    spidsname = []
    species = Species.objects.filter(pk__in=spids) #,ncomp__gt=1)
    i=0
    plots=[]
    for specie in species:
        if count_species == 0:
            speciescolor = matplotlib.cm.jet(1.)
        else:
            speciescolor = matplotlib.cm.jet(1.*i/count_species)
        spidsname.append(specie.name)
        substates = states.filter(specie=specie)

        for state in states:
            pl = ax.plot([state.qn1-0.3,state.qn1+0.3],[state.energy,state.energy], color = speciescolor)

        plots.append(pl)
        i=i+1
    if count_species > 0:
        ax.legend(plots, spidsname, loc=0)
#    ax.legend(bars,spidsname,loc=0)
    

#    for state in states:
#        ax.plot([state.qn1-0.3,state.qn1+0.3],[state.energy,state.energy], color='b')
 
    
    title = u"Energy Level Diagram "
    ax.set_title(title)


    ax.grid(True)
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    
    canvas.print_png(response)
    return response


def specieslist():
    speciess = Species.objects.filter(archiveflag=0)
    for specie in speciess:
        yield "<name>%s</name> \n" % specie.name
        yield "  <inchikey>%s</inchikey> \n" % specie.inchikey
        yield "  <stoichi>%s</stoichi> \n" % specie.molecule.stoichiometricformula
        yield "  <inchikeystem>%s<inchikeystem> \n" %  GetStringValue(specie.inchikey)[0:14]

        for nm in GetStringValue(specie.molecule.trivialname).split(","):
            yield "     <trivialname>%s<trivialname> \n" % nm
#        yield "  <trivialname>%s<trivialname> " %  GetStringValue(specie.molecule.trivialname)[0:14]
        
        yield "\n"


def plain_specieslist():
    speciess = Species.objects.filter(archiveflag=0)
    for specie in speciess:
        yield "%5s " % specie.id
        yield "%7s " % specie.speciestag
        yield "%-20s " % specie.molecule.stoichiometricformula
        yield "%-20s " % specie.molecule.structuralformula
        yield "%-20s " % specie.isotopolog        
        yield "%-30s " % specie.state        
#        yield "%-20s " % specie.name
        yield "%-20s " % specie.inchikey
        yield "%-s " % specie.molecule.trivialname
        
        yield "\n"
    
