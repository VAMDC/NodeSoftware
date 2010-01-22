#!/usr/bin/env python

from sqlite3 import dbapi2 as sqlite
DBNAME=join('/','data','sdss','sdss.db')

def readformat(fname=)

def setupdb(dbname=DBNAME):
    if not exists(dbname): newdb=True
    else: newdb=False

    connection=sqlite.connect(dbname)
    cursor=connection.cursor()

    if newdb:
        cursor.execute('CREATE TABLE sdss (objID INTEGER PRIMARY KEY)')
        connection.commit()

    return connection,cursor




def main():
    conn,curs=setupdb()
    

if __name__ == '__main__':
    main()
