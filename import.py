#!/usr/bin/env python
# -*- coding: utf-8 -*-


from import-tools import *

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



