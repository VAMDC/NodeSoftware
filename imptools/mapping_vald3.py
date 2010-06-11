#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Defines a mapping dictionary that maps between data columns 
in raw ascii data files and defines how they should be stored
into a relational (django) database.

A file like this should be created for every unique database.
It should normally contain a global list, conventionally named
'mappings', that define how data fields are to be translated into
django fields. To properly map, a custom processor also probably
has to be constructed in dbhelper as well.
"""

from string import strip
import os

#
# Functions applied to data after reading
#
def charrange(line, start, end):
    """
    Cut out part of a line of texts based on indices
    """
    return strip(line[start:end])

def charrange2int(line, start, end):
    """
    Character to integer extraction
    """
    return int(round(float(charrange(line, start, end))))

def bySepNr(line, number, sep=','):
    """
    Split a text line by sep argument and return
    the split section with given number
    """
    return strip(line.split(sep)[number])

def makeValdUpperStateKey(line):
    """
    Create a hash string linking a particular record to
    an upper state.
    """
    species=charrange(line,30,36) # id number
    coup=charrange(line,170,172) # coupling (e.g. LS)
    term=charrange(line,172,218) # term id
    if not (coup and term and species): return None
    return '%s-%s-%s' % (species, coup, term)

def makeValdLowerStateKey(line):
    """
    Create a hash string linking a particular record to
    a lower state.
    """
    species=charrange(line,30,36) # id number
    coup=charrange(line,122,124) # coupling (e.g. LS)
    term=charrange(line,124,170) # term id 
    if not (coup and term and species): return None
    return '%s-%s-%s' % (species, coup, term)

# 
# Create a config, a list of file definitions. Each entry in this
# list is a dictionary describing an input ascii file to build from.
# Each file dict definition supports the following keys
#   model       (django.db.model) - which Django model this file should populate
#   fname       (str)             - the file name
#   headlines   (int)             - number of header lines to skip   
#   commentchar (str)             - comment symbol (like #, ; etc) used in file
#   updatematch (str)             - TODO
#   cnull       (str/value)       - if defined, defines a str/value that should be ignored (e.g. 'N/A')
#   columns     (dict)
#                cname (str)      - collumn name
#                cbyte (tup)      - method to process the line and tuple to be fed to this method
#                references (tup) - which django model referenced by this collumn, and which field name
# 

# Import models for one particular node
os.environ['DJANGO_SETTINGS_MODULE']="vamdc.DjVALD.settings"
from DjVALD.vald import models as valdmodel

# Base directory for the data files

base = "/vald/"
#base = "/home/samreg/Project/VAMDC/vamdc-griatch/imptools/vald_raw/"

species_list_file = base + 'VALD_list_of_species'
vald_cfg_file = base + 'vald3_test.cfg'
states_file = base + 'states_u.dat'
vald_file = base + 'vald3.dat'
terms_file = base + 'myterms.dat'

mapping = [
    # species file 
    {'model':valdmodel.Species,     
     'fname':species_list_file,
     'headlines':0,   
     'commentchar':'#',   
     'columns':[          
            {'cname':'pk',  
             'cbyte':(charrange,(0,7))},   
            {'cname':'name',  
             'cbyte':(charrange,(9,19))},   
            {'cname':'ion',  
             'cbyte':(charrange,(20,22))},   
            {'cname':'mass',  
             'cbyte':(charrange,(23,30))},   
            {'cname':'massno',  
             'cbyte':(charrange2int,(23,30))},   
            {'cname':'ionen',  
             'cbyte':(charrange,(31,40))},   
            {'cname':'solariso',  
             'cbyte':(charrange,(41,47))},   
            {'cname':'ncomp',  
             'cbyte':(charrange,(132,133))},   
            {'cname':'atomic',  
             'cbyte':(charrange,(134,136))},   
            {'cname':'isotope',  
             'cbyte':(charrange,(137,140))},   
           ],
     }, # end of definition for species file

    # vald_cfg file
    {'model':valdmodel.Source,
     'fname':vald_cfg_file,
     'headlines':1,
     'commentchar':';',
     'columns':[\
            {'cname':'pk',
             'cbyte':(bySepNr,(1,))},
            {'cname':'srcfile',
             'cbyte':(bySepNr,(0,))},
            {'cname':'speclo',
             'cbyte':(bySepNr,(2,)),
             'references':(valdmodel.Species,'pk')},
            {'cname':'spechi',
             'cbyte':(bySepNr,(3,)),
             'references':(valdmodel.Species,'pk')},
            {'cname':'listtype',
             'cbyte':(bySepNr,(4,))},
            {'cname':'r1',
             'cbyte':(bySepNr,(5,))},
            {'cname':'r2',
             'cbyte':(bySepNr,(6,))},
            {'cname':'r3',
             'cbyte':(bySepNr,(7,))},
            {'cname':'r4',
             'cbyte':(bySepNr,(8,))},
            {'cname':'r5',
             'cbyte':(bySepNr,(9,))},
            {'cname':'r6',
             'cbyte':(bySepNr,(10,))},
            {'cname':'r7',
             'cbyte':(bySepNr,(11,))},
            {'cname':'r8',
             'cbyte':(bySepNr,(12,))},
            {'cname':'r9',
             'cbyte':(bySepNr,(13,))},
            {'cname':'srcdescr',
             'cbyte':(bySepNr,(14,)),},
            ],
    }, # end of definition for vald_cnf file

    # state file (used for first pass, to get upper states)
    {'model':valdmodel.State,   
     'fname':states_file,
     'headlines':0,     
     'commentchar':'#',   
     'columns':[          
            {'cname':'charid',  
             'cbyte':(bySepNr,(0,';'))},
            {'cname':'species',
             'cbyte':(bySepNr,(1,';')),
             'references':(valdmodel.Species,'pk')},
            {'cname':'energy',
             'cbyte':(bySepNr,(2,';'))},
            {'cname':'lande',
             'cbyte':(bySepNr,(3,';')),
             'cnull':'99.00'},
            {'cname':'coupling',
             'cbyte':(bySepNr,(4,';'))},
            {'cname':'term',
             'cbyte':(bySepNr,(5,';'))},
            {'cname':'energy_ref',
             'cbyte':(bySepNr,(6,';'))},
            {'cname':'lande_ref',
             'cbyte':(bySepNr,(7,';'))},
            {'cname':'level_ref',
             'cbyte':(bySepNr,(8,';'))},
            ]
     }, # end of state file 

    # vald file 
    {'model':valdmodel.Transition,    
     'fname':vald_file,
     'headlines':2,        
     'commentchar':'#',    
     'columns':[           
            {'cname':'vacwave',
             'cbyte':(charrange,(0,15))},  
            {'cname':'airwave',
             'cbyte':(charrange,(15,30))},  
            {'cname':'species',
             'cbyte':(charrange,(30,36)),
             'references':(valdmodel.Species,'pk')},
            {'cname':'loggf',
             'cbyte':(charrange,(36,44))},
            {'cname':'landeff',
             'cbyte':(charrange,(94,100)),
             'cnull':'99.00'},
            {'cname':'gammarad',
             'cbyte':(charrange,(100,107)),
             'cnull':'0.0'},
            {'cname':'gammastark',
             'cbyte':(charrange,(107,114)),
             'cnull':'0.0'},
            {'cname':'gammawaals',
             'cbyte':(charrange,(114,122)),
             'cnull':'0.0'},
            {'cname':'srctag',
             'cbyte':(charrange,(218,225))},
            {'cname':'acflag',
             'cbyte':(charrange,(225,226))},
            {'cname':'accur',
             'cbyte':(charrange,(226,236))},
            {'cname':'comment',
             'cbyte':(charrange,(236,252))},
            {'cname':'wave_ref',
             'cbyte':(charrange,(252,256))},
            {'cname':'loggf_ref',
             'cbyte':(charrange,(256,260))},
            {'cname':'lande_ref',
             'cbyte':(charrange,(268,272))},
            {'cname':'gammarad_ref',
             'cbyte':(charrange,(272,276))},
            {'cname':'gammastark_ref',
             'cbyte':(charrange,(276,280))},
            {'cname':'gammawaals_ref',
             'cbyte':(charrange,(280,284))},
            {'cname':'upstateid',
             'cbyte':(makeValdUpperStateKey,())},
            {'cname':'lostateid',
             'cbyte':(makeValdLowerStateKey,())},
            {'cname':'upstate',
             'cbyte':(makeValdUpperStateKey,()),
             'references':(valdmodel.State,'charid')},
            {'cname':'lostate',
             'cbyte':(makeValdLowerStateKey,()),
             'references':(valdmodel.State,'charid')},
            ],
    }, # end of vald file def 

    # term file 
    {'model':valdmodel.State,
     'fname':terms_file,
     'headlines':0,
     'commentchar':'#',
     'updatematch':'charid',
     'columns':[\
            {'cname':'charid',
             'cbyte':(bySepNr,(0,';'))},
            {'cname':'J',
             'cbyte':(bySepNr,(1,';')),
             'cnull':'X',},
            {'cname':'L',
             'cbyte':(bySepNr,(2,';')),
             'cnull':'X',},
            {'cname':'S',
             'cbyte':(bySepNr,(3,';')),
             'cnull':'X',},
            {'cname':'P',
             'cbyte':(bySepNr,(4,';')),
             'cnull':'X',},
            {'cname':'J1',
             'cbyte':(bySepNr,(5,';')),
             'cnull':'X',},
            {'cname':'J2',
             'cbyte':(bySepNr,(6,';')),
             'cnull':'X',},
            {'cname':'K',
             'cbyte':(bySepNr,(7,';')),
             'cnull':'X',},
            {'cname':'S2',
             'cbyte':(bySepNr,(8,';')),
             'cnull':'X',},
            {'cname':'Jc',
             'cbyte':(bySepNr,(9,';')),
             'cnull':'X',},
            ] 
     } # end of term def  

] # end of vald3 mapping file def list



