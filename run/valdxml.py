#!/usr/bin/env python

from vamdc import db
from vamdc.xmltools import customxml as c

conn,curs=db.cursors.sqlite('vald.db')
c.run(curs,outname='../xsl/vald.xml')