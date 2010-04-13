from vamdc.db import *

def sqlite(DBNAME):
	conn=sqlitedb.connect(DBNAME)
	curs=conn.cursor()
	curs.__dict__['par']='?'
	return conn,curs

def mysql(user,passwd,db,host='localhost'):
	conn = MySQLdb.connect(host=host,user=user,passwd=passwd,db=db)
	curs=conn.cursor()
	curs.__dict__['par']='%s'
	return conn,curs


