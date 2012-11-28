# -*- coding: utf-8 -*-
RETURNABLES = {\
'NodeID':'Tipbase',
                           
'AtomStateID':'AtomState.id',

'AtomSymbol':'Atom.atomicion.isotope.chemicalelement.elementsymbol',
'AtomInchi' : 'Atom.atomicion.inchi',
'AtomInchiKey' : 'Atom.atomicion.inchikey',
'AtomSpeciesID':'Atom.atomicion.id',
'AtomNuclearCharge':'Atom.atomicion.isotope.chemicalelement.nuclearcharge',
'AtomIonCharge':'Atom.atomicion.ioncharge',
'AtomMassNumber':'Atom.atomicion.isotope.massnumber',

'AtomStateRef':'AtomState.Sources',
'AtomStateEnergy':'AtomState.stateenergy',
'AtomStateEnergyUnit':'AtomState.stateenergyunit.value',
'AtomStateParity' : 'AtomState.parity.value',
'AtomStateMixingCoeff':'Component.mixingcoefficient',
'AtomStateMixingCoeffClass' : 'Component.mixingclass.value',
'AtomStateLifeTime': 'AtomState.lifetime',
'AtomStateStatisticalWeight' : 'AtomState.statisticalweight',
'AtomStateStatisticalWeightUnit' : 'AtomState.statisticalweightunit.value',
'AtomStateLifeTimeUnit': 'AtomState.lifetimeunit.value',
'AtomStateLifeTimeDecay':'totalRadiative',
'AtomStateIonizationEnergy' : 'AtomState.ionizationenergy',
'AtomStateIonizationEnergyUnit' : 'AtomState.ionizationenergyunit.value',
'AtomStateTotalAngMom' : 'AtomState.totalangularmomentum',
'AtomStateTermLabel' : 'Component.termlabel',
'AtomStateConfigurationLabel' : 'Component.configuration',
'AtomStateTermLSL' : 'Component.Lscoupling.l',
'AtomStateTermLSS' : 'Component.Lscoupling.s',
'AtomStateTermLSMultiplicity' : 'Component.Lscoupling.multiplicity',

'CollisionTabulatedDataRef' : 'TabData.Sources',
'CollisionTabulatedDataXDataList' : 'TabData.xdata',
'CollisionTabulatedDataXUnits' : 'TabData.xdataunit.value',
'CollisionTabulatedDataXDataListN' : 'len(TabData.xdata.split(" "))',
'CollisionTabulatedDataXParameter' : 'undef',
'CollisionTabulatedDataYDataList' : 'TabData.ydata',
'CollisionTabulatedDataYUnits' : 'TabData.ydataunit.value',
'CollisionTabulatedDataYDataListN' : 'len(TabData.ydata.split(" "))',
'CollisionTabulatedDataYParameter' : 'undef',

'CollisionDataSetDescription' : 'DataSet.dataDescription',
'CollisionReactantState' : 'Reactant.state_id()',
'CollisionReactantSpecies' : 'Reactant.species_id()',
'CollisionProductState' : 'Product.state_id()',
'CollisionID' : 'CollTran.id',

'ParticleSpeciesID' : 'Particle.species_id()',
'ParticleName' : 'Particle.name',
'ParticleMass' : 'Particle.mass',
'ParticleMassUnit' : 'Particle.massunit.value',
'ParticleCharge' : 'Particle.charge',

#source
'SourceTitle':'Source.title',
'SourceAuthorName':'Source.Authors',
'SourceCategory':'Source.sourcecategory.value',
'SourceName' : 'Source.sourcename',
'SourceYear' : 'Source.year',
'SourceURI': 'Source.uri',
'SourceVolume' : 'Source.volume',
'SourcePageBegin' : 'Source.pagebegin',
'SourcePageEnd' : 'Source.pageend',
'SourceDOI' : 'Source.doi',
'SourceID' : 'Source.id',
}

# The restrictable dictionary defines limitations to the search. 
# The left-hand side is standardized, the righ-hand size should
# be defined in Django query-language style, where e.g. a search
# for the Species.atomic field  would be written as species__atomic.

RESTRICTABLES = {\
'IonCharge' : 'ioncharge',
'AtomNuclearCharge' : 'nuclearcharge',
'AtomSymbol' : 'elementsymbol',
}

