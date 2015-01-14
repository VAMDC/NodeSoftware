# -*- coding: utf-8 -*-

from vamdctap.sqlparse import sql2Q
from dictionaries import *

import models

def setupResults(sql):
    q = sql2Q(sql)

    states = models.State.objects.select_related().filter(q)
    species = None

    return {'Atoms':species,
           }
