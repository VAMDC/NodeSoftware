# -*- coding: utf-8 -*-
import datetime
import os
import time

import logging
log=logging.getLogger('vamdc.tap')

import sqlite3

# These are needed to get the node settings.
from django.conf import settings
from importlib import import_module


import threading

from vamdctap.vamdcsqlite import generateSqlite



QUERYFUNC = import_module(settings.NODEPKG+'.queryfunc')
DICTS = import_module(settings.NODEPKG+'.dictionaries')


def getDetailsAllJobs():
    db = settings.RESULTS_CACHE_DIR + os.path.sep + 'jobs.db'
    conn = sqlite3.connect(db)
    c = conn.cursor()
    sql = 'SELECT id, state, query, expiry FROM jobs'
    c.execute(sql)
    rows = c.fetchall()
    conn.close()
    return rows

def logNewJob(id, query, expiry):
    log.debug('Query: %s'%query)
    db = settings.RESULTS_CACHE_DIR + os.path.sep + 'jobs.db'
    conn = sqlite3.connect(db)
    c = conn.cursor()
    sql = 'INSERT INTO jobs(id, state, query, expiry) VALUES(?, ?, ?, ?)'
    c.execute(sql, (str(id), 'active', query, str(expiry)))
    conn.commit()
    conn.close()
    
def logFinishedJob(id):
    db = settings.RESULTS_CACHE_DIR + os.path.sep + 'jobs.db'
    conn = sqlite3.connect(db)
    c = conn.cursor()
    sql = "UPDATE jobs SET state='finished' WHERE id=?"
    c.execute(sql, (str(id),))
    conn.commit()
    conn.close()
    
def forgetJob(id):
    db = settings.RESULTS_CACHE_DIR + os.path.sep + 'jobs.db'
    conn = sqlite3.connect(db)
    c = conn.cursor()
    sql = 'DELETE FROM jobs WHERE id=?'
    c.execute(sql, (str(id),))
    conn.commit()
    conn.close()
    fileName = settings.RESULTS_CACHE_DIR + os.path.sep + str(id) + '.sqlite3'
    os.remove(fileName)
    
def getJobState(id):
    db = settings.RESULTS_CACHE_DIR + os.path.sep + 'jobs.db'
    conn = sqlite3.connect(db)
    c = conn.cursor()
    sql = 'SELECT state, query, expiry FROM jobs WHERE id=?'
    c.execute(sql, (str(id),))
    row = c.fetchone()
    if row:
        state = row[0]
        query = row[1]
        expiry = row[2]
    else:
        state = None
        query = None
        expiry = None
    conn.close()
    return (state, query, expiry)
    



'''
Runs one query. Requires keyword arguments tap, a TAPQUERY instance,
id, a UUID for the job, and directory, the absolute path to a cache
directory in which the resutls of the query will be stored.
'''       
def asyncTapQuery(*args, **kwargs):
    (id, tap, directory) = args
    
    log.debug('%s: Running %s'%(threading.currentThread(), str(id)))
    expiry = datetime.datetime.now()
    expiry += datetime.timedelta(days=1)
    logNewJob(id, tap.query, str(expiry))
        
    try: 
        querysets = QUERYFUNC.setupResults(tap)
    except Exception as err:
        emsg = 'Query processing in setupResults() failed: %s'%err
        log.debug(emsg)
        return

    if not querysets:
        log.info('setupResults() gave something empty.')
        return 
        
    # Form a unique file-name for the results.
    filePath = directory + os.path.sep + str(id) + '.sqlite3'
        
    # Run the query and put the results into the file.
    log.debug('Copying to SQLite at %s ...'%filePath)
    generateSqlite(filePath, tap, **querysets)
    log.debug('...done.')
    logFinishedJob(id)


