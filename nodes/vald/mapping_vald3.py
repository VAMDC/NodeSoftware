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
import os, sys

# Import models for one particular node
os.environ['DJANGO_SETTINGS_MODULE']="nodes.vald.settings"
from vald.node import models 

# import the line funcs
from linefuncs import charrange, charrange2int, bySepNr, lineSplit

# 
# Create a config, a list of file definitions. Each entry in this
# list is a dictionary describing an input ascii file to build from.
# Each file dict definition supports the following keys
#   model       (django.db.model) - which Django model this file should populate
#   fname       (str)             - the file name
#   headlines   (int)             - number of header lines to skip   
#   commentchar (str)             - comment symbol (like #, ; etc) used in file
#   updatematch (str)             - gives the field used when updating an existing model of the given type.
#                                   The value in this column will be matched in the database to retrieve such an object. 
#   cnull       (str/value)       - if defined, defines a str/value that should be ignored (e.g. 'N/A')
#   debug       (bool)            - optional flag for debugging the parsing of a particular column
#   columns     (dict)
#                cname (str)      - collumn name
#                cbyte (tup)      - method to process the line and tuple to be fed to this method
#                references (tup) - which django model referenced by this collumn, and which field name
# 

# 
# Custom parser commands
#
# These always take line as the first argument; this is a list of line-strings
# (that may be only one line long) from all the files referenced in this step.
# All utility functions (bySepNr etc) make use of linedata[0] unless the keyword 'filenum'
# is given with a different index.

def get_srcfile_ref(linedata, sep1, sep2):
    "extract srcfile reference"
    l1 = bySepNr(linedata, sep1)
    l2 = bySepNr(l1, sep2, '/')
    return l2.strip("'").strip()
def get_publications(linedata):
    "extract publication data. This returns a list since it is for a multi-reference."
    return [p.strip() for p in bySepNr(linedata, 4, '||').split(',')]
def get_term_val(linedata, sep1, sep2):
    "extract configurations from term file"
    l1 = bySepNr(linedata, sep1, ':', filenum=1)
    return bySepNr(l1, sep2, ',')
def get_gammawaals(linedata, sep1, sep2):
    "extract gamma - van der waal value"
    l1 = charrange(linedata, sep1, sep2)    
    if float(l1) < 0:
        return l1
    else:
        return '0.000'
def get_alphawaals(linedata, sep1, sep2):
    "extract alpha - van der waal value"
    l1 = charrange(linedata, sep1, sep2)    
    if float(l1) > 0:
        return "%s.%s" % (0, bySepNr(linedata, 1, '.'))
    else:
        return '0.000'    
def get_sigmawaals(linedata, sep1, sep2):
    "extract sigma - van der waal value"
    l1 = charrange(linedata, sep1, sep2)   
    if float(l1) > 0:
        return bySepNr(0, '.')
    else:
        return '0.000'
def get_accur(linedata, range1, range2):
    "extract accuracy"
    return "%s,%s" % (charrange(linedata, *range1), charrange(linedata, *range2))
def merge_cols(linedata, *ranges):
    """
    Merges data from several columns into one, separating them with '-'.
     ranges are any number of tuples (indexstart, indexend) defining the columns.
    """
    return '-'.join([charrange(linedata, *ran) for ran in ranges])
    
# Base directory for the data files

base = "/vald/"

species_list_file = base + 'VALD_list_of_species'
vald_cfg_file = base + 'VALD3_config_2010.cfg'
vald_file = base + 'vald3.dat'
terms_file = base + 'terms'
publications_file = base + "publications_preprocessed.dat"
pub2source_file = base + "publications_to_sources_map.dat"

mapping = [
    # Populate Species model, using the species input file.
    {'model':models.Species,
     'fname':species_list_file,
     'headlines':0,
     'commentchar':'#',
     'linemap':[
            {'cname':'pk',
             'cbyte':(charrange, 0,7)},
            {'cname':'name',
             'cbyte':(charrange, 9,19)},
            {'cname':'ion',
             'cbyte':(charrange, 20,22)},
            {'cname':'mass',
             'cbyte':(charrange, 23,30)},
            {'cname':'massno',
             'cbyte':(charrange2int, 23,30)},
            {'cname':'ionen',
             'cbyte':(charrange, 31,40)},
            {'cname':'solariso',
             'cbyte':(charrange, 41,46)},
            {'cname':'ncomp',
             'cbyte':(charrange, 132,133)},
            {'cname':'atomic',
             'cbyte':(charrange, 134,136)},
            {'cname':'isotope',
             'cbyte':(charrange, 137,140)},
           ],
     }, # end of definition for species file

    # Populate Publication model with pre-processed bibtex data file
    {'model':models.Publication,    
     'fname':publications_file,
     'headlines':0,        
     'commentchar':'#',    
     'linemap':[           
            {'cname':'dbref',
             'cbyte':(bySepNr, 0,'||')},
            {'cname':'bibref',
             'cbyte':(bySepNr, 1,'||')},  
            {'cname':'author',
             'cbyte':(bySepNr, 2,'||')},  
            {'cname':'title',
             'cbyte':(bySepNr, 3,'||')},  
            {'cname':'category',
             'cbyte':(bySepNr, 4,'||')},  
            {'cname':'year',
             'cbyte':(bySepNr, 5,'||')},  
            {'cname':'journal',
             'cbyte':(bySepNr, 6,'||')},  
            {'cname':'volume',
             'cbyte':(bySepNr, 7,'||')},  
            {'cname':'pages',
             'cbyte':(bySepNr, 8,'||')},  
            {'cname':'url',
             'cbyte':(bySepNr, 9,'||')},            
            {'cname':'bibtex',
             'cbyte':(bySepNr, 10,'||')}, 
          ], 
      }, # end of bibtex public5Bation data
    
    # Populate Source model from vald_cfg file
    {'model':models.Source,
     'fname':vald_cfg_file,
     'headlines':1,
     'commentchar':';',
     'linemap':[
            {'cname':'pk',
             'cbyte':(bySepNr, 1)},
            {'cname':'srcfile',
             'cbyte':(bySepNr, 0)},
            {'cname':'srcfile_ref',             
             'cbyte':(get_srcfile_ref, 0, 3)},
            {'cname':'speclo',
             'cbyte':(bySepNr, 2),
             'references':(models.Species,'pk')},
            {'cname':'spechi',
             'cbyte':(bySepNr, 3),
             'references':(models.Species,'pk')},
            {'cname':'listtype',
             'cbyte':(bySepNr, 4)},
            {'cname':'r1',
             'cbyte':(bySepNr, 5)},
            {'cname':'r2',
             'cbyte':(bySepNr, 6)},
            {'cname':'r3',
             'cbyte':(bySepNr, 7)},
            {'cname':'r4',
             'cbyte':(bySepNr, 8)},
            {'cname':'r5',
             'cbyte':(bySepNr, 9)},
            {'cname':'r6',
             'cbyte':(bySepNr, 10)},
            {'cname':'r7',
             'cbyte':(bySepNr, 11)},
            {'cname':'r8',
             'cbyte':(bySepNr, 12)},
            {'cname':'r9',
             'cbyte':(bySepNr, 13)},
            {'cname':'srcdescr',
             'cbyte':(bySepNr, 14)},
            ],
    }, # end of definition for vald_conf file

    # Populate Source model with publications through pub2source file 
    {'model':models.Source,
     'fname':pub2source_file,
     'headlines':3,
     'commentchar':'#',
     'updatematch': 'srcfile_ref',
     'linemap':[
            {'cname':'srcfile_ref',
             'cbyte':(bySepNr, 1,'||'),
             'debug':False},
            {'cname':'publications',
             'cbyte':(get_publications, ), # must return a list!
             'multireferences':(models.Publication, 'dbref'),
             'debug':False}
             ]
    },

# State model read from states_file -upper states
    # (first section) 
    {'model':models.State,    
     'fname': (vald_file, terms_file),
     'headlines':(2, 0),
     'commentchar': ('#', '#'),
     'linestep':(1, 2),
     'lineoffset':(0,1),
     'errline':("Unknown", "Unknown"),
     'linemap':[
            {'cname':'charid',        #species,coup,jnum,term,energy (upper states)             
             'cbyte':(merge_cols,
                      (30,36), (170,172), (77,82), (172,218), (63,77))}, 
            {'cname':'species',
             'cbyte':(charrange, 30,36),
             'references':(models.Species,'pk')},
            {'cname':'energy',
             'cbyte':(charrange, 63,77)},
            #{'cname':'j',   
            # 'cbyte':(charrange, 77,82),},
            {'cname':'lande',
             'cbyte':(charrange, 88,94),
             'cnull':'99.00'},
            {'cname':'coupling',
             'cbyte':(charrange, 170,172)},
            {'cname':'term',
             'cbyte':(charrange, 172,218)},
            {'cname':'energy_ref',
             'cbyte':(charrange, 264,268)},
             #'references':(models.Source,'pk')},
            {'cname':'lande_ref',
             'cbyte':(charrange, 268,272)},
             #'references':(models.Source,'pk')},
            {'cname':'level_ref',
             'cbyte':(charrange, 284,288)},
             #'references':(models.Source,'pk')},
            # these are read from term file
            {'cname':'j',
             'filenum':1, # use term file
             'cbyte':(get_term_val, 2,1),
             'cnull':'X',},
            {'cname':'l',
             'filenum':1, # use term file
             'cbyte':(get_term_val, 2,2),
             'cnull':'X',},
            {'cname':'s',
             'filenum':1, # use term file
             'cbyte':(get_term_val, 2,3),
             'cnull':'X',},
            {'cname':'p',
             'filenum':1, # use term file
             'cbyte':(get_term_val, 2,4),
             'cnull':'X',},
            {'cname':'j1',
             'filenum':1, # use term file
             'cbyte':(get_term_val, 2,5),
             'cnull':'X',},
            {'cname':'j2',
             'filenum':1, # use term file
             'cbyte':(get_term_val, 2,6),
             'cnull':'X',},
            {'cname':'k',
             'filenum':1, # use term file
             'cbyte':(get_term_val, 2,7),
             'cnull':'X',},
            {'cname':'s2',
             'filenum':1, # use term file
             'cbyte':(get_term_val, 2,8),
             'cnull':'X',},
            {'cname':'jc',
             'filenum':1, # use term file
             'cbyte':(get_term_val, 2,9),
             'cnull':'X',},
            ]
     }, # end of State-model creation - upper states
    
    # State model read from states_file - lower states
    # (second section)
    {'model':models.State,
     'fname':(vald_file, terms_file),
     'headlines':(2, 0), 
     'commentchar':('#','#'),
     'linestep':(1, 2),     
     'errline':("Unknown", "Unknown"),
     'linemap':[
            {'cname':'charid',         #species,coup,jnum,term,energy (lower states) 
             'cbyte':(merge_cols,
                      (30,36), (122,124), (58,63), (124,170), (44,58))},
            {'cname':'species',
             'cbyte':(charrange, 30,36) ,
             'references':(models.Species,'pk')},
            {'cname':'energy',
             'cbyte':(charrange, 44,58)},
            #{'cname':'j',
            # 'cbyte':(charrange, 58,63)},
            {'cname':'lande',
             'cbyte':(charrange, 82,88),
             'cnull':'99.00'},
            {'cname':'coupling',
             'cbyte':(charrange, 122,124)},
            {'cname':'term',
             'cbyte':(charrange, 124,170)},
            {'cname':'energy_ref',
             'cbyte':(charrange, 264,268)},
             #'references':(models.Source,'pk')},
            {'cname':'lande_ref',
             'cbyte':(charrange, 268,272)},
             #'references':(models.Source,'pk')},
            {'cname':'level_ref',
             'cbyte':(charrange, 284,288)},
             #'references':(models.Source,'pk')},
            # these are read from term file
            {'cname':'j',
             'cbyte':(get_term_val, 2,1),           
             'cnull':'X',},
            {'cname':'l',
             'cbyte':(get_term_val, 2,2),
             'cnull':'X',},
            {'cname':'s',
             'cbyte':(get_term_val, 2,3),
             'cnull':'X',},
            {'cname':'p',
             'cbyte':(get_term_val, 2,4),
             'cnull':'X',},
            {'cname':'j1',
             'cbyte':(get_term_val, 2,5),
             'cnull':'X',},
            {'cname':'j2',
             'cbyte':(get_term_val, 2,6),
             'cnull':'X',},
            {'cname':'k',
             'cbyte':(get_term_val, 2,7),
             'cnull':'X',},
            {'cname':'s2',
             'cbyte':(get_term_val, 2,8),
             'cnull':'X',},
            {'cname':'jc',
             'cbyte':(get_term_val, 2,9),
             'cnull':'X',},
            ]
     }, # end of State model creation - lower states
   
    # Transition model, using the vald file    
    {'model':models.Transition,
     'fname':vald_file,
     'headlines':2,
     'commentchar':'#',
     'linemap':[
            {'cname':'vacwave',
             'cbyte':(charrange, 0,15)},
            {'cname':'airwave',
             'cbyte':(charrange, 15,30)},
            {'cname':'species',
             'cbyte':(charrange, 30,36),
             'references':(models.Species,'pk')},
            {'cname':'loggf',
             'cbyte':(charrange, 36,44)},
            {'cname':'landeff',
             'cbyte':(charrange, 94,100),
             'cnull':'99.00'},
            {'cname':'gammarad',
             'cbyte':(charrange, 100,107),
             'cnull':'0.0'},
            {'cname':'gammastark',
             'cbyte':(charrange, 107,114),
             'cnull':'0.000'},            
            {'cname':'gammawaals',
             'cbyte':(get_gammawaals, 114,122),
             'cnull':'0.000',
             'debug':False},
            {'cname':'sigmawaals', # only filled if raw value > 0.  
             'cbyte':(get_sigmawaals, 114,122),
             'cnull':'0.000',
             'debug':False},
            {'cname':'alphawaals',
             'cbyte':(get_alphawaals, 114,122),
             'cnull':'0.000',
             "debug":False},
            {'cname':'srctag',
             'cbyte':(charrange, 218,225),
             'references':(models.Publication,'dbref'),
             'skiperror':True},             
            #            {'cname':'acflag',
#             'cbyte':(charrange,(225,226))},
#            {'cname':'accur',
#             'cbyte':(charrange,(226,236))},
            {'cname':'accur',
             'cbyte':(get_accur, (225,226), (226,236)),
             'debug':False},
            {'cname':'comment',
             'cbyte':(charrange, 236,252)},
            {'cname':'wave_ref',             
             'cbyte':(charrange, 252,256)},
             #'references':(models.Source,'pk')},
            {'cname':'loggf_ref',
             'cbyte':(charrange, 256,260)},
             #'references':(models.Source,'pk')},
            {'cname':'lande_ref',
             'cbyte':(charrange, 268,272)},
             #'references':(models.Source,'pk')},
            {'cname':'gammarad_ref',
             'cbyte':(charrange, 272,276)},
             #'references':(models.Source,'pk')},
            {'cname':'gammastark_ref',
             'cbyte':(charrange, 276,280)},
             #'references':(models.Source,'pk')},
            {'cname':'waals_ref',  
             'cbyte':(charrange, 280,284)},
             #'references':(models.Source,'pk')},            
            {'cname':'upstateid',     #species,coup,jnum,term,energy   
             'cbyte':(merge_cols,
                      (30,36), (170,172), (77,82), (172,218),(63,77))},
            {'cname':'lostateid',
             'cbyte':(merge_cols,
                      (30,36), (122,124), (58,63), (124,170), (44,58))},
            {'cname':'upstate',
             'cbyte':(merge_cols,
                      (30,36), (170,172), (77,82), (172,218), (63,77)),
             'references':(models.State,'charid')},
            {'cname':'lostate',
             'cbyte':(merge_cols,
                      (30,36), (122,124), (58,63), (124,170), (44,58)),
             'references':(models.State,'charid')},
            ],
    } # end of vald file def

] # end of vald3 mapping file def list

mapping=[mapping[-1]]
