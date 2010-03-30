#!/usr/bin/env python

from vamdc import db,xmltools

conn,curs=db.cursors.sqlite('vald.db')

xmltools.c.run(curs)