from vamdc.db import *

def sqlite(DBNAME):
	conn=sqlitedb.connect(DBNAME)
	return conn,conn.cursor()

def mysql(user,passwd,db,host='localhost'):
    conn = MySQLdb.connect(host=host,user=user,passwd=passwd,db=db)
    return conn,conn.cursor()

