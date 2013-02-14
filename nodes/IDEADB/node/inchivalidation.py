#!/usr/bin/python

from suds.client import Client
import suds
import re

url = 'http://www.chemspider.com/InChI.asmx?WSDL'
try:
    client = Client(url)
#except WebFault, f:
#    print f
except Exception, e:
    print e 

def inchi2inchikey(inchi):
    """Convert InChI to InChI-Key"""
    try:
        result = client.service.InChIToInChIKey(inchi)
    except suds.WebFault as detail:
        result = ''
    return result

def inchikey2inchi(inchikey):
    """Convert InChI-Key to InChI"""
    try:
        result = client.service.InChIKeyToInChI(inchikey)
    except suds.WebFault as detail:
        result = ''
    return result

def inchi2chemicalformula(inchi):
    """Extract chemical formula from InChI"""
    match = re.match('^InChI=1S/(([A-Z]{1}[a-z]{0,2}[0-9]{0,3})+)+(/)?.*$', str(inchi))
    if match is not None:
        return match.group(1)
    else:
        return None

def inchikey2chemicalformula(inchikey):
    """Convert InChi to InChI-Key and extract chemical formula from InChI"""
    inchi = inchikey2inchi(inchikey)
    return inchi2chemicalformula(inchi)
