# -*- coding: utf-8 -*-

RETURNABLES = {\
'NodeID':'Topbase',

#'SourceID':'Source.id',
#'SourceAuthorName':'Source.author',
#'SourceCategory':'Source.category',
#'SourcePageBegin':'Source.pages',
#'SourcePageEnd':'Source.pages',
#'SourceName':'Source.journal',
#'SourceTitle':'Source.title',
#'SourceURI':'Source.url',
#'SourceVolume':'Source.volume',
#'SourceYear':'Source.year',                                                              

#'MethodID':'Method.id',
#'MethodCategory':'Method.category',
                           
'AtomStateID':'AtomState.id',
'AtomInchi' : 'Atom.atomicion.inchi',
'AtomInchiKey' : 'Atom.atomicion.inchikey',
'AtomSymbol':'Atom.atomicion.isotope.chemicalelement.elementsymbol',
'AtomSpeciesID':'Atom.atomicion.id',
'AtomNuclearCharge':'Atom.atomicion.isotope.chemicalelement.nuclearcharge',
'AtomIonCharge':'Atom.atomicion.ioncharge',
'AtomMassNumber':'Atom.atomicion.isotope.massnumber',

'AtomStateEnergy':'AtomState.stateenergy',
'AtomStateRef':'AtomState.Sources',
'AtomStateEnergyUnit':'AtomState.stateenergyunit',
'AtomStateParity' : 'AtomState.parity.value',
'AtomStateMixingCoeff':'Component.mixingcoefficient',
'AtomStateMixingCoeffClass' : 'Component.mixingclass.value',
'AtomStateLifeTime': 'AtomState.lifetime',
'AtomStateLifeTimeDecay':'totalRadiative',
'AtomStateStatisticalWeight' : 'AtomState.statisticalweight',
'AtomStateStatisticalWeightUnit' : 'AtomState.statisticalweightunit',
'AtomStateLifeTimeUnit': 'AtomState.lifetimeunit',
'AtomStateIonizationEnergy' : 'AtomState.ionizationenergy',
'AtomStateIonizationEnergyUnit' : 'AtomState.ionizationenergyunit',
'AtomStateTotalAngMom' : 'AtomState.totalangularmomentum',
'AtomStateTermLabel' : 'Component.termlabel',
'AtomStateConfigurationLabel' : 'Component.configuration',
'AtomStateTermLSL' : 'Component.Lscoupling.l',
'AtomStateTermLSS' : 'Component.Lscoupling.s',
'AtomStateTermLSMultiplicity' : 'Component.Lscoupling.multiplicity',

'RadTransID':'RadTran.id',
'RadTransRefs' : 'RadTran.Sources',
'RadTransWavelength':'RadTran.wavelength',
'RadTransWavelengthUnit':'RadTran.wavelengthunit',
'RadTransProbabilityWeightedOscillatorStrength' : 'RadTran.abs_weightedoscillatorstrength()',
'RadTransUpperStateRef':'RadTran.upperatomicstate.id',
'RadTransLowerStateRef':'RadTran.loweratomicstate.id',
'RadTransSpeciesRef' : 'RadTran.version.atomicion.id', 
'RadTransProbabilityA' : 'RadTran.transitionprobability',
'RadTransProbabilityAUnit' : '1/s',


'CrossSectionState' : 'RadCros.id',
'CrossSectionID' : 'RadCros.id',
'CrossSectionX' : 'RadCros.xdata',
'CrossSectionXUnit' : 'RadCros.xdataunit',
'CrossSectionXN' : 'len(RadCros.xdata.split(" "))',
'CrossSectionY' : 'RadCros.ydata',
'CrossSectionYUnit' : 'RadCros.ydataunit',
'CrossSectionYN' : 'len(RadCros.ydata.split(" "))',

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
'RadTransWavelength':'wavelength',
'IonCharge' : 'ioncharge',
'AtomNuclearCharge' : 'nuclearcharge',
'AtomSymbol' : 'elementsymbol',
'InchiKey' : 'inchikey',
}

