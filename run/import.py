#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from vamdc.imptools import *

def main():
    if len(sys.argv) < 2:
        print "Usage: ./import.py name.cfg\nOr ./import.py dummy\nOr ./import.py vald[sqlite|mysql]"
        return

    if sys.argv[1]=='dummy':
        try: os.remove('dummy.db')
        except: pass
        conn,curs=sqlite('dummy.db')
        config=dummycfg
        writedummydata()
        dbtype='sqlite'
    elif sys.argv[1]=='valdsqlite':
        #try: os.remove('vald.db')
        #except: pass
        conn,curs=sqlite('vald.db')
        config=vald3cfg
        dbtype='sqlite'
    elif sys.argv[1]=='valdmysql':
        conn,curs=mysql('vald','V@ld','vald')
        try: curs.execute('drop table transitions; drop table meta; drop table sources; drop table species; drop table states;'); conn.commit()
        except: pass
        config=vald3cfg
        dbtype='mysql'
    else:
        dbname=s.replace(sys.argv[1],'.cfg','')+'.db'
        conn,curs=sqlite(dbname)
        config=readcfg(sys.argv[1])
        dbtype='sqlite'
    
    #createmeta(curs)
    fillmeta(curs,config)

    for tconf in config['tables']:
        print 'Working on table %s:'%tconf['tname'],
        #print 'Create...',
        #createtable(curs,tconf,dbtype)
        print 'done. Fill...',
        filldata(curs,tconf,dbtype)
        print 'done.'
    conn.commit() # IMPORTANT! This actually writes the database.
                  # Before everything's only in memory.
    conn.close()

if __name__ == '__main__':
    main()



