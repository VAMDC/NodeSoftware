# -*- coding: utf-8 -*-

RESTRICTABLES = {\
'AtomSymbol':'atomsymbol',
'AtomNuclearCharge':'chiantiradtransfinalstateindex__atomnuclearcharge',
'AtomIonCharge':'atomioncharge',
'AtomStateEnergyExperimentalValue':'chiantiradtransfinalstateindex__atomstateenergyexperimentalvalue',
'AtomStateEnergyTheoreticalValue':'chiantiradtransfinalstateindex__atomstateenergytheoreticalvalue',
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

from vamdctap.caselessdict import CaselessDict
RESTRICTABLES = CaselessDict(RESTRICTABLES)
RETURNABLES = CaselessDict(RETURNABLES)
