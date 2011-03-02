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
'RadTransWavenumber': 'RadTran.nu',
'RadTransWavenumberUnit': '1/cm',
'RadTransWavenumberRef': 'RadTran.nu_ref',
'RadTransWavenumberAccuracy': 'RadTran.nu_err',
'RadTransProbabilityA': 'RadTran.a',
'RadTransProbabilityAUnit': '1/s',
'RadTransProbabilityARef': 'RadTran.a_ref',
'RadTransProbabilityAAccuracy': 'RadTran.a_err',
'RadTransProbabilityMultipoleValue': 'RadTran.multipole',
# XXX test
'RadTransMolecularBroadeningXML': 'RadTran.broadening_xml',

'MoleculeChemicalName': 'Molecule.chemical_names',
'MoleculeOrdinaryStructuralFormula': 'Molecule.molec_name',
'MoleculeStoichiometricFormula': 'Molecule.stoichiometric_formula',
'MoleculeID': 'Molecule.inchikey',
'MoleculeInChI': 'Molecule.inchi',
'MoleculeInChIKey': 'Molecule.inchikey',
# use the Comment field to 
'MoleculeComment': 'Molecule.iso_name',

'MoleculeStateStateID':'MoleculeState.id',
'MoleculeStateMolecularSpeciesID':'MoleculeState.inchikey',
'MoleculeStateEnergyValue':'MoleculeState.energy',
'MoleculeStateEnergyUnit':'1/cm',
'MoleculeStateEnergyOrigin':'Zero-point energy',
'MoleculeStateCharacTotalStatisticalWeight':'MoleculeState.g',
'MoleculeStateQuantumNumbers': 'MoleculeState.parsed_qns',

'MoleculeQnStateID': 'MolQN.stateid',
'MoleculeQnCase': 'MolQN.case',      # e.g. 'dcs', 'ltcs', ...
'MoleculeQnLabel': 'MolQN.label',    # e.g. 'J', 'asSym', ...
'MoleculeQnValue': 'MolQN.value',
'MoleculeQnAttribute': 'MolQN.qn_attr',
'MoleculeQnXML': 'MolQN.xml',
'Inchikey':'inchikey'})

RESTRICTABLES = CaselessDict({\
'Inchikey':'inchikey',
'RadTransWavenumberExperimentalValue':'nu',
'RadTransProbabilityTransitionProbabilityAValue':'a',
})
