#!/usr/bin/python

from suds.client import Client
import suds

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
