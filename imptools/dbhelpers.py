#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

helper functions to create and fill the database

"""

from vamdc.db.cursors import *

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
    sql+='cfmt VARCHAR(64)'
#    sql+='PRIMARY KEY (cname)'
    sql+=' );'
    
    curs.execute(sql)

def fillmeta(curs,conf):
    """
        fills the meta table according to the config
    """
    for table in conf['tables']:
        tname=table['tname']
        for col in table['columns']:
            sql='INSERT INTO meta VALUES ("%s", "%s", "%s", "%s", "%s")'%(col['cname'],tname,col['ccom'],col['cunit'],col['cfmt'])
            sql=sql.replace('"NULL"','NULL')
            #print sql,d
            curs.execute(sql)

def createindices(curs,conf):
    pass
        
def filldata(curs,tconf):
    """
        read the data-files and fill the data into the tables in the DB
    """
    f=open(tconf['fname'])
    for i in range(tconf['headlines']):
        f.readline()

    for line in f:
        if line.startswith(tconf['commentchar']): continue
        data=[]
        for colconf in tconf['columns']:
            if colconf['cbyte']:
                fu=colconf['cbyte'][0]
                args=colconf['cbyte'][1]
                d=fu(line,*args)
                if d==colconf['cnull']:
                    data.append('NULL')
                else:
                    data.append(s.strip(d))
            else:
                data.append('NULL')

        sql='%s %s '%(tconf['method'],tconf['tname'])
        if tconf['method'].startswith('INSERT'):
            sql+=' VALUES ("%s'%s.join(data,'","')
            sql=sql+ '");'
        
        elif tconf['method'].startswith('UPDATE'):
            sql+='SET '
            for i,colconf in enumerate(tconf['columns']):
                sql+='%s="%s",'%(colconf['cname'],data[i])
            sql=sql[:-1] + ' WHERE id="%s"'%data[0]
        else:
            print 'Dont know what to do with method "%s"'%tconf['method']
            continue
        
        sql=sql.replace('"NULL"','NULL')
        #print sql
        curs.execute(sql)
        #sql+=' VALUES (%s)'%s.join(('?',)*len(data),', ')
        #curs.execute(sql,tuple(data))
        
 

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



### LEGACY BELOW HERE

def splitfixedcol(line,cols,delim):
    data=[]
    for col in cols:
        start=col['cbyte'][0]
        end=col['cbyte'][1]
        d=s.strip(line[start:end])
        if d==col['cnull']: d='NULL'
        data.append(d)
    return data

def splitbydelim(line,cols,delim):
    data=[]
    for col in cols:
        d=line.split(delim)[col['cbyte']] 
        d=s.strip(d)
        if d==col['cnull']: d='NULL'
        data.append(d)
    return data
    
def filldata_old(curs,tconf):
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
        sql='INSERT OR IGNORE INTO %s '%(tconf['tname'])
        sql+=' VALUES ("%s'%s.join(data,'","')
        sql=sql+ '")'
        sql=sql.replace('"NULL"','NULL')
        #print sql
        curs.execute(sql)
        #sql+=' VALUES (%s)'%s.join(('?',)*len(data),', ')
        #curs.execute(sql,tuple(data))
        
