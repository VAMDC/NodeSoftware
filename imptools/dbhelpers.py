#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

helper functions to create and fill the database

"""

import string as s

def readcfg(fname):
    """
       Read the config dictionary from a file.
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
    #print sql
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
    sql+='cfmt VARCHAR(64),'
    sql+='PRIMARY KEY (cname)'
    sql+=' );'
    
    curs.execute(sql)

def fillmeta(curs,conf):
    """
        fills the meta table according to the config
    """
    for table in conf['tables']:
        tname=table['tname']
        for col in table['columns']:
            sql='INSERT INTO meta VALUES (?, ?, ?, ?, ?)'
            d=(col['cname'],tname,col['ccom'],col['cunit'],col['cfmt'])
            #print sql,d
            curs.execute(sql,d)

def createindices(curs,conf):
    pass
        
    

def splitfixedcol(line,cols,delim):
    data=[]
    for col in cols:
        start=col['cbyte'][0]
        end=col['cbyte'][1]
        data.append(s.strip(line[start:end]))
    return data

def splitbydelim(line,cols,delim):
    data=[]
    for col in cols:
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
        if line.startswith(tconf['commentchar']): continue
        data=splitter(line,tconf['columns'],delim)
        data=tconf['function'](data)
        sql='INSERT INTO %s '%(tconf['tname'])
        sql+=' VALUES (%s)'%s.join(('?',)*len(data),', ')
        #print sql,data
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
