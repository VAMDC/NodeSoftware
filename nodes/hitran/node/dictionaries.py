# -*- coding: utf-8 -*-

RETURNABLES={\
'NodeID': 'HIT',    # unique identifier for the HITRAN node

'SourceID': 'Source.sourceid',
'SourceAuthorName': 'Source.authors',
'SourceTitle': 'Source.title',
'SourcePageBegin': 'Refs.page_start',		
'SourcePageEnd': 'Refs.page_end',		
'SourceVolume': 'Refs.volume',
'SourceYear': 'Refs.year',
'SourceName': 'Refs.journal',    # closest we can get to the journal name
'SourceCategory': 'Refs.type',
'SourcePageBegin': 'Refs.page_start',
'SourcePageEnd': 'Refs.page_end',

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
'MoleculeInchi': 'Molecule.inchi',
'MoleculeInchiKey': 'Molecule.inchikey',
'MoleculeSpeciesID': 'Molecule.inchikey',
# use the Comment field to 
'MoleculeComment': 'Molecule.iso_name',

'MoleculeStateID':'MoleculeState.id',
'MoleculeStateMolecularSpeciesID':'MoleculeState.inchikey',
'MoleculeStateEnergyValue':'MoleculeState.energy',
'MoleculeStateEnergy':'MoleculeState.energy',
'MoleculeStateEnergyUnit':'1/cm',
'MoleculeStateEnergyOrigin':'Zero-point energy',
'MoleculeStateCharacTotalStatisticalWeight':'MoleculeState.g',
'MoleculeStateQuantumNumbers': 'MoleculeState',

'MoleculeQnStateID': 'MolQN.stateid',
'MoleculeQnCase': 'MolQN.case',      # e.g. 'dcs', 'ltcs', ...
'MoleculeQnLabel': 'MolQN.label',    # e.g. 'J', 'asSym', ...
'MoleculeQnValue': 'MolQN.value',
'MoleculeQnAttribute': 'MolQN.qn_attr',
'MoleculeQnXML': 'MoleculeState.get_qn_xml()',
'Inchikey':'inchikey'}

# MoleculeChemicalName and MoleculeStoichiometricFormula are associated with
# 'dummy' because the HITRAN node handles these RESTRICTABLES explicitly,
# transforming them into the corresponding InChIKeys
RESTRICTABLES = {\
'MoleculeChemicalName': 'dummy',
'MoleculeStoichiometricFormula': 'dummy',
'MoleculeInchiKey': 'inchikey',
'RadTransWavenumber': 'nu',
'RadTransProbabilityA': 'a',
}
