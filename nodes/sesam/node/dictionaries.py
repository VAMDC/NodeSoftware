# -*- coding: utf-8 -*-
"""
ExampleNode dictionary definitions.
"""

# The returnable dictionary is used internally by the node and defines
# all the ways the VAMDC standard keywords (left-hand side) maps to
# the internal database representation queryset (right-hand side)
#
# When writing this, it helps to remember that dictionary is applied
# in a loop to every matching *instance* of the queryset variables
# returned from queryfunc.py. So in the example below, all 'AtomStates'
# will be looped over by the node software, using the name 'AtomState'
# (singular). 'AtomState' will be one single instance of a matching
# database object, from which we extract everything we need by parsing
# the VAMDC_standard LHS of this dictionary to how it maps to our specific
# database on the RHS. So, when looping through all AtomState objects
# matching the given query, the generator will for example know that
# to get the AtomStateEnergy VAMDC value, it will need to look at
# the AtomState.energy, i.e. the "energy" property of the current
# database object being worked on.
#
# (if you look at queryfuncs.py, you'll see 'AtomStates' being
#  assigned)

RETURNABLES = {\
'NodeID':'sesam', # required
############################################################
'MethodID':'Method.id',
'MethodCategory':'Method.category',
############################################################
#Molecule
'MoleculeStoichiometricFormula':'Molecule.stoichiometric_formula',
'MoleculeOrdinaryStructuralFormula':'Molecule.ordinary_structural_formula',
'MoleculeChemicalName':'Molecule.chemical_name',
'MoleculeInchiKey':'Molecule.inchikey',
'MoleculeInchi':'Molecule.inchi',
'MoleculeSpeciesID':'Molecule.id',
############################################################
#Sources
'SourceID':'Source.id',
'SourceCategory':'Source.sourcecategory.value',
'SourceYear':'Source.year',
'SourceVolume':'Source.volume',
'SourceDOI':'Source.doi',
'SourceURI':'Source.uri',
'SourceAuthorName':'Source.authornames()',
############################################################
'RadTransID':'RadTran.id',
'RadTransWavelength':'RadTran.wavelength',
'RadTransWavelengthUnit':u'A',
'RadTransSpeciesRef':'RadTran.molecule.id',
'RadTransLowerStateRef':'RadTran.lowerstate.id',
'RadTransUpperStateRef':'RadTran.upperstate.id',
'RadTransProbabilityOscillatorStrength':'RadTran.oscillator_strength',
'RadTransWavenumber':'RadTran.getWavenumbers()',
'RadTransWavenumberMethod':'RadTran.getWavenumberMethods()',
'RadTransWavenumberComment':'RadTran.getWavenumberComments()',
'RadTransWavenumberUnit':'1/cm',
'RadTransProbabilityA' : 'RadTran.transition_probability',
'RadTransProbabilityAUnit' : '1/s',
'RadTransRefs' : 'RadTran.source.id',


############################################################
'MoleculeStateEnergy':'MoleculeState.energy',
'MoleculeStateEnergyOrigin':'MoleculeState.origin',
'MoleculeStateEnergyUnit':'1/cm',
'MoleculeStateID':'MoleculeState.id',
'MoleculeStateTotalStatisticalWeight':'MoleculeState.total_statistical_weight',
'MoleculeQnCase':'MoleculeState.SubCase.name',
'MoleculeQNElecStateLabel':'MoleculeState.Case.elec_state_label',
'MoleculeQNJ':'MoleculeState.Case.j',
'MoleculeQNF':'MoleculeState.Case.f',
'MoleculeQNr':'MoleculeState.Case.r',
'MoleculeQNparity':'MoleculeState.Case.parity',
#dcs,hundb
'MoleculeQNv':'MoleculeState.SubCase.v',
'MoleculeQNF1':'MoleculeState.SubCase.f1',
'MoleculeQNasSym':'MoleculeState.SubCase.as_sym',
'MoleculeQNelecInv':'MoleculeState.SubCase.elec_inv',
'MoleculeQNelecRefl':'MoleculeState.SubCase.elec_refl',
'MoleculeQNLambda':'MoleculeState.SubCase.lambda_field',
'MoleculeQNS':'MoleculeState.SubCase.s',
'MoleculeQNN':'MoleculeState.SubCase.n',
'MoleculeQNSpinComponentLabel':'MoleculeState.SubCase.spin_component_label',
'MoleculeQNF1':'MoleculeState.SubCase.f1',
'MoleculeQNKronigParity':'MoleculeState.SubCase.kronig_parity',
}

# The restrictable dictionary defines limitations to the search.
# The left-hand side is standardized, the righ-hand size should
# be defined in Django query-language style, where e.g. a search
# for the Species.atomic field  would be written as species__atomic.

RESTRICTABLES = {\
'MoleculeChemicalName':'ordinarystructuralformula',
'MoleculeStoichiometricFormula':'molecule__stoichiometric_formula',
'RadTransWavelength':'wavelength',
'RadTransProbabilityOscillatorStrength':'oscillator_strength',
'StateEnergy':'lowerstate__energy',
'RadTransWavenumber':'wavenumber_calculated',
'InchiKey':'inchikey',
'lower.StateEnergy':'lowerstate__energy',
'upper.StateEnergy':'upperstate__energy',
'RadTransProbabilityA':'transition_probability',
}

PREFIXES = {\
#'lower.StateEnergy':'lowerstate__energy',
#'upper.StateEnergy':'upperstate__energy',
}

