#!/usr/bin/env python

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

     52.68200
"""

from os.path import join,exists
from os import remove
import string as s
from sys import argv

valdcfg={\
    'tables':[\
        {'tname':'merged',
         'fname':'merged.dat',
         'delim':'fixedcol',
         'headlines':2,
         'columns':[\
                ('l','%.3f',0,12,'FLOAT'),
                ('l','%.3f',0,12,'FLOAT'),
                ('l','%.3f',0,12,'FLOAT'),
                ('l','%.3f',0,12,'FLOAT'),
                ('l','%.3f',0,12,'FLOAT'),
    }

def readcfg(fname):
    """
       Read the config dictionary.
       Note: very unsafe, since the content gets executed.
       Have a look at createcfg() to see how it should look like.
    """
    f=open(fname)
    exec(s.join(f.readlines()))
    
    return config
    
def createtable(curs,tconf):
    """
       create the tables with typed columns, according to the config-dict
    """
    sql='CREATE TABLE IF NOT EXISTS %s '%tconf['tname']
    sql+='(id INTEGER PRIMARY KEY, '
    for i,colname in enumerate(tconf['colnames']):
        sql+='%s %s, '%(colname,tconf['coltypes'][i])
    sql=sql[:-2]
    sql+=');' 
    curs.execute(sql)

def filldata(curs,tconf):
    """
        read the data-files and fill the data into the tables in the DB
    """
    delim=tconf['delim']
    f=open(tconf['fname'])
    for i in range(tconf['headlines']):
        f.readline()
    for line in f:
        l=line.split()
        if len(l) != len(tconf['colnames']):
            print 'skipped line'
            continue
        sql='INSERT INTO %s '%(tconf['tname'])
        curs.execute(sql+' VALUES (NULL, %s)'%s.join(('?')*len(l),', '),tuple(l))
        

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
    

def dummycfg():
    """
        return code to create a config-dictionary that matches the
        dummy data below.
    """
    return """config = { \
	'tables':[\
	       {'fname':'dummy.dat',\
		'delim':' ',\
		'tname':'dummy1',\
		'headlines':0,\
		'ncols':3,\
		'colnames':['c1', 'c2', 'c3'],\
		'coltypes':['REAL', 'REAL', 'TEXT'],\
		}\
	]
}

"""

def writedummydata(n=100):
    """
        write random dummy data into dummy.dat
    """
    from random import random,choice
    f=open('dummy.dat','w')
    while n>0:
        f.write('%f %f %s\n'%(random(),random(),choice(s.letters)))
        n-=1
    f.close()

def main():
    if len(argv) < 2:
        print "usage: ./import.py name.cfg\nOr ./import.py dummy"
        return

    if argv[1]=='dummy':
        try: remove('dummy.db')
        except: pass
        conn,curs=connect_sqlite('dummy.db')
        exec(dummycfg())
        writedummydata()
    elif argv[1]='vald':
         conn,curs=connect_mysql()
         config=readcfg('merged.cfg')
    else:
        dbname=s.replace(argv[1],'.cfg','')+'.db'
        conn,curs=connect_sqlite(dbname)
        config=readcfg(argv[1])

    for tconf in config['tables']:
        createtable(curs,tconf)
        filldata(curs,tconf)

    conn.commit() # IMPORTANT! This actually writes the database.
                  # Before everything's only in memory.
    

if __name__ == '__main__':
    main()
