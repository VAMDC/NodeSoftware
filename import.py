#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from imptools import *

def main():
    if len(sys.argv) < 2:
        print "usage: ./import.py name.cfg\nOr ./import.py dummy"
        return

    if sys.argv[1]=='dummy':
        try: os.remove('dummy.db')
        except: pass
        conn,curs=connect_sqlite('dummy.db')
        config=dummycfg
        writedummydata()
    elif sys.argv[1]=='vald':
         conn,curs=connect_mysql()
         try: curs.execute('drop table merged; drop table meta; drop table refs;'); conn.commit()
         except: pass
         config=valdcfg
    else:
        dbname=s.replace(sys.argv[1],'.cfg','')+'.db'
        conn,curs=connect_sqlite(dbname)
        config=readcfg(sys.argv[1])

    createmeta(curs)
    fillmeta(curs,config)

    for tconf in config['tables']:
        print tconf['tname']
        createtable(curs,tconf)
        filldata(curs,tconf)

    conn.commit() # IMPORTANT! This actually writes the database.
                  # Before everything's only in memory.
    conn.close()

if __name__ == '__main__':
    main()



