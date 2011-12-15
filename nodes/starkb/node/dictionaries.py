# -*- coding: utf-8 -*-
from vamdctap.caselessdict import CaselessDict
RETURNABLES = ({\
'NodeID':'starkb',

#atomstate 
'AtomStateID':'AtomState.id',
'AtomSymbol':'Atom.ion.symbol',
'AtomNuclearCharge':'Atom.ion.nuclear_charge',
'AtomSpeciesID':'Atom.particle_ion_id()',
'AtomIonCharge':'Atom.ion.ion_charge',
'AtomStateConfigurationLabel':'AtomState.config',
'AtomStateTermLabel':'AtomState.term',
'AtomStateTotalAngMom' : 'AtomState.j_asFloat()',
'AtomStateRef':'AtomState.Sources',

#radiative transition
'RadTransBroadeningPressure':'RadTran',
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
'RadTransRefs':'RadTran.Sources',

# environments
'EnvironmentID': 'Environment.id',
'EnvironmentTemperature' : 'Environment.temperature.temperature',
'EnvironmentTemperatureUnit' : 'K',
'EnvironmentTotalNumberDensity':'Environment.temperature.transitiondata.density',
'EnvironmentTotalNumberDensityUnit':'1/cm3',
'EnvironmentSpeciesName':'EnvSpecies.particle_ion_name()',
'EnvironmentSpeciesRef': 'EnvSpecies.particle_ion_id()',

#source
'SourceTitle':'Source.encoded_title()',
'SourceCategory':'journal',
'SourceName' : 'Source.journal.encoded_name()',
'SourceVolume' : 'Source.volume',
'SourceYear' : 'Source.publication_year',
'SourceURI': 'Source.ads_reference',
'SourceVolume' : 'Source.volume',
'SourceID' : 'Source.id',

# particle
'ParticleSpeciesID' : 'Particle.particle_ion_id()',
'ParticleName' : 'Particle.particle_ion_name()',
#'ParticleMass' : 'Particle.mass',
#'ParticleMassUnit' : 'Particle.massunit.value',
#'ParticleCharge' : 'Particle.charge',
})

RESTRICTABLES = ({\
'RadTransWavelength':'wavelength',
'AtomSymbol':'target__ion__symbol',
'IonCharge':'target__ion__ion_charge',
'EnvironmentTemperature' : 'temperature',
'EnvironmentTotalNumberDensity':'density'
})
