#!/usr/bin/env python

import pyxb
pyxb.RequireValidWhenGenerating(False)
B=pyxb.BIND

import XsamsPyxb as XSAMS

trans=XSAMS.RadiativeTransitionType()
trans.methodRef='MOBS'
trans.Comments='Ho ho ho!'
trans.EnergyWavelength=B()
trans.EnergyWavelength.Wavelength=B()
trans.EnergyWavelength.Wavelength.Experimental=B(sourceRef='RefX')
trans.EnergyWavelength.Wavelength.Experimental.Value=B('5.6')
rad=XSAMS.Radiative()
rad.RadiativeTransition.append(trans)

print rad.toxml(root_only=True)
