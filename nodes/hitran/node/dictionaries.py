# -*- coding: utf-8 -*-

RETURNABLES={\
'NodeID': 'HIT',    # unique identifier for the HITRAN node
'XSAMSVersion': '0.2',
'SchemaLocation': '/Users/christian/research/VAMDC/XSAMS/release-0.2/xsams.xsd',

'SourceID': 'Source.refID',
'SourceAuthorName': 'Source.author_list()',
'SourceTitle': 'Source.title',
'SourcePageBegin': 'Source.page_start',		
'SourcePageEnd': 'Source.page_end',		
'SourceVolume': 'Source.volume',
'SourceYear': 'Source.year',
'SourceName': 'Source.journal',    # closest we can get to the journal name
'SourceCategory': 'Source.ref_type',
'SourceComments': 'Source.note',

'MethodID': 'Method.id',
'MethodCategory': 'Method.category',
'MethodDescription': 'Method.category',

# the node software refers to my Trans objects as RadTran
'RadTransComments': '',
'RadTransMethodRef': 'EXP',
'RadTransFinalStateRef': 'RadTran.statep.id',
'RadTransInitialStateRef': 'RadTran.statepp.id',
'RadTransWavenumber': 'RadTran.nu.val',
'RadTransWavenumberUnit': '1/cm',
'RadTransWavenumberRef': 'RadTran.nu.ref',
'RadTransWavenumberAccuracy': 'RadTran.nu.err',
'RadTransProbabilityA': 'RadTran.A.val',
'RadTransProbabilityAUnit': '1/s',
'RadTransProbabilityARef': 'RadTran.A.ref',
'RadTransProbabilityAAccuracy': 'RadTran.A.err',
'RadTransProbabilityMultipoleValue': 'RadTran.multipole',

# the node software calls my species (isotopologue) entity 'Molecule'
'MoleculeChemicalName': 'Molecule.molecule.common_name',
'MoleculeOrdinaryStructuralFormula': 'Molecule.molecule.ordinary_formula',
'MoleculeStoichiometricFormula': 'Molecule.molecule.stoichiometric_formula',
'MoleculeIonCharge': 'Molecule.molecule.charge',
'MoleculeID': 'Molecule.InChIKey',
'MoleculeInchi': 'Molecule.InChI',
'MoleculeInchiKey': 'Molecule.InChIKey',
'MoleculeSpeciesID': 'Molecule.InChIKey',
'MoleculeComment': 'Molecule.iso_name',
'MoleculeStructure': 'Molecule',    # we have an XML() method for this

'MoleculeStateID': 'MoleculeState.id',
'MoleculeStateMolecularSpeciesID': 'MoleculeState.iso.InChIKey_explicit',
'MoleculeStateEnergy': 'MoleculeState.energy',
'MoleculeStateEnergyUnit': '1/cm',
'MoleculeStateEnergyOrigin': 'Zero-point energy',
'MoleculeStateTotalStatisticalWeight': 'MoleculeState.g',
'MoleculeStateQuantumNumbers': 'MoleculeState',    # use the an XML() method

'MoleculeQnStateID': 'Qns.state',
'MoleculeQnCase': 'Qns.case',      # e.g. 'dcs', 'ltcs', ...
'MoleculeQnLabel': 'Qns.qn_name',    # e.g. 'J', 'asSym', ...
'MoleculeQnValue': 'Qns.qn_val',
'MoleculeQnAttribute': 'Qns.qn_attr',
'MoleculeQnXML': 'Qns.xml',
}

# MoleculeChemicalName and MoleculeStoichiometricFormula are associated with
# 'dummy' because the HITRAN node handles these RESTRICTABLES explicitly,
# transforming them into the corresponding InChIKeys
RESTRICTABLES = {\
'MoleculeChemicalName': 'dummy',
'MoleculeStoichiometricFormula': 'dummy',
'MoleculeInchiKey': 'iso__InChIKey_explicit',
'RadTransWavenumber': 'nu',
'RadTransWavelength': 'dummy', 
'RadTransProbabilityA': 'A',
}
