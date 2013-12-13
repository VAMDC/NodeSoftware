# -*- coding: utf-8 -*-

RETURNABLES = {\
'NodeID':'ExampleNode', # required
'AtomStateID':'AtomState.id',
'AtomSymbol':'Atom.name',
'AtomSpeciesID':'Atom.id',
'AtomStateEnergy':'AtomState.energy',
}

RESTRICTABLES = {\
'AtomSymbol':'species__name',
'AtomStateEnergy':'upstate__energy',
}

