# -*- coding: utf-8 -*-

from vamdctap.unitconv import invcm2eV

# In the RESTRICTABLES dictionary, keys are names from the dictionary and values are 
# names from the Django model for the transitions table.
#
# Where a field is actually in the transitions model (i.e. in the transitions table and
# not in a linked table) then the name of the field appears without punctuation. Where
# the field is in a related model (meaning that Django must join tables to get at it),
# the double-underscore operator expressed the chain of relations.
#
# E.g., radtranswavelengthexperimentalvalue refers a field directly in the transitions model.
# finalstateindex__species__atomsymbol refers to the atomsymbol field in the
# species model. The transitions model has a foreign key to the states model in a field
# called finalstateindex. The states model has a foreign key to the species model in a
# field called species. All three parts of finalstateindex__species__atomsymbol are names of 
# fields in models; names of entire models are not part of this syntax.

RESTRICTABLES = {\
'AtomSymbol':'finalstateindex__species__atomsymbol',
'AtomNuclearCharge':'finalstateindex__species__atomnuclearcharge',
'AtomIonCharge':'finalstateindex__species__atomioncharge',
'AtomStateEnergy':('finalstateindex__atomstateenergyexperimentalvalue', invcm2eV),
'RadTransWavelength':'wavelength'
}

RETURNABLES = {\
'NodeID':'chianti', # Constant value

'MethodID':'Method.id',
'MethodCategory':'Method.category',

'AtomSpeciesId':'Atom.id',
'AtomSymbol':'Atom.atomsymbol',
'AtomNuclearCharge':'Atom.atomnuclearcharge',
'AtomIonCharge':'Atom.atomioncharge',

'AtomStateId':'AtomState.id',
'AtomStateS':'AtomState.atomstates',
'AtomStateL':'AtomState.atomstatel',
'AtomStateTotalAngMom':'AtomState.atomstatetotalangmom',
'AtomStateEnergyExperimentalValue':'AtomState.atomstateenergyexperimentalvalue',
'AtomStateEnergyTheoreticalValue':'AtomState.atomstateenergytheoreticalvalue',
'AtomStateConfigurationLabel':'AtomState.atomstateconfigurationlabel',

'RadTransWavelength':'RadTran.wavelength',
'RadTransWavelengthMethod': 'RadTran.wavelengthmethod',
'RadTransWavelengthUnit':u'A', # Constant: Angstrom symbol
'RadTransProbabilityWeightedOscillatorStrength':'RadTran.weightedoscillatorstrength',
'RadTransProbabilityA':'RadTran.probabilitya',
'RadTransProbabilityAUnits':u'1/s',
'RadTransInitialStateRef':'RadTran.initialstateindex.id',
'RadTransFinalStateRef':'RadTran.finalstateindex.id',
'RadTransSpeciesRef':'RadTran.initialstateindex.species.id'
}
