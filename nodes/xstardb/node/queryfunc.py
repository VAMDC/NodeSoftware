# -*- coding: utf-8 -*-
from django.db.models import Q

from models import *

import sys
def LOG(s):
    if settings.DEBUG: print >> sys.stderr, s


from vamdctap.sqlparse import *


def setupResults(sql):
    LOG(sql)
    q=where2q(sql.where,RESTRICTABLES)
    try: q=eval(q)
    except: return {}
    
    ions = Ion.objects.filter(q)
    
    return {#'RadTrans':transs,
            'AtomStates':ions,
            #'Sources':sources,
           }


