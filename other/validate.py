#!/usr/bin/env python

from lxml import etree as e
from sys import stdin,stdout,argv,exit

if len(argv)<2:
    print "give an xsd file!"
elif len(argv)<3:
    xsd=open(argv[1])
    xml=stdin
else:
    xsd=open(argv[1])
    xml=open(argv[2])

xsd=e.XMLSchema(e.parse(xsd))
xml=e.parse(xml)

xsd.assertValid(xml)
