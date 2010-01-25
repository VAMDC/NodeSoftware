#!/usr/bin/env python

from sqlite3 import dbapi2 as sqlite
from os.path import join,exists
from sys import argv

DBNAME='merged.db'

def readcfg(fname='merged.cfg'):
    f=open(fname)
    exec(f.readlines())
    
    print config
    return config
    
def fillit(curs,config):
    delim=config['delim']
    for talbe in config['tables']

def setupdb(dbname=DBNAME):
    conn=sqlite.connect(dbname)
    curs=connection.cursor()
    return conn,curs



def main():
    conn,curs=setupdb()
    config=readcfg(argv[1])
    fillit(curs,config)
    conn.commit()
    

if __name__ == '__main__':
    main()
