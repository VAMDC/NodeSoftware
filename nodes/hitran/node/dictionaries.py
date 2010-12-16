# -*- coding: utf-8 -*-

from vamdctap.caselessdict import CaselessDict

RETURNABLES=CaselessDict({\
'SourceID':'Refs.sourceid',
'SourceAuthorName':'Refs.author',
'SourceTitle':'Refs.title',
# NB my Refs model has pages, not page_begin and page_end:
'SourcePageBegin':'Refs.pages',		
'SourceVolume':'Refs.volume',
'SourceYear':'Refs.year',
'SourceName':'Refs.journal',    # closest we can get to the journal name

'RadTransComments':'',
'RadTransFinalStateRef':'RadTran.finalstateref',
'RadTransInitialStateRef':'RadTran.initialstateref',
'RadTransWavenumberExperimentalValue':'RadTran.nu',
'RadTransWavenumberExperimentalSourceRef':'RadTran.nu_ref',
'RadTransWavenumberExperimentalAccuracy':'RadTran.nu_err',
'RadTransProbabilityTransitionProbabilityAValue':'RadTran.a',
'RadTransProbabilityTransitionProbabilityASourceRef':'RadTran.a_ref',
'RadTransProbabilityTransitionProbabilityAAccuracy':'RadTran.a_err',
'RadTransProbabilityProbability:MultipoleValue':'RadTran.multipole',

'MolecularSpeciesChemicalName':'Molecule.chemical_names',
'MolecularSpeciesOrdinaryStructuralFormula':'Molecule.molec_name',
'MolecularSpeciesOrdinaryStoichiometricFormula': \
        'Molecule.stoichiometric_formula',

'MolecularStateStateID':'MolState.stateid',
'MolecularStateEnergyValue':'MolState.energy',
'MolecularStateEnergyUnit':'cm-1',
'MolecularStateEnergyOrigin':'Zero-point energy',
'MolecularStateCharacTotalStatisticalWeight':'MolState.g',

'MolQnStateID': 'MolQN.stateid',
'MolQnCase': 'MolQN.case',      # e.g. 'dcs', 'ltcs', ...
'MolQnLabel': 'MolQN.label',    # e.g. 'J', 'asSym', ...
'MolQnValue': 'MolQN.value'
})

RESTRICTABLES = CaselessDict({\
'Inchikey':'inchikey',
'RadTransWavenumberExperimentalValue':'nu',
'RadTransProbabilityTransitionProbabilityAValue':'a',
})
