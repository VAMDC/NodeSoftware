from ..node_common.queryfunc import *
from models import *

def setupResults(sql):
    q = sql2Q(sql)
    log.debug('Just ran sql2Q(sql); setting up QuerySets now.')
    transs = Transition.objects.filter(q)
    ntranss=transs.count()
    if TRANSLIM < ntranss and (not sql.requestables or 'radiative' in sql.requestables):
        percentage = '%.1f'%(float(TRANSLIM)/ntranss *100)
        #transs = transs.order_by('wave')
        newmax = transs[TRANSLIM].wave
        transs = Transition.objects.filter(q,Q(wave__lt=newmax))
        log.debug('Truncated results to %s, i.e %s A.'%(TRANSLIM,newmax))
    else: percentage=None
    log.debug('Transitions QuerySet set up. References next.')
    #refIDs = set( transs.values_list('wave_ref_id','loggf_ref_id','gammarad_ref_id','gammastark_ref_id','waals_ref') )
    #sources = Reference.objects.filter(pk__in=refIDs)
    sources = Reference.objects.all()
    log.debug('Sources QuerySet set up. References next.')

    addStates = (not sql.requestables or 'atomstates' in sql.requestables)
    atoms,nspecies,nstates = getSpeciesWithStates(transs,Species,State,addStates)

    methods = getMethods()

    if ntranss:
        size_estimate='%.2f'%(ntranss*0.0014 + 0.01)
    else: size_estimate='0.00'

    headerinfo={\
            'TRUNCATED':percentage,
            'COUNT-ATOMS':atoms.count(),
            'COUNT-MOLECULES':molecules.count(),
            'COUNT-SPECIES':atoms.count() + molecules.count(),
            'COUNT-STATES':nstates,
            'CoUNT-RADIATIVE':ntranss,
            'APPROX-SIZE':size_estimate,
            }

    log.debug('Returning from setupResults()')
    return {'RadTrans':transs,
            'Atoms':atoms,
            'Molecules':molecules,
            'Sources':sources,
            'HeaderInfo':headerinfo,
            'Environments':Environments, #this is set up statically in models.py
            'Methods':methods
           }
