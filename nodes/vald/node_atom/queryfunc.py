from ..node_common.queryfunc import *
from models import *

def setupResults(sql):
    q = sql2Q(sql)
    log.debug('Just ran sql2Q(sql); setting up QuerySets now.')
    transs = Transition.objects.filter(q)
    ntranss=transs.count()
    if TRANSLIM < ntranss and (not sql.requestables or 'radiative' in sql.requestables):
        percentage = '%.1f'%(float(TRANSLIM)/ntranss *100)
        newmax = transs[TRANSLIM].wave
        transs = Transition.objects.filter(q,Q(wave__lt=newmax))
        log.debug('Truncated results to %s, i.e %s A.'%(TRANSLIM,newmax))
    else:
        percentage=None
    log.debug('Transitions QuerySet set up. References next.')

    if ntranss:
        size_estimate='%.2f'%(ntranss*0.0014 + 0.01)
    else:
        size_estimate='0.00'

    headerinfo={\
            'TRUNCATED':percentage,
            'COUNT-RADIATIVE':ntranss,
            'APPROX-SIZE':size_estimate,
            }
    log.debug('Returning from setupResults()')
    return {'RadTrans':transs,
            'HeaderInfo':headerinfo,
            'Environments':Environments, #set up statically in node_common.models
            'Methods':getMethods(),      #defined in node_common.queryfuncs
            'Functions':Functions        #set up statically in node_common.models
           }


### Custom generator hack below here

from vamdctap.generators import *
# collect references and state IDs in global variables
stateIDs = {}
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
        if not stateIDs.has_key(RadTran.species_id):
            stateIDs[RadTran.species_id] = set()
        stateIDs[RadTran.species_id].add(RadTran.upstate_id)
        stateIDs[RadTran.species_id].add(RadTran.lostate_id)
        refIDs.update(RadTran.wave_ref_id)
        refIDs.update(RadTran.waveritz_ref_id)
        refIDs.update(RadTran.loggf_ref_id)
        refIDs.update(RadTran.gammarad_ref_id)
        refIDs.update(RadTran.gammastark_ref_id)
        refIDs.update(RadTran.waals_ref_id)

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



def customXsams(tap, RadTrans, HeaderInfo, Environments, Methods, Functions):
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
        except:
            errs+=generatorError(' RadTran')
    yield '</Radiative>\n'
    yield '</Processes>\n'


    Atoms = Species.objects.filter(pk__in=stateIDs.keys())
    if requestables and Atoms and ('atomstates' not in requestables):
        for Atom in Atoms:
            Atom.States = []
    else:
        for Atom in Atoms:
            print stateIDs[Atom.pk]
            Atom.States = State.objects.filter(pk__in=stateIDs[Atom.pk])

    yield '<Species>\n'
    if not requestables or 'atoms' in requestables:
        log.debug('Working on Atoms.')
        try:
            for Atom in XsamsAtoms(Atoms):
                yield Atom
        except: errs+=generatorError(' Atoms')

    yield '</Species>\n'


    for Atom in Atoms:
        for state in Atom.States:
            refIDs.update(state.energy_ref_id)
            refIDs.update(state.lande_ref_id)
            refIDs.update(state.level_ref_id)

    Sources = Reference.objects.filter(pk__in=refIDs)
    if not requestables or 'sources' in requestables:
        log.debug('Working on Sources.')
        try:
            for Source in XsamsSources(Sources, tap):
                yield Source
        except: errs+=generatorError(' Sources')

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


