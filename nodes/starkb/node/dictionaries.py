# -*- coding: utf-8 -*-
from vamdctap.caselessdict import CaselessDict
RETURNABLES = ({\
'NodeID':'starkb',

'AtomStateID':'AtomState.id',
'AtomSymbol':'Atom.ion.symbol',
'AtomNuclearCharge':'Atom.ion.nuclear_charge',
'AtomSpeciesID':'Atom.particle_ion_id()',
'AtomIonCharge':'Atom.ion.ionization_decimal',


'AtomStateConfigurationLabel':'AtomState.config',
'AtomStateTermLabel':'AtomState.term',
#'AtomStateID':'AtomState.id',
'AtomStateTotalAngMom' : 'AtomState.j_asFloat()',

'RadTransBroadeningPressure':'RadTran',
'RadTransBroadeningPressureComment':'stark effect',
'RadTransBroadeningPressureLineshapeName':'Lorentzian',
'RadTransBroadeningPressureLineshapeParameterName':'gammaL',
'RadTransBroadeningPressureLineshapeParameterComment':'Broadening.comment',
'RadTransBroadeningPressureLineshapeParameterUnit':'A',
'RadTransBroadeningPressureLineshapeParameter':'Broadening.value',
'RadTransBroadeningPressureLineshapeParameterAccurracy':'',
'RadTransBroadeningPressureEnvironment':'Broadening.environment',

#'RadTransShiftingName':'test name',
#'RadTransShiftingParam':'ShiftingParam.value',
#'RadTransShiftingParamName':'test value',
#'RadTransShiftingParamUnits':'A',
#'RadTransShiftingEnv':'ShiftingParam.environment',

'RadTransFinalStateRef':'RadTran.upper_level.id',
'RadTransInitialStateRef':'RadTran.lower_level.id',

'RadTransWavelength':'RadTran.wavelength',
'RadTransWavelengthUnit':'A',


'EnvironmentID': 'Environment.id',
'EnvironmentTemperature' : 'Environment.temperature.temperature',
'EnvironmentTemperatureUnit' : 'K',
'EnvironmentTotalNumberDensity':'Environment.temperature.transitiondata.density',
'EnvironmentTotalNumberDensityUnit':'1/cm3',
'EnvironmentSpeciesName':'EnvSpecies.particle_ion_name()',
'EnvironmentSpeciesRef': 'EnvSpecies.particle_ion_id()',

'ParticleSpeciesID' : 'Particle.particle_ion_id()',
'ParticleName' : 'Particle.particle_ion_name()',
#'ParticleMass' : 'Particle.mass',
#'ParticleMassUnit' : 'Particle.massunit.value',
#'ParticleCharge' : 'Particle.charge',
})

RESTRICTABLES = ({\
'RadTransWavelength':'wavelength'
})
