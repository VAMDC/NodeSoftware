# -*- coding: utf-8 -*-

RESTRICTABLES = {\
'AtomSymbol':'states__species__atomsymbol',
'AtomNuclearCharge':'states__species__atomnuclearcharge',
'AtomIonCharge':'states__species__atomioncharge',
'RadTransWavelengthExperimentalValue':'radtranswavelengthexperimentalvalue'
}

RETURNABLES = {\
'NodeID':'chianti',
'AtomSymbol':'AtomState.atomsymbol',
'AtomNuclearCharge':'AtomState.atomnuclearcharge',
'AtomIonCharge':'AtomState.atomioncharge',
'AtomStateS':'AtomState.atomstates',
'AtomStateL':'AtomState.atomstatel',
'AtomStateTotalAngMom':'AtomState.atomstatetotalangmom',
'AtomStateEnergyExperimentalValue':'AtomState.atomstateenergyexperimentalvalue',
'AtomStateEnergyTheoreticalValue':'AtomState.atomstateenergytheoreticalvalue',
'AtomStateConfigurationLabel':'AtomState.atomstateconfigurationlabel',
'RadTransWavelengthExperimentalValue':'RadTran.radtranswavelengthexperimentalvalue',
'RadTransWavelengthExperimentalUnits':u'A', # Angstrom symbol
'RadTransWavelengthTheorecticalValue':'RadTran.radtranswavelengththeoreticalvalue',
'RadTransWavelengthTheoreticalUnits':u'A', # Angstrom symbol
'RadTransProbabilityWeightedOscillatorStrengthValue':'RadTran.radtransprobabilityweightedoscillatorstrengthvalue',
'RadTransProbabilityTransitionProbabilityAValue':'RadTran.radtransprobabilitytransitionprobabilityavalue',
'RadTransProbabilityTransitionProbabilityAUnits':u'Hz'
}
