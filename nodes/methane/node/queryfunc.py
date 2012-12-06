# -*- coding: utf-8 -*-
#
# This module (which must have the name queryfunc.py) is responsible
# for converting incoming queries to a database query understood by
# this particular node's database schema.
#
# This module must contain a function setupResults, taking a sql object
# as its only argument.
#

# library imports

from django.db.models import Q
from vamdctap.sqlparse import *
from dictionaries import *
from models import *
from itertools import chain

import logging
log=logging.getLogger('vamdc.node.queryfu')

LIMIT = 100000

def getRefs(transitions):
    refset = set()
    for t in transitions.values_list('wavenumber_sourceid', 'intensity_sourceid',
                                     'gamma1_sourceid','delta1_sourceid','nexp1_sourceid',
                                     'gamma2_sourceid','delta2_sourceid','nexp2_sourceid',
                                     'gamma3_sourceid','delta3_sourceid','nexp3_sourceid',
                                     'gamma4_sourceid','delta4_sourceid','nexp4_sourceid',
                                     'gamma5_sourceid','delta5_sourceid','nexp5_sourceid',
                                     'gamma6_sourceid','delta6_sourceid','nexp6_sourceid',
                                     'gamma7_sourceid','delta7_sourceid','nexp7_sourceid',
                                     'gamma8_sourceid','delta8_sourceid','nexp8_sourceid',
                                     'gamma9_sourceid','delta9_sourceid','nexp9_sourceid'):
        refset = refset.union(t)

    # Use the found reference keys to extract the correct references from the References table.
    refmatches = Sources.objects.filter(pk__in=refset) # only match primary keys in refset
    return refmatches

def getMethods(transitions):
    mids    = set( transitions.values_list('typeid',flat=True) )
    methods = TransitionTypes.objects.filter(pk__in=mids)
    return methods

def getMolecules(transitions):
    spids     = set( transitions.values_list('isotopeid',flat=True) )
    isotopes  = MoleculesIsotopes.objects.filter(pk__in=spids)
    nisotopes = isotopes.count()
    return isotopes,nisotopes

def getStates(transitions,isotopes,addStates,addBStates):
    nstates = 0

    if addStates:
        for isotope in isotopes:
            # States
            subtransitions = transitions.filter(isotopeid=isotope)
            up             = subtransitions.values_list('upstateid',flat=True)
            lo             = subtransitions.values_list('lowstateid',flat=True)
            eos            = (isotope.eostateid,)
            sids           = set(chain(up,lo,eos))
            isotope.States = MolecularStates.objects.filter(stateid__in = sids)
            if addBStates:
                # BasisStates
                sublevids = set()
                for MS in isotope.States:
                    sublevids = sublevids.union( (MS.sublevid1_id, MS.sublevid2_id, MS.sublevid3_id, MS.sublevid4_id, MS.sublevid5_id,
                                                  MS.sublevid6_id, MS.sublevid7_id, MS.sublevid8_id, MS.sublevid9_id, MS.sublevid10_id,
                                                  MS.sublevid11_id,MS.sublevid12_id,MS.sublevid13_id,MS.sublevid14_id,MS.sublevid15_id,
                                                  MS.sublevid16_id,MS.sublevid17_id,MS.sublevid18_id,MS.sublevid19_id,MS.sublevid20_id,
                                                  MS.sublevid21_id,MS.sublevid22_id,MS.sublevid23_id,MS.sublevid24_id,MS.sublevid25_id,
                                                  MS.sublevid26_id,MS.sublevid27_id,MS.sublevid28_id,MS.sublevid29_id,MS.sublevid30_id,
                                                  MS.sublevid31_id,MS.sublevid32_id,MS.sublevid33_id,MS.sublevid34_id,MS.sublevid35_id,
                                                  MS.sublevid36_id,MS.sublevid37_id,MS.sublevid38_id,MS.sublevid39_id,MS.sublevid40_id,
                                                  MS.sublevid41_id,MS.sublevid42_id,MS.sublevid43_id,MS.sublevid44_id,MS.sublevid45_id,
                                                  MS.sublevid46_id,MS.sublevid47_id,MS.sublevid48_id,MS.sublevid49_id,MS.sublevid50_id,
                                                  MS.sublevid51_id,MS.sublevid52_id,MS.sublevid53_id,MS.sublevid54_id,MS.sublevid55_id,
                                                  MS.sublevid56_id,MS.sublevid57_id,MS.sublevid58_id,MS.sublevid59_id,MS.sublevid60_id)[:MS.nbcoefn0] )
                isotope.BasisStates = VibrationalSublevels.objects.filter(pk__in=sublevids)
            #
            nstates += len(sids)

    return nstates

####################################################################################################

def setupResults(sql):
    """
      This function is always called by the software.
    """
### log.debug('>>>  REQUESTABLES : %s' % sql.requestables)
### log.debug('>>>  QUERY : %s' % sql.request['QUERY'])
### log.debug('>>>  SQL.WHERE : %s'%sql.where)
    q = sql2Q(sql)

    # RadTrans
    transitions  = Transitions.objects.filter(q).order_by('wavenumber')
    ntransitions = transitions.count()

### if 'species' in sql.requestables:
    if sql.request['QUERY'].upper() == 'SELECT SPECIES':
        # LIMIT
        percentage = None
        # Molecules
        isotopes  = MoleculesIsotopes.objects.all()
        nisotopes = isotopes.count()
        # States and BasisStates
        nstates = 0
        # Sources 
        sources  = Sources.objects.all()
        nsources = sources.count()
        # Methods 
        methods = TransitionTypes.objects.all()
###     mids    = (1,2,6)
###     methods = TransitionTypes.objects.filter(pk__in=mids)
    else:
        # LIMIT
        if ntransitions > LIMIT:
            percentage   = '%.1f'%(float(LIMIT)/ntransitions *100)
            limitwave    = transitions[LIMIT].wavenumber
            transitions  = Transitions.objects.filter(q,Q(wavenumber__lt=limitwave))
            ntransitions = transitions.count()
        else:
            percentage = None
        # Molecules
        isotopes,nisotopes = getMolecules(transitions)
        # States and BasisStates
        addStates  = ( not sql.requestables or 'moleculestates' in sql.requestables )
        addBStates = ( not sql.requestables or ('moleculebasisstates' in sql.requestables) or ('moleculequantumnumbers' in sql.requestables) )
        nstates = getStates(transitions,isotopes,addStates,addBStates)
        # Sources
        sources  = getRefs(transitions)
        nsources = sources.count()
        # Methods
        methods = getMethods(transitions)

### log.debug(>>>  'NTRANSITIONS = %s, NISOTOPES = %s' % (ntransitions,nisotopes) )

    # APPROX-SIZE
    if ntransitions:
        size = 0.01
        if( not sql.requestables or 'radiativetransitions' in sql.requestables ):
            size += ntransitions*0.000825
        if( not sql.requestables or 'moleculestates' in sql.requestables ):
            size += nstates*0.000310
        if( not sql.requestables or 'moleculequantumnumbers' in sql.requestables ):
            size += nstates*0.000493
        size_estimate = '%.2f'%(size)
    else:
        size_estimate = '0.01'

######
# thanks to smpo

    funcs = [ Function('gammaL',
                       'gammaL',
                       'Fortran',
                       'gammaL_ref * (296./T)**n',
                       'gammaL',
                       '1/cm/atm',
                       'Temperature-dependence of the Lorentzian component of the pressure broadening coefficient',
                       '',
                       [('T','K', 240, 350, 'The absolute temperature')],
                       [('gammaL_ref', '1/cm/atm', 'The Lorentzian line broadening coefficient, broadened at Tref = 296 K'),
                        ('n','unitless', 'The temperature exponent of the gammaL function')]) ]
             #          ('n','unitless', 'The temperature exponent of the gammaL function')]),
             #Function('delta',
             #         'delta',
             #         'Fortran',
             #         'delta_ref',
             #         'delta',
             #         '1/cm/atm',
             #         'line shift coefficient of the absorption line wave number shift: nu = nu_ref + delta*p',
             #         '',
             #         [['NONE']],
             #         [('delta_ref', '1/cm/atm', 'The pressure-shift coefficient')])]

    envs = [ Environment('refT',
                         'reference temperature',
                         296.0),
             Environment('Broadening-self',
                         'self-broadening reference conditions',
                         296.0,
                         1.0,
                         [('self',1.0)]),
             Environment('Broadening-N2',
                         'N2-broadening reference conditions',
                         296.0,
                         1.0,
                         [('N2',1.0)]),
             Environment('Broadening-O2',
                         'O2-broadening reference conditions',
                         296.0,
                         1.0,
                         [('O2',1.0)]),
             Environment('Broadening-air',
                         'air-broadening reference conditions',
                         296.0,
                         1.0,
                         [('N2',0.79),('O2',0.21)]),
             Environment('Broadening-H2O',
                         'H2O-broadening reference conditions',
                         296.0,
                         1.0,
                         [('H2O',1.0)]),
             Environment('Broadening-CO2',
                         'CO2-broadening reference conditions',
                         296.0,
                         1.0,
                         [('CO2',1.0)]),
             Environment('Broadening-H2',
                         'H2-broadening reference conditions',
                         296.0,
                         1.0,
                         [('H2',1.0)]),
             Environment('Broadening-He',
                         'He-broadening reference conditions',
                         296.0,
                         1.0,
                         [('He',1.0)]),
             Environment('Broadening-Ar',
                         'Ar-broadening reference conditions',
                         296.0,
                         1.0,
                         [('Ar',1.0)]) ]

#
######

    # HEADERINFO
    headerinfo=CaselessDict({\
            'TRUNCATED'       :percentage,
            'COUNT-SOURCES'   :nsources,
            'COUNT-SPECIES'   :nisotopes,
            'COUNT-MOLECULES' :nisotopes,
            'COUNT-STATES'    :nstates,
            'COUNT-RADIATIVE' :ntransitions,
            'APPROX-SIZE'     :size_estimate
            })

    if (ntransitions > 0):
        return {'RadTrans'     :transitions,
                'Molecules'    :isotopes,
                'Sources'      :sources,
                'Methods'      :methods,
                'Functions'    :funcs,
                'Environments' :envs,
                'HeaderInfo'   :headerinfo
               }
    else:
        return {}

