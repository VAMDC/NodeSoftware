#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from vamdc.imptools import *

def main():
    if len(sys.argv) < 2:
        print "Usage: ./import.py name.cfg\nOr ./import.py dummy\nOr ./import.py vald"
        return

    if sys.argv[1]=='dummy':
        try: os.remove('dummy.db')
        except: pass
        conn,curs=sqlite('dummy.db')
        config=dummycfg
        writedummydata()
    elif sys.argv[1]=='vald':
        try: os.remove('vald.db')
        except: pass
        conn,curs=sqlite('vald.db')
        #try: curs.execute('drop table merged; drop table meta; drop table refs;'); conn.commit()
        #except: pass
        config=valdcfg
    else:
        dbname=s.replace(sys.argv[1],'.cfg','')+'.db'
        conn,curs=sqlite(dbname)
        config=readcfg(sys.argv[1])

    createmeta(curs)
    fillmeta(curs,config)

    for tconf in config['tables']:
        print 'Working on table %s:'%tconf['tname'],
        print 'Create...',
        createtable(curs,tconf)
        print 'done. Fill...',
        filldata(curs,tconf)
        print 'done.'

    conn.commit() # IMPORTANT! This actually writes the database.
                  # Before everything's only in memory.
    conn.close()

if __name__ == '__main__':
    main()



