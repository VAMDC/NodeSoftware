from django.utils.html import strip_tags
from django.utils.encoding import force_unicode
from django.db.models import Q
from vamdctap.sqlparse import *
from dictionaries import *
from models import *
from itertools import chain
from xml.sax.saxutils import escape

import logging
log=logging.getLogger('vamdc.node.queryfu')

if hasattr(settings,'TRANSLIM'):
    TRANSLIM = settings.TRANSLIM
else: TRANSLIM = 5000

def getPartfun(mol, isot):
    pf = PartFun.objects.get(mol_id=mol,mi_id=isot)
    ss = StatSum.objects.filter(mol_id=mol,mi_id=isot).order_by("q_ind")
    pft = []
    pfv = []
    for item in ss:
        pft.append(pf.Tmin + item.q_ind*2)
        pfv.append(pf.Z0*item.value)

    return pft,pfv

def getRefs(src_ids):
    sources = Sources.objects.filter(pk__in=src_ids) 
    for source in sources:
        source.SourceTitle = strip_tags(force_unicode(source.SourceTitle))
        source.SourceURI = escape(str(source.SourceURI))
#        source.SourceURI = '<![CDATA[' + str(source.SourceURI) + ']]>'

    return sources

def getStates(transs):
    Sources = ['Predicted from PES', 'Directly observed at high resolution', 'Dark states deducted from observed resonance perturbations', 'Observed low resolution']
    srefs = set([])
    isots = set([])
    state_ids = set([])
    for trans in transs:
	isots.add((trans.mol_id,trans.mi_id))
	state_ids.add((trans.mol_id,trans.mi_id,trans.vlup,trans.sup))
	state_ids.add((trans.mol_id,trans.mi_id,trans.vllow,trans.slow))
	#    LOG(isots)

    isotopes = []
    nstates = 0
    for isot in isots:
	isotope = Isotopes.objects.get(mol_id=isot[0],mi_id=isot[1])
	isotopes.append(isotope)
        if isotope.ref_mass>0:
            srefs.add(isotope.ref_mass)
        isotope.pft,isotope.pfv = getPartfun(isot[0], isot[1])

	isotope.States = []
	for state_id in state_ids:
	    if state_id[0]==isot[0] and state_id[1]==isot[1]:
		state = VibLevels.objects.get(mol_id=state_id[0], mi_id=state_id[1], vl_num=state_id[2], symm=state_id[3])
                if state.ref_e>0:
                    srefs.add(state.ref_e)
		state.src = Sources[state.src_id]
		state.id = str(state_id[0]) + '-' + str(state_id[1]) + '-' + str(state_id[2]) + '-' + state_id[3]
		isotope.States.append(state)
                nstates = nstates + 1
    nisotopes = len(isotopes)

    return isotopes,nisotopes,nstates,srefs

def setupResults(sql):

    log.debug('sql.where: %s'%sql.where)   
    q = sql2Q(sql)
    
    refs = set([])
    transs = Transitions.objects.filter(q).order_by('wn')
    ntranss = transs.count()

    if ntranss > TRANSLIM:
        percentage = '%.1f'%(float(TRANSLIM)/ntranss *100)
        limitwave = transs[TRANSLIM].wn
        transs = Transitions.objects.filter(q,Q(wn__lt=limitwave))
    else: percentage=None

    log.debug(TRANSLIM)
    ntranss = transs.count()
    for tran in transs:
        if tran.ref_wn>0:
            refs.add(tran.ref_wn)
        if tran.ref_s>0:
            refs.add(tran.ref_s)
        if tran.ref_e>0:
            refs.add(tran.ref_e)

    isotopes,nspecies,nstates,srefs = getStates(transs)
    refs = refs.union(srefs)
    sources = getRefs(refs)
    nsources = sources.count()

    methods = [Method('EXP', 'experiment', 'experiment'),
               Method('THEORY', 'theory', 'theory')]

    funcs = [Function('gammaL', 'gammaL', 'Fortran', 'gammaL_ref * p * (296./T)**n', 'gammL', '1/cm', 'Pressure- and temperature-dependence of the Lorentzian component of the pressure-broadened line width (HWHM)', '', [('T','K', 240, 350),('P','atm',0,2)], [('hwhm','1/cm'),('tc',)])]

    envs = [Environment('PT', 296.0, 1.0),
               Environment('BRDself', 296.0, 1.0, [('self',1.0)]),
               Environment('BRDair', 296.0, 1.0, [('N2',0.79),('O2',0.21)])]

    headerinfo=CaselessDict({'TRUNCATED':percentage,
                'COUNT-SOURCES':nsources,
                'COUNT-SPECIES':nspecies,
                'COUNT-STATES':nstates,
                'COUNT-RADIATIVE':ntranss,
               })

    return {'RadTrans':transs,
            'Molecules':isotopes,
            'Sources':sources,
            'Methods': methods,
            'Functions': funcs,
            'Environments': envs,
            'HeaderInfo':headerinfo
           }