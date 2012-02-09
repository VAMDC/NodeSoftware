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

'AtomSymbol':'Atom.atomicion.isotope.chemicalelement.elementsymbol',
'AtomSpeciesID':'Atom.atomicion.id',
'AtomNuclearCharge':'Atom.atomicion.isotope.chemicalelement.nuclearcharge',
'AtomIonCharge':'Atom.atomicion.ioncharge',
'AtomMassNumber':'Atom.atomicion.isotope.massnumber',

'AtomStateEnergy':'AtomState.stateenergy',
'AtomStateEnergyUnit':'AtomState.stateenergyunit.value',
'AtomStateParity' : 'AtomState.parity.value',
'AtomStateMixingCoeff':'Component.mixingcoefficient',
'AtomStateMixingCoeffClass' : 'Component.mixingclass.value',
'AtomStateLifeTime': 'AtomState.lifetime',
'AtomStateLifeTimeDecay':'totalRadiative',
'AtomStateStatisticalWeight' : 'AtomState.statisticalweight',
'AtomStateStatisticalWeightUnit' : 'AtomState.statisticalweightunit.value',
'AtomStateLifeTimeUnit': 'AtomState.lifetimeunit.value',
'AtomStateIonizationEnergy' : 'AtomState.ionizationenergy',
'AtomStateIonizationEnergyUnit' : 'AtomState.ionizationenergyunit.value',
'AtomStateTotalAngMom' : 'AtomState.totalangularmomentum',
'AtomStateTermLabel' : 'Component.termlabel',
'AtomStateTermLSL' : 'Component.Lscoupling.l',
'AtomStateTermLSS' : 'Component.Lscoupling.s',
'AtomStateTermLSMultiplicity' : 'Component.Lscoupling.multiplicity',

'RadTransID':'RadTran.id',
'RadTransWavelength':'RadTran.wavelength',
'RadTransWavelengthUnit':u'A',
'RadTransProbabilityWeightedOscillatorStrength' : 'RadTran.abs_weightedoscillatorstrength()',
'RadTransUpperStateRef':'RadTran.upperatomicstate.id',
'RadTransLowerStateRef':'RadTran.loweratomicstate.id',
'RadTransProbabilityA' : 'RadTran.transitionprobability',
'RadTransProbabilityAUnit' : '1/s',


#'CrossSectionState' : 'RadCros.id',
'CrossSectionID' : 'RadCros.id',
'CrossSectionX' : 'RadCros.xdata',
'CrossSectionXUnit' : 'RadCros.xdataunit.value',
'CrossSectionXN' : 'len(RadCros.xdata.split(" "))',
'CrossSectionY' : 'RadCros.ydata',
'CrossSectionYUnit' : 'RadCros.ydataunit.value',
'CrossSectionYN' : 'len(RadCros.ydata.split(" "))',
}

# The restrictable dictionary defines limitations to the search. 
# The left-hand side is standardized, the righ-hand size should
# be defined in Django query-language style, where e.g. a search
# for the Species.atomic field  would be written as species__atomic.

RESTRICTABLES = {\
'RadTransWavelength':'wavelength',
'AtomIonCharge' : 'ioncharge',
'AtomNuclearCharge' : 'nuclearcharge',
'AtomSymbol' : 'elementsymbol',
}

