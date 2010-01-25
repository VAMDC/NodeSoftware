#!/usr/bin/env python

from sqlite3 import dbapi2 as sqlite
from os.path import join,exists
import string as s
from sys import argv

DBNAME='merged.db'

def readcfg(fname='merged.cfg'):
    f=open(fname)
    exec(s.join(f.readlines()))
    
    print config
    return config
    
def createtables(curs,tconf):
    
        sql='CREATE TABLE IF NOT EXISTS %s '%tconf['tname']
        sql+='(id INTEGER PRIMARY KEY, '
        for i,colname in enumerate(tconf['colnames']):
            sql+='%s %s, '%(colname,tconf['coltypes'][i])
        sql=sql[:-2]
        sql+=');'
        print sql
        curs.execute(sql)

def filldata(curs,tconf):
    delim=tconf['delim']
    f=open(tconf['fname'])
    
    for line in f:
        print line.split(delim)

def setupdb(dbname=DBNAME):
    conn=sqlite.connect(dbname)
    curs=conn.cursor()
    return conn,curs



def main():
    conn,curs=setupdb()
    config=readcfg(argv[1])
    for tconf in config['tables']:
        createtables(curs,tconf)
        filldata(curs,tconf)
    conn.commit()
    

if __name__ == '__main__':
    main()
