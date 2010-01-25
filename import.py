#!/usr/bin/env python

from sqlite3 import dbapi2 as sqlite
from os.path import join,exists
from os import remove
import string as s
from sys import argv

def readcfg(fname):
    f=open(fname)
    exec(s.join(f.readlines()))
    
    print config
    return config
    
def createtable(curs,tconf):
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
    for i in range(tconf['headlines']):
        f.readline()
    for line in f:
        l=line.split()
        if len(l) != len(tconf['colnames']):
            print 'skipped line'
            continue
        sql='INSERT INTO %s '%(tconf['tname'])
        curs.execute(sql+' VALUES (NULL, %s)'%s.join(('?')*len(l),', '),tuple(l))
        

def setupdb(dbname):
    conn=sqlite.connect(dbname)
    curs=conn.cursor()
    return conn,curs

def dummycfg():
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
        conn,curs=setupdb('dummy.db')
        exec(dummycfg())
        writedummydata()
    else:
        dbname=s.replace(argv[1],'.cfg','')+'.db'
        conn,curs=setupdb(dbname)
        config=readcfg(argv[1])

    for tconf in config['tables']:
        createtable(curs,tconf)
        filldata(curs,tconf)
    conn.commit()
    

if __name__ == '__main__':
    main()
