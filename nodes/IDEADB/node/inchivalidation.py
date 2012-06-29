#!/usr/bin/python

from suds.client import Client
import suds
import re

url = 'http://www.chemspider.com/InChI.asmx?WSDL'

client = Client(url)

def inchi2inchikey(inchi):
    try:
        result = client.service.InChIToInChIKey(inchi)
    except suds.WebFault as detail:
        result = ''
    return result

def inchikey2inchi(inchikey):
    try:
        result = client.service.InChIKeyToInChI(inchikey)
    except suds.WebFault as detail:
        result = ''
    return result

def inchi2chemicalformula(inchi):
    match = re.match('^InChI=1S/(([A-Z]{1}[a-z]{0,2}[0-9]{0,3})+)+/.*$', inchi)
    if match is not None:
        return match.group(1)
    else:
        return None

def inchikey2chemicalformula(inchikey):
    inchi = inchikey2inchi(inchikey)
    return inchi2chemicalformula(inchi)
