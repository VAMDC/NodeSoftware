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
# returned from queryfunc.py. So in the example below, all 'Sources'
# will be looped over by the node software, using the name 'Source'
# (singular). 'Source' will be one single instance of a matching
# database object, from which we extract everything we need (if you
# look at queryfuncs.py, you'll see 'Sources' being assigned)

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
'AtomStateMixingCoeff':'AtomState.Component.mixingcoefficient',
'AtomStateMixingCoeffClass' : 'AtomState.Component.mixingclass.value',
'AtomStateLifeTime': 'AtomState.lifetime',
'AtomStateLifeTimeDecay':'totalRadiative',
'AtomStateStatisticalWeight' : 'AtomState.statisticalweight',
'AtomStateStatisticalWeightUnit' : 'AtomState.statisticalweightunit.value',
'AtomStateLifeTimeUnit': 'AtomState.lifetimeunit.value',
'AtomStateIonizationEnergy' : 'AtomState.ionizationenergy',
'AtomStateIonizationEnergyUnit' : 'AtomState.ionizationenergyunit.value',
'AtomStateTotalAngMom' : 'AtomState.totalangularmomentum',
'AtomStateTermLabel' : 'AtomState.Component.termlabel',
'AtomStateTermLSL' : 'AtomState.Component.Lscoupling.l',
'AtomStateTermS' : 'AtomState.Component.Lscoupling.s',
'AtomStateTermLSMultiplicity' : 'AtomState.Component.Lscoupling.multiplicity',

'RadTransWavelength':'RadTran.wavelength',
'RadTransWavelengthUnit':u'A',
'RadTransProbabilityWeightedOscillatorStrength' : 'RadTran.weightedoscillatorstrength',

'RadTransFinalStateRef':'RadTran.finalatomicstate.id',
'RadTransInitialStateRef':'RadTran.initialatomicstate.id',
'RadTransProbabilityA' : 'RadTran.transitionprobability',

'CrossSectionState' : 'RadCros.id',
#'CrossSectionID' : 'RadCros.id',
'CrossSectionX' : 'RadCros.xdata',
'CrossSectionXUnits' : 'RadCros.crosssectionunit.value',
'CrossSectionXN' : 'len(RadCros.xdata.split(" "))',
'CrossSectionY' : 'RadCros.ydata',
'CrossSectionYUnits' : 'RadCros.crosssectionunit.value',
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

