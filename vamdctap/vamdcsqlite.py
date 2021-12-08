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


'''
Generates an SQLite database on the given file-path.
The super-set of tables is hard-coded in this method,
but the set of those actually written is determined by the
node's dictionaries. The columns for each table are also specified 
by the node's dictionaries. The data for the tables comes from 
other arguments of this function, which are Django QuerySets.
'''
def generate_sqlite(file_path, tap, HeaderInfo=None, Sources=None, Methods=None, Functions=None,
          Environments=None, Atoms=None, Molecules=None, Solids=None, Particles=None,
          CollTrans=None, RadTrans=None, RadCross=None, NonRadTrans=None):
          
    conn = None
              
    try:
        log.debug('Connecting SQLite to %s...'%file_path)
        conn = sqlite3.connect(file_path)
        log.debug('...connected')

        if Atoms and hasattr(DICTS, 'ATOMS_COLUMNS'):
            write_plain_table(conn, 'Atoms', DICTS.ATOMS_COLUMNS, Atoms)

        if Atoms and hasattr(DICTS, 'ATOMSTATES_COLUMNS'):
            write_states_table(conn, 'Atomstates', DICTS.ATOMSTATES_COLUMNS, Atoms)
            
        if Molecules and hasattr(DICTS, 'MOLECULES_COLUMNS'):
            write_plain_table(conn, 'Molecules', DICTS.MOLECULES_COLUMNS, Molecules)
            
        if Molecules and hasattr(DICTS, 'MOLECULESTATES_COLUMNS'):
            write_states_table(conn, 'Moleculestates', DICTS.MOLECULESTATES_COLUMNS, Molecules)
            
        if RadTrans and hasattr(DICTS, 'RADTRANS_COLUMNS'):
            write_plain_table(conn, 'Radtrans', DICTS.RADTRANS_COLUMNS, RadTrans)
            
        if Particles and hasattr(DICTS, 'PARTICLES_COLUMNS'):
            write_plain_table(conn, 'Particles', DICTS.PARTICLES_COLUMNS, Particles)
            
        if Sources and hasattr(DICTS, 'SOURCES_COLUMNS'):
            write_plain_table(conn, 'Sources', DICTS.SOURCES_COLUMNS, Sources)
        
    finally:
        if conn:
            conn.close()
            
'''
Creates and writes an SQLite table directly from the given data-source.
The data-source must be a Django QuerySet.
'''
def write_plain_table(conn, table_name, columns, data_source):
    create_table(conn, table_name, columns)
    write_rows(conn, table_name, columns, data_source)
    conn.commit()
    
    
'''
Creates and writes an SQLite table from the Django QuerySets nested
as the .states attributes of the objects found by iterating
over the given data-source.
'''
def write_states_table(conn, table_name, columns, data_source):
    create_table(conn, table_name, columns)
    for q in data_source:
        if hasattr(q, 'States'):
            write_rows(conn, table_name, columns, q.States)
            conn.commit()
    conn.commit()
    

'''
Creates an SQLite table based on the column names and types given
to the columns parameter.
'''
def create_table(conn, table_name, columns):
    
    cursor = conn.cursor()
 
    create_columns = []
    for k in columns:
        create_columns.append('%s %s'%(k, columns[k][0]))
        
    create_sql = 'CREATE TABLE %s(%s)'%(table_name, ', '.join(create_columns))
    cursor.execute(create_sql)
    

'''
Writes rows to an SQLite table, transcribing from the Django QuerySet
provided to the data_source parameter. The columns parameter specifies
how to get the column values out of the QuerySet. This function may be 
called multiple times for each table and appends rows to any that were 
previously written,
'''
def write_rows(conn, table_name, columns, data_source):
    
    cursor = conn.cursor()

    placeholders = []
    for k in columns:
        placeholders.append('?')
    insert_sql = 'INSERT INTO %s VALUES(%s)'%(table_name, ','.join(placeholders))
    
    # Process each row in turn. Count the rows, and flush to file every 1000.
    # The data_source is a Django QuerySet and each row is a Model object.
    n = 0
    for row in data_source:
        n += 1
        
        # For each column the list of column details states a Python
        # fragment, to be evaluated as an attribute of the Model object representing
        # the row as raised by Django. Column_magic is an array of these evaluations
        # and is used as the argument array for the insertion into SQLite. Note that
        # the local variable called row is used in the evaluation, despite showing
        # up as unused in static analysis. 
        column_magic = []
        for k in columns:
            q = 'row.' + columns[k][1]
            column_magic.append(eval(q))
        cursor.execute(insert_sql, column_magic)
        if n % 1000 == 0:
            conn.commit()


