# -*- coding: utf-8 -*-

from vamdctap.caselessdict import CaselessDict

RETURNABLES=CaselessDict({\
'NodeID': 'HIT',    # unique identifier for the HITRAN node
'SourceID': 'Source.sourceid',
'SourceAuthorName': 'Source.authors',
'SourceTitle': 'Source.title',
# NB my Refs model has pages, not page_begin and page_end:
'SourcePageBegin': 'Refs.pages',		
'SourceVolume': 'Source.volume',
'SourceYear': 'Source.year',
'SourceName': 'Source.journal',    # closest we can get to the journal name
'SourceCategory': 'Source.type',
'SourcePageBegin': 'Source.page_start',
'SourcePageEnd': 'Source.page_end',

'MethodID': 'Method.id',
'MethodCategory': 'Method.category',
'MethodDescription': 'Method.category',

'RadTransComments': '',
'RadTransMethodRef': 'EXP',
'RadTransFinalStateRef': 'RadTran.finalstateref',
'RadTransInitialStateRef': 'RadTran.initialstateref',
'RadTransWavenumberExperimentalValue': 'RadTran.nu',
'RadTransWavenumberExperimentalUnits': '1/cm',
'RadTransWavenumberExperimentalSourceRef': 'RadTran.nu_ref',
'RadTransWavenumberExperimentalAccuracy': 'RadTran.nu_err',
'RadTransProbabilityTransitionProbabilityAValue': 'RadTran.a',
'RadTransProbabilityTransitionProbabilityASourceRef': 'RadTran.a_ref',
'RadTransProbabilityTransitionProbabilityAAccuracy': 'RadTran.a_err',
'RadTransProbabilityProbability:MultipoleValue': 'RadTran.multipole',
# XXX test
'RadTransMolecularBroadeningXML': 'RadTran.broadening_xml',

'MolecularSpeciesChemicalName': 'Molecule.chemical_names',
'MolecularSpeciesOrdinaryStructuralFormula': 'Molecule.molec_name',
'MolecularSpeciesStoichiometricFormula': 'Molecule.stoichiometric_formula',
'MolecularSpeciesID': 'Molecule.inchikey',

'MolecularStateStateID':'MolState.id',
'MolecularStateMolecularSpeciesID':'MolState.inchikey',
'MolecularStateEnergyValue':'MolState.energy',
'MolecularStateEnergyUnit':'1/cm',
'MolecularStateEnergyOrigin':'Zero-point energy',
'MolecularStateCharacTotalStatisticalWeight':'MolState.g',

'MolQnStateID': 'MolQN.stateid',
'MolQnCase': 'MolQN.case',      # e.g. 'dcs', 'ltcs', ...
'MolQnLabel': 'MolQN.label',    # e.g. 'J', 'asSym', ...
'MolQnValue': 'MolQN.value',
'MolQnAttribute': 'MolQN.qn_attr',
'MolQnXML': 'MolQN.xml',
'Inchikey':'inchikey'})

RESTRICTABLES = CaselessDict({\
'Inchikey':'inchikey',
'RadTransWavenumberExperimentalValue':'nu',
'RadTransProbabilityTransitionProbabilityAValue':'a',
})
