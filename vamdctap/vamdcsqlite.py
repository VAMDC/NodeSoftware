# -*- coding: utf-8 -*-

import uuid
import os

import logging
log=logging.getLogger('vamdc.tap')

import sqlite3

# This is rubbish way to get at this information. Refactor!
from importlib import import_module
from django.conf import settings
DICTS = import_module(settings.NODEPKG+'.dictionaries')


from django.db.models.query import QuerySet


        
def generateSqlite(filePath, tap, HeaderInfo=None, Sources=None, Methods=None, Functions=None,
          Environments=None, Atoms=None, Molecules=None, Solids=None, Particles=None,
          CollTrans=None, RadTrans=None, RadCross=None, NonRadTrans=None):
          
    conn = None
    
              
    try:
        log.debug('Connecting SQLite to %s...'%filePath)
        conn = sqlite3.connect(filePath)
        log.debug('...connected')
        c = conn.cursor()

        if Atoms and DICTS.ATOMS_COLUMNS:
            create_table(conn, 'Atoms', DICTS.ATOMS_COLUMNS)
            write_rows(conn, 'Atoms', DICTS.ATOMS_COLUMNS, Atoms)
            conn.commit()

        if Atoms:
            create_table(conn, 'Atomstates', DICTS.ATOMSTATES_COLUMNS)
            for a in Atoms:
                if hasattr(a, 'States'):
                    write_rows(conn, 'Atomstates', DICTS.ATOMSTATES_COLUMNS, a.States)
            conn.commit()
            
        if RadTrans and DICTS.RADTRANS_COLUMNS:
            create_table(conn, 'Radtrans', DICTS.RADTRANS_COLUMNS)
            n = 0
            write_rows(conn, 'Radtrans', DICTS.RADTRANS_COLUMNS, RadTrans)
            conn.commit()
        
    finally:
        if conn:
            conn.close()
            

def create_table(conn, table_name, columns):
    log.debug(table_name)
    log.debug(columns)
    
    cursor = conn.cursor()
 
    create_columns = []
    for k in columns:
        create_columns.append('%s %s'%(k, columns[k][0]))
        
    create_sql = 'CREATE TABLE %s(%s)'%(table_name, ', '.join(create_columns))
    log.debug(create_sql)
    cursor.execute(create_sql)
    
    
def write_rows(conn, table_name, columns, data_source):
    #log.debug(table_name)
    #log.debug(columns)
    
    cursor = conn.cursor()

    placeholders = []
    for k in columns:
        placeholders.append('?')
    insert_sql = 'INSERT INTO %s VALUES(%s)'%(table_name, ','.join(placeholders))
    #log.debug(insert_sql)
    
    n = 0
    for row in data_source:
        n += 1
        column_magic = []
        for k in columns:
            q = 'row.' + columns[k][1]
            #log.debug(q);
            column_magic.append(eval(q))
        #log.debug(column_magic)
        cursor.execute(insert_sql, column_magic)
        if n % 1000 == 0:
            conn.commit()


