#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
import.py

Very modest beginning of the import tool that will
take data from ascii-tables and fill them into the 
relational database.

The idea is to have a config file/dictionary that contains the
necessary information on both how to parse the ascii files and on how
to layout the table structure. This dictionary can have global
keywords valid for the whole data set. The keyword "tables" then
contains a list of dictionaries with the source-file-specific
information.

Quite a bit of thought will be needed on how to descibe the splitting
into several tables, indices etc.

"""

from os.path import join,exists
from os import remove
import string as s
from sys import argv

### FUCTIONS TO APPLY TO DATA AFTER READING
def fixvald(data):
    return data

def fixrefs(data):
    return data

def fixnothing(data):
    return data

### CONFIG "FILES"
dummycfg = {\
    'tables':[\
        {'fname':'dummy.dat',
         'delim':' ',
         'tname':'dummy1',
         'headlines':0,
         'commentchar':'',
         'function':fixnothing,
         'columns':[\
                {'cname':'c1',
                 'cfmt':'%d',
                 'ccom':'column 1',
                 'cunit':None,
                 'cbyte':0,
                 'cnull':None,
                 'ctype':'UNSIGNED INT',
                 },
                {'cname':'c2',
                 'cfmt':'%.2f',
                 'ccom':'column 2',
                 'cunit':'Å',
                 'cbyte':1,
                 'cnull':0.0,
                 'ctype':'FLOAT',
                 },
                ]
         },
        {'fname':'dummy.dat',
         'delim':' ',
         'tname':'dummy2',
         'headlines':0,
         'commentchar':'',
         'function':fixnothing,
         'columns':[\
                {'cname':'c1',
                 'cfmt':'%d',
                 'ccom':'column 1',
                 'cunit':None,
                 'cbyte':0,
                 'cnull':None,
                 'ctype':'UNSIGNED INT',
                 },
                {'cname':'c2',
                 'cfmt':'%.2f',
                 'ccom':'column 2',
                 'cunit':'eV',
                 'cbyte':2,
                 'cnull':0.0,
                 'ctype':'UNSIGNED FLOAT',
                 },
                ],
         'relations':[{\
                'table1':'dummy1',
                'column1':'c1',
                'table2':'dummy2',
                'column2':'c1'
                }]
      
         }
        ]
    }

valdcfg={\
    'tables':[\
        {'tname':'merged',
         'fname':'merged.dat',
         'delim':'fixedcol', # delimiter character or 'fixedcol'
         'headlines':2,      # this many lies ignored in file header
         'commentchar':'',   # lines that start with this are ignored
         'function':fixvald,  # to be applied on each line
         'columns':[\
                {'cname':'wavel',     # column name
                 'cfmt':'%.5f',       # print format
                 'ccom':'Wavelength', # description
                 'cunit':'Å',         # Units
                 'cbit':(0,13),       # place in the line
                 'cnull':None,        # value to be converted to NULL
                 'ctype':'UNSIGNED FLOAT', # data format in database
                 },
                {'cname':'atomic',
                 'cfmt':'%d',
                 'ccom':'Atomic number',
                 'cunit':None,
                 'cbit':(13,16),
                 'cnull':None,
                 'ctype':'UNSIGNED TINYINT'},
                {'cname':'ion',
                 'cfmt':'%d',
                 'ccom':'Ionization stage, 0 is neutral',
                 'cunit':None,
                 'cbit':(17,19),
                 'cnull':None,
                 'ctype':'UNSIGNED TINYINT'},
                {'cname':'loggf',
                 'cfmt':'%.3f',
                 'ccom':'oscillator strength, log g*f',
                 'cunit':None,
                 'cbit':(19,27),
                 'cnull':None,
                 'ctype':'FLOAT'},
                {'cname':'lowev',
                 'cfmt':'%.3f',
                 'ccom':'excitation energy of the lower level',
                 'cunit':'eV',
                 'cbit':(27,35),
                 'cnull':None,
                 'ctype':'UNSIGNED FLOAT'},
                {'cname':'lowj',
                 'cfmt':'%.2f',
                 'ccom':'quantum number J of the lower level',
                 'cunit':None,
                 'cbit':(35,40),
                 'cnull':None,
                 'ctype':'UNSIGNED FLOAT'},
                {'cname':'hiev',
                 'cfmt':'%.3f',
                 'ccom':'excitation energy of the upper level',
                 'cunit':'eV',
                 'cbit':(40,48),
                 'cnull':None,
                 'ctype':'UNSIGNED FLOAT'},
                {'cname':'hij',
                 'ccom':'quantum number J of the upper level',
                 'cfmt':'%.2f',
                 'cunit':None,
                 'cbit':(48,53),
                 'cnull':None,
                 'ctype':'UNSIGNED FLOAT'},
                {'cname':'landup',
                 'cfmt':'%.2f',
                 'cunit':None,
                 'cbit':(53,59),
                 'cnull':None,
                 'ctype':'FLOAT'},
                {'cname':'landlo',
                 'cfmt':'%.2f',
                 'cunit':None,
                 'cbit':(59,65),
                 'cnull':None,
                 'ctype':'FLOAT'},
                {'cname':'',
                 'cfmt':'%.2f',
                 'ccom':'',
                 'cunit':None,
                 'cbit':(0,12),
                 'cnull':None,
                 'ctype':'FLOAT'},
                ]
         },
        {'tname':'refs',
         'fname':'',
         'delim':',',
         'headlines':1,
         'commentchar':';',
         'function':fixrefs,
         'columns':[\
                {'cname':'',
                 'cfmt':'%.2f',
                 'ccom':'',
                 'cunit':None,
                 'cbit':(0,12),
                 'cnull':None,
                 'ctype':'FLOAT'},
                ]
         },
        ],
    'relations':[ # descibe which table.column is related to another
        {'table1':'',
         'column1':'',
         'table2':'',
         'column2':'',
         }
        ]
    }


#### WORKER FUNCTIONS; I.E. THE "IMPORT TOOLS"

def readcfg(fname):
    """
       Read the config dictionary.
       Note: very unsafe, since the content gets executed.
       Have a look at createcfg() to see how it should look like.
    """
    f=open(fname)
    #exec(s.join(f.readlines()))
    exec(f.read())
    return config
    
def createtable(curs,tconf):
    """
       create the tables with typed columns, according to the config-dict
    """
    sql='CREATE TABLE IF NOT EXISTS %s ('%tconf['tname']
    for col in tconf['columns']:
        sql+='%s %s, '%(col['cname'],col['ctype'])
    sql=sql[:-2]
    sql+=');' 
    curs.execute(sql)

def createmeta(curs):
    """
        creates the meta table
    """
    sql='CREATE TABLE IF NOT EXISTS meta ('
    sql+='cname VARCHAR(64),'
    sql+='tname VARCHAR(64),'
    sql+='ccom TEXT,'
    sql+='cunit VARCHAR(64),'
    sql+='cfmt VARCHAR(64)'
    sql+=' );'
    
    curs.execute(sql)

def fillmeta(curs,conf):
    """
        fills the meta table according to the config
    """
    for table in conf['tables']:
        tname=table['tname']
        for col in table['columns']:
            sql='INSERT INTO meta VALUES (?, ?, ?, ?, ?);'
            d=[col['cname'],tname,col['ccom'],col['cunit'],col['cfmt']]
            
            print sql,d
            curs.execute(sql,d)

def createindices(curs,conf):
    pass
        
    

def splitfixedcol(line,cols,delim):
    data=[]
    for col in cols:
        start=col['cbyte'][0]
        ned=col['cbyte'][1]
        data.append(s.strip(line[start:end]))
    return data

def splitbydelim(line,cols,delim):
    data=[]
    for col in cols:
        print col
        d=line.split(delim)[col['cbyte']] 
        data.append(s.strip(d))
    return data
    
def filldata(curs,tconf):
    """
        read the data-files and fill the data into the tables in the DB
    """
    f=open(tconf['fname'])
    for i in range(tconf['headlines']):
        f.readline()

    delim=tconf['delim']
    if delim=='fixedcol': 
        splitter=splitfixedcol
    else:
        splitter=splitbydelim

    for line in f:
        data=splitter(line,tconf['columns'],delim)
        data=tconf['function'](data)
        sql='INSERT INTO %s '%(tconf['tname'])
        sql+=' VALUES (%s)'%s.join(('?')*len(data),', ')
        curs.execute(sql,tuple(data))
        

def connect_sqlite(dbname):
    """
       connect to the database file and return cursor and connection handle
    """
    from sqlite3 import dbapi2 as sqlite
    conn=sqlite.connect(dbname)
    return conn,conn.cursor()
    
def connect_mysql(host='localhost',user='vald',passwd='V@ld',db='vald'):
    import MySQLdb
    conn = MySQLdb.connect (host=host,user=user,passwd=passwd,db=db)
    return conn,conn.cursor()
    


def writedummydata(n=100,filename='dummy.dat'):
    """
        write random dummy data
    """
    from random import random
    f=open(filename,'w')
    while n>0:
        n-=1
        f.write('%d %f %f\n'%(100-n,random(),random()))
    f.close()

def main():
    if len(argv) < 2:
        print "usage: ./import.py name.cfg\nOr ./import.py dummy"
        return

    if argv[1]=='dummy':
        try: remove('dummy.db')
        except: pass
        conn,curs=connect_sqlite('dummy.db')
        config=dummycfg
        writedummydata()
    elif argv[1]=='vald':
         conn,curs=connect_mysql()
         config=readcfg('merged.cfg')
    else:
        dbname=s.replace(argv[1],'.cfg','')+'.db'
        conn,curs=connect_sqlite(dbname)
        config=readcfg(argv[1])

    createmeta(curs)
    fillmeta(curs,config)

    for tconf in config['tables']:
        createtable(curs,tconf)
        filldata(curs,tconf)

    conn.commit() # IMPORTANT! This actually writes the database.
                  # Before everything's only in memory.
    conn.close()

if __name__ == '__main__':
    main()
