from vamdctap.sqlparse import sql2Q
from vamdctap.generators import *
import vamdctap.generators as generators
from .models import *
from django.conf import settings
import logging
log = logging.getLogger('vamdc.node.queryfunc')

TRANSLIM = settings.TRANSLIM if hasattr(settings,'TRANSLIM') else 2000


class Method:
    def __init__(self, mid, category):
        self.id = mid
        self.category = category
        self.description = f'{category} method'

def getMethods():
    """Return method information for XSAMS output"""
    method_map = {
        0: 'experiment',
        1: 'observed',
        2: 'empirical',
        3: 'theory',
        4: 'semiempirical',
        5: 'compilation',
        6: 'derived'  # for Ritz wavelengths
    }
    return [Method(mid, cat) for mid, cat in method_map.items()]


def returnHeaders(transs):
    log.debug('Calculating statistics.')
    ntranss=transs.count()
    headers={'COUNT-RADIATIVE': ntranss}

    if TRANSLIM < ntranss:
        headers['TRUNCATED'] = '%.1f'%(float(TRANSLIM)/ntranss *100)

    if ntranss:
        headers['APPROX-SIZE']='%.2f'%(ntranss*0.0014 + 0.01)
    else:
        headers['APPROX-SIZE']='0.00'

    if ntranss < 1E7:
        species_ids = transs.values_list('species_id', flat=True).distinct()
        species_objs = Species.objects.filter(pk__in=species_ids)
        atoms_count = sum(1 for s in species_objs if not s.isMolecule())
        molecules_count = sum(1 for s in species_objs if s.isMolecule())
        headers['COUNT-ATOMS'] = atoms_count
        headers['COUNT-MOLECULES'] = molecules_count
        headers['COUNT-SPECIES'] = atoms_count + molecules_count
        sids = transs.values_list('upstate_id','lostate_id')
        sids = set(item for s in sids for item in s)
        headers['COUNT-STATES'] = len(sids)
    else:
        headers['COUNT-ATOMS'] = -1
        headers['COUNT-MOLECULES'] = -1
        headers['COUNT-SPECIES'] = -1
        headers['COUNT-STATES'] = -1

    return headers

def setupResults(sql):
    q = sql2Q(sql)
    log.debug('Just ran sql2Q(sql); setting up QuerySets now.')

    log.debug('%s\n%s'%(sql.parsedSQL.columns,type(sql.where)))
    if (len(sql.parsedSQL.columns) == 1) and (sql.where == ''):
        log.debug('Special case of "select species"')
        all_species = Species.objects.all()
        atoms_list = [s for s in all_species if not s.isMolecule()]
        molecules_list = [s for s in all_species if s.isMolecule()]
        return {'Atoms': atoms_list,
                'Molecules': molecules_list,
                'HeaderInfo':{'COUNT-SPECIES':all_species.count(),
                              'COUNT-ATOMS':len(atoms_list),
                              'COUNT-MOLECULES':len(molecules_list)}}

    transs = Transition.objects.filter(q)
    if sql.HTTPmethod == 'HEAD':
        return {'HeaderInfo':returnHeaders(transs)}

    transs = transs[:TRANSLIM]
    log.debug('Returning from setupResults()')
    return {'RadTrans':transs,
            'Environments':Environments, #set up statically in node_common.models
            'Methods':getMethods(),      #defined in node_common.queryfuncs
            'Functions':Functions,        #set up statically in node_common.models
            #'HeaderInfo':returnHeaders(transs),
           }


### Custom generator hack below here

from vamdctap.generators import *
from collections import defaultdict
# collect references and state IDs in global variables
stateIDs = defaultdict(set)
refIDs = set()

def XsamsRadTrans(RadTrans):
    """
    Generator for the XSAMS radiative transitions.
    """
    if not isiterable(RadTrans):
        return

    global stateIDs
    global refIDs

    for RadTran in RadTrans:
        stateIDs[RadTran.species_id].add(RadTran.upstate_id)
        stateIDs[RadTran.species_id].add(RadTran.lostate_id)
        refIDs.update(RadTran.wave_ref_id or [])
        refIDs.update(RadTran.waveritz_ref_id or [])
        refIDs.update(RadTran.loggf_ref_id or [])
        refIDs.update(RadTran.gammarad_ref_id or [])
        refIDs.update(RadTran.gammastark_ref_id or [])
        refIDs.update(RadTran.waals_ref_id or [])

        G = lambda name: GetValue(name, RadTran=RadTran)
        group = G('RadTransGroup')
        proc = G('RadTransProcess')
        attrs=''
        if group: attrs += ' groupLabel="%s"'%group
        if proc: attrs += ' process="%s"'%proc
        yield '<RadiativeTransition id="P%s-R%s"%s>'%(NODEID,G('RadTransID'),attrs)
        yield makeOptionalTag('Comments','RadTransComment',G)
        yield makeSourceRefs(G('RadTransRefs'))
        yield '<EnergyWavelength>'
        yield makeDataType('Wavenumber', 'RadTransWavenumber', G)
        yield makeDataType('Wavelength', 'RadTransWavelength', G,
                extraAttr={'envRef':G('RadTransWavelengthEnv'),
                    'vacuum':G('RadTransWavelengthVacuum')},
                extraElem={'AirToVacuum':G('RadTransWavelengthAirToVac')})
        yield makeDataType('Frequency', 'RadTransFrequency', G)
        yield makeDataType('Energy', 'RadTransEnergy', G)
        yield '</EnergyWavelength>'

        upper = G('RadTransUpperStateRef')
        if upper:
            yield '<UpperStateRef>S%s-%s</UpperStateRef>\n' % (NODEID, upper)
        lower = G('RadTransLowerStateRef')
        if lower:
            yield '<LowerStateRef>S%s-%s</LowerStateRef>\n' % (NODEID, lower)
        species = G('RadTransSpeciesRef')
        if species:
            yield '<SpeciesRef>X%s-%s</SpeciesRef>\n' % (NODEID, species)

        yield '<Probability>'
        yield makeDataType('TransitionProbabilityA', 'RadTransProbabilityA', G)
        yield makeDataType('OscillatorStrength', 'RadTransProbabilityOscillatorStrength', G)
        yield makeDataType('LineStrength', 'RadTransProbabilityLineStrength', G)
        yield makeDataType('WeightedOscillatorStrength', 'RadTransProbabilityWeightedOscillatorStrength', G)
        yield makeDataType('Log10WeightedOscillatorStrength', 'RadTransProbabilityLog10WeightedOscillatorStrength', G)
        yield makeDataType('IdealisedIntensity', 'RadTransProbabilityIdealisedIntensity', G)
        yield makeOptionalTag('Multipole','RadTransProbabilityMultipole',G)
        yield makeOptionalTag('TransitionKind','RadTransProbabilityKind',G)
        yield makeDataType('EffectiveLandeFactor', 'RadTransEffectiveLandeFactor', G)
        yield '</Probability>\n'

        yield "<ProcessClass>"
        yield makeOptionalTag('UserDefinition', 'RadTransUserDefinition',G)
        yield makeOptionalTag('Code','RadTransCode',G)
        yield makeOptionalTag('IAEACode','RadTransIAEACode',G)
        yield "</ProcessClass>"

        if hasattr(RadTran, 'XML_Broadening'):
            yield RadTran.XML_Broadening()
        else:
            yield XsamsRadTranBroadening(G)
        if hasattr(RadTran, 'XML_Shifting'):
            yield RadTran.XML_Shifting()
        else:
            yield XsamsRadTranShifting(RadTran)
        yield '</RadiativeTransition>\n'



def customXsams(tap, RadTrans=None, Environments=None, Atoms=None, Molecules=None,
        Methods=None, Functions=None, HeaderInfo=None):
    #return GEN.Xsams(tap, **kwargs)
    yield XsamsHeader(HeaderInfo)
    errs=''
    requestables = tap.requestables

    global stateIDs
    global refIDs

    log.debug('Working on Processes.')
    yield '<Processes>\n'
    yield '<Radiative>\n'
    if not requestables or 'radiativetransitions' in requestables:
        try:
            for RadTran in XsamsRadTrans(RadTrans):
                yield RadTran
        except Exception:
            errs+=generatorError(' RadTran')
    else: # loop over transitons anyway because we now collect states & species on the fly.
        try:
            for RadTran in XsamsRadTrans(RadTrans):
                pass
        except Exception:
            errs+=generatorError(' RadTran')
    yield '</Radiative>\n'
    yield '</Processes>\n'

    # Split species into atoms and molecules
    if Atoms is None and Molecules is None:
        # Normal query case: build from stateIDs
        all_species = Species.objects.filter(pk__in=stateIDs.keys())
        atoms_list = []
        molecules_list = []

        for species in all_species:
            if species.isMolecule():
                molecules_list.append(species)
            else:
                atoms_list.append(species)
    else:
        # SELECT SPECIES case: use predefined lists
        atoms_list = Atoms or []
        molecules_list = Molecules or []

    # Attach states to each species (works for both atoms and molecules)
    if requestables and ('atomstates' not in requestables):
        for species in atoms_list + molecules_list:
            species.States = []
    else:
        # Filter states by species_id - works for both atoms and molecules
        for species in atoms_list + molecules_list:
            # Convert set to list to avoid "set changed size during iteration" error
            state_ids = list(stateIDs[species.pk])

            # Add ground state if it's not already in the list (needed for energyOrigin reference)
            if species.ground_state_id and species.ground_state_id not in stateIDs[species.pk]:
                state_ids.append(species.ground_state_id)

            species.States = State.objects.filter(pk__in=state_ids)

    yield '<Species>\n'

    # Yield atomic species
    if not requestables or 'atoms' in requestables:
        log.debug('Working on Atoms.')
        try:
            for Atom in XsamsAtoms(atoms_list):
                yield Atom
        except: errs+=generatorError(' Atoms')

    # Yield molecular species
    if not requestables or 'molecules' in requestables:
        log.debug('Working on Molecules.')
        try:
            for Molecule in XsamsMolecules(molecules_list):
                yield Molecule
        except: errs+=generatorError(' Molecules')

    yield '</Species>\n'

    # Collect reference IDs from all states
    for species in atoms_list + molecules_list:
        for state in species.States:
            refIDs.update(state.energy_ref_id or [])
            refIDs.update(state.lande_ref_id or [])
            refIDs.update(state.level_ref_id or [])


    log.debug(refIDs)

    if len(refIDs) == 0:
        Sources = Reference.objects.all()
    else:
        Sources = Reference.objects.filter(pk__in=refIDs)
    if not requestables or 'sources' in requestables:
        log.debug('Working on Sources.')
        try:
            for Source in XsamsSources(Sources, tap):
                yield Source
        except: errs+=generatorError(' Sources')


    # reset them for the next query!
    stateIDs = defaultdict(set)
    refIDs = set()


    if not requestables or 'methods' in requestables:
        log.debug('Working on Methods.')
        try:
            for Method in XsamsMethods(Methods):
                yield Method
        except: errs+=generatorError(' Methods')

    if not requestables or 'functions' in requestables:
        log.debug('Working on Functions.')
        try:
            for Function in XsamsFunctions(Functions):
                yield Function
        except: errs+=generatorError(' Functions')

    if not requestables or 'environments' in requestables:
        log.debug('Working on Environments.')
        try:
            for Environment in XsamsEnvironments(Environments):
                yield Environment
        except: errs+=generatorError(' Environments')


    if errs: yield """<!--
           ATTENTION: There was an error in making the XML output and at least one item in the following parts was skipped: %s
-->
                 """ % errs

    yield '</XSAMSData>\n'
    log.debug('Done with XSAMS')


