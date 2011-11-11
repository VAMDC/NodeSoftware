# -*- coding: utf-8 -*-
RETURNABLES = {\
'NodeID':'Tipbase',
                           
'AtomStateID':'AtomState.id',

'AtomSymbol':'Atom.atomicion.isotope.chemicalelement.elementsymbol',
'AtomSpeciesID':'Atom.atomicion.id',
'AtomNuclearCharge':'Atom.atomicion.isotope.chemicalelement.nuclearcharge',
'AtomIonCharge':'Atom.atomicion.ioncharge',
'AtomMassNumber':'Atom.atomicion.isotope.massnumber',


'AtomStateEnergy':'AtomState.stateenergy',
'AtomStateEnergyUnit':'AtomState.stateenergyunit.value',

'AtomStateParity' : 'AtomState.parity.value',
'AtomStateMixingCoeff':'AtomState.Component.mixingcoefficient',
'AtomStateMixingCoeffClass' : 'AtomState.Component.mixingclass.value',
'AtomStateLifeTime': 'AtomState.lifetime',
'AtomStateStatisticalWeight' : 'AtomState.statisticalweight',
'AtomStateStatisticalWeightUnit' : 'AtomState.statisticalweightunit.value',
'AtomStateLifeTimeUnit': 'AtomState.lifetimeunit.value',
'AtomStateLifeTimeDecay':'totalRadiative',
'AtomStateIonizationEnergy' : 'AtomState.ionizationenergy',
'AtomStateIonizationEnergyUnit' : 'AtomState.ionizationenergyunit.value',
'AtomStateTotalAngMom' : 'AtomState.totalangularmomentum',
'AtomStateTermLabel' : 'AtomState.Component.termlabel',
'AtomStateTermLSL' : 'AtomState.Component.Lscoupling.l',
'AtomStateTermS' : 'AtomState.Component.Lscoupling.s',
'AtomStateTermLSMultiplicity' : 'AtomState.Component.Lscoupling.multiplicity',

                                                                         
'CollisionTabulatedDataX' : 'TabData.xdata',
'CollisionTabulatedDataXUnits' : 'undef',
'CollisionTabulatedDataXN' : 'len(TabData.xdata.split(" "))',
'CollisionTabulatedDataXParameter' : 'undef',
'CollisionTabulatedDataY' : 'TabData.ydata',
'CollisionTabulatedDataYUnits' : 'undef',
'CollisionTabulatedDataYN' : 'len(TabData.ydata.split(" "))',
'CollisionTabulatedDataYParameter' : 'undef',
'CollisionDataSetDescription' : 'DataSet.Description',
'CollisionReactantState' : 'Reactant.state_id()',
'CollisionReactantSpecies' : 'Reactant.species_id()',
'CollisionProductState' : 'Product.state_id()',

'ParticleSpeciesID' : 'Particle.species_id()',
'ParticleName' : 'Particle.name',
'ParticleMass' : 'Particle.mass',
'ParticleMassUnit' : 'Particle.massunit.value',
'ParticleCharge' : 'Particle.charge',
}

# The restrictable dictionary defines limitations to the search. 
# The left-hand side is standardized, the righ-hand size should
# be defined in Django query-language style, where e.g. a search
# for the Species.atomic field  would be written as species__atomic.

RESTRICTABLES = {\
'AtomIonCharge' : 'ioncharge',
'AtomNuclearCharge' : 'nuclearcharge',
'AtomSymbol' : 'elementsymbol',
}

