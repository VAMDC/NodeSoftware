# -*- coding: utf-8 -*-
import os
import logging
import threading

# These are needed to get the node settings.
from django.conf import settings
from importlib import import_module

from django.utils import timezone

from vamdctap.vamdcsqlite import generateSqlite
from vamdctap.models import Job


log=logging.getLogger('vamdc.tap')

QUERYFUNC = import_module(settings.NODEPKG+'.queryfunc')
DICTS = import_module(settings.NODEPKG+'.dictionaries')



    
'''
Runs one query. Requires keyword arguments tap, a TAPQUERY instance,
id, a UUID for the job, and directory, the absolute path to a cache
directory in which the resutls of the query will be stored.
'''       
def asyncTapQuery(*args, **kwargs):
    (id, tap, directory) = args
    j = Job.objects.filter(id=id)[0]
    j.phase='ACTIVE'
    j.save()
    
    filePath = directory + os.path.sep + j.file
        
    try: 
        querysets = QUERYFUNC.setupResults(tap)
    except Exception as err:
        emsg = 'Query processing in setupResults() failed: %s'%err
        log.debug(emsg)
        j.phase='failed'
        j.save()
        return

    if not querysets:
        log.info('setupResults() gave something empty.')
        j.phase = 'failed'
        j.save()
        return 
        
    
        
    # Run the query and put the results into the file.
    log.debug('Copying to SQLite at %s ...'%filePath)
    generateSqlite(filePath, tap, **querysets)
    log.debug('...done.')
    j.phase = 'finished'
    j.save()


def purgeJobs():
    for j in Job.objects.all():
        if timezone.now() > j.expiry:
            j.delete()
            
            
