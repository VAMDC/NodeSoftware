from django.db.models import Q
from vamdctap.sqlparse import *
from dictionaries import *
from models import *

LIMIT = 10000

def setupResults(sql):
    q = eval( where2q(sql.where,RESTRICTABLES) )
    transs = Transition.objects.filter(q).order_by('wavelength')
    ntranss = transs.count()

    if ntranss > LIMIT:
        percentage = '%.1f'%(float(LIMIT)/ntranss *100)
        limitwave = transs[LIMIT].wavelength
        transs = Transition.objects.filter(q,Q(vacwave__lt=limitwave))
    else: percentage=None

    spids = set( transs.values_list('species_id',flat=True) )
    species = Species.objects.filter(id__in=spids)
    nspecies = species.count()
    nstates = 0
    for specie in species:
        subtranss = transs.filter(species=specie)
        up=subtranss.values_list('upper_state_id',flat=True)
        lo=subtranss.values_list('lower_state_id',flat=True)
        sids = set(up+lo)
        specie.States = State.objects.filter(id__in = sids)
        nstates += len(sids)

    headerinfo={'TRUNCATED':percentage,
                'COUNT-SPECIES':nspecies,
                'COUNT-STATES':nstates,
                'COUNT-RADIATIVE':ntranss
               }


    return {'RadTrans':transs,
            'Atoms':species,
            'HeaderInfo':headerinfo
           }

