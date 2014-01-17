# -*- coding: utf-8 -*-

from vamdctap.sqlparse import sql2Q
from dictionaries import *

import models

def setupResults(sql):
    q = sql2Q(sql)

    states = models.State.objects.select_related(depth=2).filter(q)
    species = None

    headerinfo = {'COUNT-SOURCES':nsources,
                  'COUNT-SPECIES':nspecies,
                  'COUNT-STATES':nstates,
                  'APPROX-SIZE':states.count()*0.001 }

    return {'Atoms':species,
            'HeaderInfo':headerinfo,
           }
