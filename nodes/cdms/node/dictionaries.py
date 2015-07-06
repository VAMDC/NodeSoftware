RETURNABLES = {
'XSAMSVersion':'1.0',
'AtomInchi':'Atom.inchi',
'AtomInchiKey':'Atom.inchikey',
'AtomVAMDCSpeciesID':'Atom.inchikey',
'AtomIonCharge':'Atom.molecule.formalcharge',
#'AtomMass':'AtomState.',
'AtomMassNumber':'Atom.massnumber', #getMassNumber()',
'AtomNuclearCharge':'Atom.atom.nuclearcharge',
#'AtomNuclearSpin':'AtomState.',
'AtomSpeciesID':'Atom.id',
#'AtomStateCompositionComments':'AtomState.',
#'AtomStateConfigurationLabel':'AtomState.',
#'AtomStateCoupling':'AtomState.',
#'AtomStateDescription':'AtomState.',
'AtomStateEnergy':'AtomState.energy',
'AtomStateEnergyOrigin':'AtomState.energyorigin', #'Zero-point energy',
'AtomStateEnergyUnit':'1/cm', 
#'AtomStateHyperfineConstantA':'AtomState.',
#'AtomStateHyperfineConstantB':'AtomState.',
'AtomStateID':'AtomState.id',
'AtomStateAuxillary':'AtomState.auxillary()',
#'AtomStateIonizationEnergy':'AtomState.',
#'AtomStateJ1':'AtomState.',
#'AtomStateJ2':'AtomState.',
#'AtomStateK':'AtomState.',
#'AtomStateKappa':'AtomState.',
#'AtomStateL':'AtomState.L',
#'AtomStateLandeFactor':'AtomState.',
#'AtomStateLifeTime':'AtomState.',
#'AtomStateMagneticQuantumNumber':'AtomState.',
#'AtomStateMixingCoefficient':'AtomState.',
#'AtomStateParity':'AtomState.',
#'AtomStatePolarizability':'AtomState.',
#'AtomStateQuantumDefect':'AtomState.',
#'AtomStateRef':'AtomState.',
#'AtomStateS':'AtomState.S',
#'AtomStateS2':'AtomState.',
'AtomStateStatisticalWeight':'AtomState.degeneracy',
'AtomStateTermLSL':'Component.L', #AtomState.attach_atomic_qn()',
'AtomStateTermLSS':'Component.S', #AtomState.S',
'AtomStateTotalAngMom':'AtomState.attach_atomic_qn()',
'AtomStateHyperfineMomentum':'AtomState.F',
'AtomSymbol':'Atom.molecule.elementsymbol', #molecule.stoichiometricformula',

'MethodComment':'Method.description',
'MethodCategory':'Method.category', # <- NEW
'MethodDescription':'Method.description', # <- NEW
'MethodRef':'Method.ref',
'MethodID':'Method.id', # <- NEW
'MethodSourceRef':'Method.sourcesref', # <- NEW

'MoleculeChemicalName':'Molecule.molecule.trivialname',
'MoleculeID':'Molecule.id',
'MoleculeInchi':'Molecule.inchi',
'MoleculeInchiKey':'Molecule.inchikey',
'MoleculeVAMDCSpeciesID':'Molecule.inchikey',
'MoleculePartitionFunction':'Molecule.pfT',
'MoleculePartitionFunctionUnit':'K',
'MoleculePartitionFunctionQ':'Molecule.pfQ',
'MoleculePartitionFunctionNSIName':'Molecule.pfnsiname', #nuclearspinisomer',
'MoleculePartitionFunctionNSILowestEnergyStateRef':'Molecule.pflowestrovibstateid', #nsiorigin()',
'MoleculePartitionFunctionNSISymGroup':'Molecule.pfsymmetrygroup', #msgroup',
'MoleculePartitionFunctionNSILowestRoVibSym':'Molecule.pfnsilowestrovibsym',

'MoleculeMolecularWeight':'Molecule.massnumber', #getMassNumber()',
#'MoleculeNormalModeHarmonicFrequency':'Molecule.',
#'MoleculeNormalModeIntensity':'Molecule.',
#'MoleculeNuclearSpins':'Molecule.',
#'MoleculeNuclearSpinsAtomArray':'Molecule.',
#'MoleculeNuclearSpinsBondArray':'Molecule.',
'MoleculeSpeciesID':'Molecule.id',
'MoleculeStructure': 'Molecule',    # we have an XML() method for this

#'MoleculeStateCharacLifeTime':'MoleculeState.',
#'MoleculeStateCharacNuclearSpinSymmetry':'MoleculeState.',
'MoleculeStateEnergy':'MoleculeState.energy',
'MoleculeStateEnergyOrigin':'MoleculeState.origin()', #'Zero-point energy',
'MoleculeStateEnergyUnit':'1/cm',
'MoleculeStateEnergyMethod':'MoleculeState.dataset_id',
'MoleculeStateTotalStatisticalWeight':'MoleculeState.degeneracy', # has to be changed  <- new
'MoleculeStateNSIName':'MoleculeState.nsiname()', #nuclearspinisomer',
'MoleculeStateNSILowestEnergyStateRef':'MoleculeState.nsi.lowestrovibstateid()', #nsiorigin()',
'MoleculeStateNSISymGroup':'MoleculeState.nsi.symmetrygroup', #msgroup',
'MoleculeStateNSILowestRoVibSym':'MoleculeState.nsi.lowestrovibsym', #nuclearspinisomersym',
'MoleculeStateNuclearStatisticalWeight':'MoleculeState.nuclearstatisticalweight',
'MoleculeStateID':'MoleculeState.id',
'MoleculeStateAuxillary':'MoleculeState.auxillary()',
#'MoleculeStateQuantumNumbers':'MoleculeState.parsed_qns',
'MoleculeStateQuantumNumbers':'MoleculeState',
#'MoleculeStateMethod':'MoleculeState.dataset_id',
'MoleculeStoichiometricFormula':'Molecule.molecule.stoichiometricformula',
'MoleculeOrdinaryStructuralFormula':'Molecule.isotopolog',
'MoleculeComment': 'Molecule.shortcomment', #'Molecule.name',
'MoleculeQnStateID': 'MolQN.stateid', # <- new
'MoleculeQnCase': 'MolQN.case',       # <- new 
'MoleculeQnLabel': 'MolQN.label',     # <- new 
'MoleculeQnValue': 'MolQN.value',     # <- new
'MoleculeQnAttribute': 'MolQN.attribute', # <- new
#'MoleculeQnXML': 'MolQN.xml',  #

'NodeID':'CDMS',

#'NonRadTranEnergy':'',
#'NonRadTranProbability':'',
#'NonRadTranWidth':'',
#'NormalModeHarmonicFrequency':'Molecule.',
#'NormalModeIntensity':'Molecule.',
#'NormalModeSymmetry':'Molecule.',
'RadTransID':'RadTran.id',
#'RadTransBandCentre':'RadTran.',
#'RadTransBandWidth':'RadTran.',
#'RadTransBroadeningComment':'RadTran.',
#'RadTransBroadeningInstrumentLineshapeName':'RadTran.',
#'RadTransBroadeningInstrumentLineshapeParameter':'RadTran.',
#'RadTransBroadeningInstrumentLineshapeParameterName':'RadTran.',
#'RadTransBroadeningInstrumentRef':'RadTran.',
#'RadTransBroadeningNaturalLineshapeName':'RadTran.',
#'RadTransBroadeningNaturalLineshapeParameter':'RadTran.',
#'RadTransBroadeningNaturalLineshapeParameterName':'RadTran.',
#'RadTransBroadeningNaturalRef':'RadTran.',
#'RadTransBroadeningRef':'RadTran.',
#'RadTransBroadeningStarkLineshapeName':'RadTran.',
#'RadTransBroadeningStarkLineshapeParameter':'RadTran.',
#'RadTransBroadeningStarkLineshapeParameterName':'RadTran.',
#'RadTransBroadeningStarkRef':'RadTran.',
#'RadTransBroadeningVanDerWaalsLineshapeName':'RadTran.',
#'RadTransBroadeningVanDerWaalsLineshapeParameter':'RadTran.',
#'RadTransBroadeningVanDerWaalsLineshapeParameterName':'RadTran.',
#'RadTransBroadeningVanDerWaalsRef':'RadTran.',
#'RadTransComments':'RadTran.',
#'RadTransEffectiveLandeFactor':'RadTran.',
#'RadTransEnergy':'RadTran.',
'RadTransUpperStateRef':'RadTran.upperstateref_id',
'RadTransLowerStateRef':'RadTran.lowerstateref_id',
#'RadTransFrequency':'RadTran.get_exp_transitions()', #frequencyArray',
#'RadTransFrequency':'RadTran.attach_exp_frequencies()',
'RadTransFrequency':'eval(RadTran.frequencies)',
'RadTransFrequencyUnit':'MHz', #RadTran.units',
'RadTransFrequencyAccuracy':'eval(RadTran.uncertainties)',
'RadTransFrequencyRef':'eval(RadTran.references)',
#'RadTransFrequencyMethod':'RadTran.freqmethodref_id',
#'RadTransFrequencyMethod':'RadTran.species_id',
'RadTransFrequencyMethod':'eval(RadTran.methods)',
'RadTransProbabilityA':'RadTran.einsteina',
'RadTransProbabilityAUnit':'1/cm', # <-New
'RadTransProbabilityIdealisedIntensity':'RadTran.intensity',
#'RadTransProbabilityLineStrength':'RadTran.',
#'RadTransProbabilityLog10WeightedOscillatorStrength':'RadTran.intensity',
'RadTransProbabilityMultipole':'E2',
#'RadTransProbabilityOscillatorStrength':'RadTran.',
#'RadTransProbabilityWeightedOscillatorStrength':'RadTran.',
'RadTransProcess':'excitation', # CDMS transitions are always absorption lines
#'RadTransRefs':'RadTran.',
'RadTransSpeciesRef':'RadTran.specie_id',
#'RadTransWavelength':'RadTran.',
#'RadTransWavenumber':'RadTran.',
#'RadTransFrequencyEval':'RadTran.evaluations',
#'RadTransFrequencyEvalRecommended':'RadTran.recommendations',
#'RadTransFrequencyEvalRef':'RadTran.evalrefs',

'RadTransCode':'eval(str(RadTran.processclass))',

'SourceAuthorName':'Source.getAuthorList()',
'SourceCategory':'Source.category',
'SourceID':'Source.id',
'SourceName':'Source.name',
'SourcePageBegin':'Source.pageBegin',
'SourcePageEnd':'Source.pageEnd',
#'SourceTitle':'Source.title',
#'SourceURI':'Source.',
'SourceVolume':'Source.vol',
'SourceYear':'Source.year',
'SourceDOI':'Source.doi'
}


# import the unit converter functions
from vamdctap.unitconv import *
from string import strip
import sys
# Q-objects for always True / False
QTrue = Q(pk=F('pk'))
QFalse = ~QTrue

OPTRANS= { # transfer SQL operators to django-style
    '<':  '__lt',
    '>':  '__gt',
    '=':  '__exact',
    '<=': '__lte',
    '>=': '__gte',
    '!=': '',
    '<>': '',
    'in': '__in',
    'like': '',
}

def atomsymbol(r,op,*rhs):
    """
    """
    try:

        if op=='in':
            if not (rhs[0]=='(' and rhs[-1]==')'):
                log.error('Values for IN not bracketed: %s'%rhs)
            else: rhs=rhs[1:-1]
            ins = map(strip,rhs,('\'"',)*len(rhs))
            return Q(**{'specie__molecule__stoichiometricformula'+'__in':ins})& Q(**{'specie__molecule__numberofatoms'+'':'Atomic'})
    
        op = OPTRANS[op]
        ins = map(strip,rhs,('\'"',)*len(rhs))
        return Q(**{'specie__molecule__stoichiometricformula'+op:ins[0]}) & Q(**{'specie__molecule__numberofatoms'+'':'Atomic'})

    except Exception, e:
        #print >> sys.stderr, e
        #print >> sys.stderr, "RHS: op: "+op
        #for i in rhs:
        #    print >> sys.stderr, i
    
        #print >> sys.stderr, "DICTIONARY EX"
#        return Q(**{'specie__molecule__stoichiometricformula'+'__exact':'C'}) #Q(**{'specie__molecule__numberofatoms'+'':'Atomic'})
        return Q(pk__isnull=True)

def stoichiometricformula(r,op,rhs):
    """
    """
    try:
        op = OPTRANS[op]
        #float(rhs)
        return Q(**{'specie__molecule__stoichiometricformula'+op:rhs}) & Q(**{'specie__molecule__numberofatoms'+'!=':'Atomic'})
    except:
        return Q(pk__isnull=True)


def processclass(r, op, *rhs):
    """
    Generate filter for process classes. Information on process classes are not
    stored in a single field in the database. 
    """
    try:

        if op=='in':
            if not (rhs[0]=='(' and rhs[-1]==')'):
                log.error('Values for IN not bracketed: %s'%rhs)
            else: rhs=rhs[1:-1]
            
            ins = map(strip,rhs,('\'"',)*len(rhs))

            for i in ins:
                if i[:3]=='hyp':
                    try:
                        q = q & Q(**{'hfsflag__exact':i[3]})
                    except NameError:
                        q = Q(**{'hfsflag__exact':i[3]})
            return q
        else:
            op = OPTRANS[op]
#            ins = rhs.strip('\'"')
            ins = map(strip,rhs,('\'"',)*len(rhs))
            ins = ins[0]
            if ins[:3]=='hyp':
                return Q(**{'hfsflag'+op:ins[3]})
            else:
                return QFalse
            
            
        return QFalse
    except:
        return QFalse

def environment(r, op, *rhs):
    """
    This is currently a dummy to pass the temperature as a variable to queryfunc.py
    """
    return Q(pk__isnull=False)


RESTRICTABLES = { 
#'AsOfDate':'',
#'AtomInchi':'',
#'AtomInchiKey':'',
'IonCharge':'specie__molecule__formalcharge',
#'AtomMass':'',
'AtomMassNumber':'specie__atom__massnumber',
'AtomNuclearCharge':'specie__atom__nuclearcharge',
#'AtomNuclearSpin':'',
#'AtomStateCoupling':'',
#'AtomStateEnergy':'',
#'AtomStateHyperfineMomentum':'',
#'AtomStateID':'',
#'AtomStateIonizationEnergy':'',
#'AtomStateKappa':'',
#'AtomStateLandeFactor':'',
#'AtomStateLifeTime':'',
#'AtomStateMagneticQuantumNumber':'',
#'AtomStateMixingCoefficient':'',
#'AtomStateParity':'',
#'AtomStatePolarizability':'',
#'AtomStateQuantumDefect':'',
#'AtomStateStatisticalWeight':'',
#'AtomSymbol':'',
'AtomSymbol':'specie__atom__element', #molecule__elementsymbol', #atomsymbol, #'specie__molecule__stoichiometricformula',
'MoleculeInchiKey':'specie__inchikey',
'InchiKey':'specie__inchikey',
'VAMDCSpeciesID':'specie__inchikey',
'MoleculeChemicalName':'specie__molecule__trivialname',
#'MoleculeMolecularWeight':'',
#'MoleculeNormalModeHarmonicFrequency':'',
#'MoleculeNormalModeIntensity':'',
#'MoleculeStateCharacLifeTime':'',
#'MoleculeStateCharacNuclearSpinSymmetry':'',
'MoleculeStateNSIName':'lowerstateref__nsi__name', #nuclearspinisomer',
'MoleculeStateNuclearSpinIsomer':'lowerstateref__nsi__name',
'MoleculeStateEnergy':'lowerstateref__energy',
#'MoleculeStateID':'',
'MoleculeStoichiometricFormula':'specie__molecule__stoichiometricformula',
#'MoleculeStoichiometricFormula':stoichiometricformula,
'MoleculeOrdinaryStructuralFormula':'specie__isotopolog',
#'NonRadTranEnergy':'',
#'NonRadTranProbability':'',
#'NonRadTranWidth':'',
#'NormalModeSymmetry':'',
#'RadTransBandCentre':'',
#'RadTransBandWidth':'',
#'RadTransEffectiveLandeFactor':'',
'RadTransEnergy':('frequency',eV2MHz),
'RadTransFrequency':'frequency',
'RadTransProbabilityA':'einsteina',
'RadTransProbabilityIdealisedIntensity':'intensity',
#'RadTransProbabilityLineStrength':'',
#'RadTransProbabilityLog10WeightedOscillatorStrength':'',
#'RadTransProbabilityOscillatorStrength':'',
#'RadTransProbabilityWeightedOscillatorStrength':'',
'RadTransWavelength':('frequency',Angstr2MHz),
#'RadTransWavelength':'frequency',
'RadTransWavenumber':('frequency',invcm2MHz),
'RadTransCode':processclass,
#'SourceCategory':'',
#'SourceYear':'',
'MoleculeSpeciesID':'specie',
'SpeciesID':'specie',
'Lower.StateEnergy':'lowerstateref__energy',
'Upper.StateEnergy':'upperstateref__energy',
'StateEnergy':bothStates,
'EnvironmentTemperature':'environmenttemp',
}

CDMSONLYRESTRICTABLES = {
    # 'MoleculeSpeciesID':'species',
    'dataset':'dataset',
    'hfsflag':'hfsflag',
    'getonlycalc':'getonlycalc',
    'geteinsteina':'geteinsteina',
    'MoleculeSpeciesTag':'specie__speciestag',
}
