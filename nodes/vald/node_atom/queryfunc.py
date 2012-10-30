from ..node_common.queryfunc import *
from models import *

def setupResults(sql):
    q = sql2Q(sql)
    log.debug('Just ran sql2Q(sql); setting up QuerySets now.')
    transs = Transition.objects.filter(q)
    ntranss=transs.count()
    if TRANSLIM < ntranss and (not sql.requestables or 'radiative' in sql.requestables):
        percentage = '%.1f'%(float(TRANSLIM)/ntranss *100)
        newmax = transs[TRANSLIM].wave
        transs = Transition.objects.filter(q,Q(wave__lt=newmax))
        log.debug('Truncated results to %s, i.e %s A.'%(TRANSLIM,newmax))
    else:
        percentage=None
    log.debug('Transitions QuerySet set up. References next.')

    from time import time
    sources = Reference.objects.all()
    ## about 100 times slower than objects.all() objects
    #refIDs = set(tuple(transs.values_list('wavevac_ref_id', flat=True)) +
    #             tuple(transs.values_list('loggf_ref_id', flat=True)) +
    #             tuple(transs.values_list('gammarad_ref_id', flat=True)) +
    #             tuple(transs.values_list('gammastark_ref_id', flat=True)) +
    #             tuple(transs.values_list('waals_ref', flat=True)))
    #sources = Reference.objects.filter(pk__in=refIDs)

    log.debug('Sources QuerySet set up. References next.')
    addStates = (not sql.requestables or 'atomstates' in sql.requestables)
    atoms,nspecies,nstates = getSpeciesWithStates(transs,Species,State,addStates)

    if ntranss:
        size_estimate='%.2f'%(ntranss*0.0014 + 0.01)
    else:
        size_estimate='0.00'

    headerinfo={\
            'TRUNCATED':percentage,
            'COUNT-ATOMS':nspecies,
            'COUNT-SPECIES':nspecies,
            'COUNT-STATES':nstates,
            'COUNT-RADIATIVE':ntranss,
            'APPROX-SIZE':size_estimate,
            }
    log.debug('Returning from setupResults()')
    return {'RadTrans':transs,
            'Atoms':atoms,
            'Sources':sources,
            'HeaderInfo':headerinfo,
            'Environments':Environments, #set up statically in node_common.models
            'Methods':getMethods(),      #defined in node_common.queryfuncs
            'Functions':Functions        #set up statically in node_common.models
           }
