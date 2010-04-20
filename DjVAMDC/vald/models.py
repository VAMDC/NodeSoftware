from DjVAMDC.node.models import *

## where VALD deviates from the standard node model goes here!

class Transition(models.Model):
    class Meta:
        verbose_name = _('Transition')
        verbose_name_plural = _('Transitions')
    

        vacwave=
        airwave
        species
        loggf
        landeff
        gammarad
        gammastark
        gammawaals
        srctag
        acflag
        accur
        comment
        wave_ref
        loggf_ref
        lande_ref
        gammarad_ref
        gamastark_ref
        gammawaals_ref
        upcoupling
        upterm
        locoupling
        loterm

class State(models.Model):
    class Meta:
        verbose_name = _('State')
        verbose_name_plural = _('States')
    
        species
        energy
        j
        lande
        coupling
        term
        energy_ref
        lande_ref
        level_ref
        idstring
        J
        L
        S
        P
        J1
        J2
        K
        S2
        Jc


class Species(models.Model):
    class Meta:
        verbose_name = _('Species')
        verbose_name_plural = _('Species')
        id
        name
        ion
        mass
        ionen
        solariso
        ncomp
        atomic
        isotope

class Source(models.Model):
    class Meta:
        verbose_name = _('Source')
        verbose_name_plural = _('Sources')
 
        srcfile
        refid
        speclo
        spechi
        blob
        r1
        r2
        r3
        r4
        r5
        r6
        r7
        r8
        r9
        srcdescr
