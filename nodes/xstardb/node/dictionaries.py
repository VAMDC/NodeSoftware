# -*- coding: utf-8 -*-

RESTRICTABLES = {\
'AtomIonCharge' : 'charge',
'AtomSymbol' : 'element__sym',
'AtomNuclearCharge' : 'element__z',
#'AtomStateEnergy' : 'Levels.energy'
}

RETURNABLES = {\
'AtomIonCharge' : 'AtomState.charge',
'AtomNuclearCharge' : 'AtomState.element.z',
'AtomSymbol' : 'AtomState.element.sym',
'AtomMassNumber' : 'AtomState.element.mass',
#'AtomStateEnergy' : 'Levels.energy',
#'AtomStateDescription' : 'Levels.label'
}
