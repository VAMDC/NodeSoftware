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
#sys.path.append("..")
#os.environ['DJANGO_SETTINGS_MODULE']="DjVALD.settings"
from DjVALD.node import models as valdmodel

# import the line funcs
from imptools import charrange, charrange2int, bySepNr, chainCmds
from imptools import idFromLine, lineStrip, lineSplit, mergeCols
    
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

# Base directory for the data files

base = "/vald/"
#base = "/home/samreg/vamdc-git/imptools/vald_raw/"

# species_list_file = base + 'VALD_list_of_species'
# vald_cfg_file = base + 'vald3_test.cfg'
# states_file = base + 'states_preprocessed.dat'
# transitions_file = base + 'transitions_preprocessed.dat'
# terms_file = base + 'terms_preprocessed.dat'
# publications_file = base + "publications_preprocessed.dat"

species_list_file = base + 'VALD_list_of_species'
#vald_cfg_file = base + 'vald3_test.cfg'
vald_cfg_file = base + 'VALD3_config_2010.cfg'
vald_file = base + 'vald3.dat'
terms_file = base + 'terms'
publications_file = base + "publications_preprocessed.dat"
pub2source_file = base + "publications_to_sources_map.dat"


mapping = [
    # Populate Species model, using the species input file.
    {'model':valdmodel.Species,
     'fname':species_list_file,
     'headlines':0,
     'commentchar':'#',
     'linemap':[
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
             'cbyte':(charrange,(41,46))},
            {'cname':'ncomp',
             'cbyte':(charrange,(132,133))},
            {'cname':'atomic',
             'cbyte':(charrange,(134,136))},
            {'cname':'isotope',
             'cbyte':(charrange,(137,140))},
           ],
     }, # end of definition for species file

    # Populate Publication model with pre-processed bibtex data file
    {'model':valdmodel.Publication,    
     'fname':publications_file,
     'headlines':0,        
     'commentchar':'#',    
     'linemap':[           
            {'cname':'dbref',
             'cbyte':(bySepNr, (0,'||')),},  
            {'cname':'bibref',
             'cbyte':(bySepNr, (1,'||')),},  
            {'cname':'author',
             'cbyte':(bySepNr, (2,'||')),},  
            {'cname':'bibtex',
             'cbyte':(bySepNr, (3,'||')),},            
          ], 
      }, # end of bibtex public5Bation data
    
    # Populate Source model from vald_cfg file
    {'model':valdmodel.Source,
     'fname':vald_cfg_file,
     'headlines':1,
     'commentchar':';',
     'linemap':[
            {'cname':'pk',
             'cbyte':(bySepNr,(1,))},
            {'cname':'srcfile',
             'cbyte':(bySepNr,(0,))},
            {'cname':'srcfile_ref',             
             'cbyte':(chainCmds, ((bySepNr,(0,)),
                                  (bySepNr,(3,'/')),
                                  (lineStrip, ("'"))))},
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
    }, # end of definition for vald_conf file

    # Populate Source model with publications through pub2source file 
    {'model':valdmodel.Source,
     'fname':pub2source_file,
     'headlines':3,
     'commentchar':'#',
     'updatematch': 'srcfile_ref',
     'linemap':[
            {'cname':'srcfile_ref',
             'cbyte':(bySepNr,(1,'||')),
             'debug':False},
            {'cname':'publications',
             'cbyte':(chainCmds, ((bySepNr,(4,'||')),
                                  (lineSplit,(',',)))), # returns a list! 
             'multireferences':(valdmodel.Publication, 'dbref'),
             'debug':False}
             ]
    },

# State model read from states_file -upper states
    # (first section) 
    {'model':valdmodel.State,    
     'fname': (vald_file, terms_file),
     'headlines':(2, 0),
     'commentchar': ('#', '#'),
     'linestep':(1, 2),
     'lineoffset':(0,1),
     'errline':("Unknown", "Unknown"),
     'linemap':[
            {'cname':'charid',        #species,coup,jnum,term,energy (upper states)             
             'cbyte':(idFromLine,('-',(charrange,(30,36)),
                                      (charrange,(170,172)),
                                      (charrange,(77,82)),
                                      (charrange,(172,218)),
                                      (charrange,(63,77)) ))},           
            {'cname':'species',
             'cbyte':(charrange,(30,36)),
             'references':(valdmodel.Species,'pk')},
            {'cname':'energy',
             'cbyte':(charrange,(63,77))},
            #{'cname':'j',   
            # 'cbyte':(charrange,(77,82)),},
            {'cname':'lande',
             'cbyte':(charrange,(88,94)),
             'cnull':'99.00'},
            {'cname':'coupling',
             'cbyte':(charrange,(170,172))},
            {'cname':'term',
             'cbyte':(charrange,(172,218))},
            {'cname':'energy_ref',
             'cbyte':(charrange,(264,268))},
             #'references':(valdmodel.Source,'pk')},
            {'cname':'lande_ref',
             'cbyte':(charrange,(268,272))},
             #'references':(valdmodel.Source,'pk')},
            {'cname':'level_ref',
             'cbyte':(charrange,(284,288))},
             #'references':(valdmodel.Source,'pk')},
            # these are read from term file
            {'cname':'j',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(1,',')))),
             'cnull':'X',},
            {'cname':'l',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(2,',')))),         
             'cnull':'X',},
            {'cname':'s',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(3,',')))), 
             'cnull':'X',},
            {'cname':'p',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(4,',')))),
             'cnull':'X',},
            {'cname':'j1',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(5,',')))),
             'cnull':'X',},
            {'cname':'j2',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(6,',')))),
             'cnull':'X',},
            {'cname':'k',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(7,',')))),
             'cnull':'X',},
            {'cname':'s2',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(8,',')))),
             'cnull':'X',},
            {'cname':'jc',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(9,',')))),
             'cnull':'X',},
            ]
     }, # end of State-model creation - upper states
    
    # State model read from states_file - lower states
    # (second section)
    {'model':valdmodel.State,
     'fname':(vald_file, terms_file),
     'headlines':(2, 0), 
     'commentchar':('#','#'),
     'linestep':(1, 2),     
     'errline':("Unknown", "Unknown"),
     'linemap':[
            {'cname':'charid',         #species,coup,jnum,term,energy (lower states) 
             'cbyte':(idFromLine,('-',(charrange,(30,36)),
                                      (charrange,(122,124)),
                                      (charrange,(58,63)),
                                      (charrange,(124,170)),
                                      (charrange,(44,58)) ))},            
            {'cname':'species',
             'cbyte':(charrange,(30,36)) ,
             'references':(valdmodel.Species,'pk')},
            {'cname':'energy',
             'cbyte':(charrange,(44,58))},
            #{'cname':'j',
            # 'cbyte':(charrange,(58,63))},
            {'cname':'lande',
             'cbyte':(charrange,(82,88)),
             'cnull':'99.00'},
            {'cname':'coupling',
             'cbyte':(charrange,(122,124))},
            {'cname':'term',
             'cbyte':(charrange,(124,170))},
            {'cname':'energy_ref',
             'cbyte':(charrange,(264,268))},
             #'references':(valdmodel.Source,'pk')},
            {'cname':'lande_ref',
             'cbyte':(charrange,(268,272))},
             #'references':(valdmodel.Source,'pk')},
            {'cname':'level_ref',
             'cbyte':(charrange,(284,288))},
             #'references':(valdmodel.Source,'pk')},
            # these are read from term file
            {'cname':'j',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(1,',')))),
             'cnull':'X',},
            {'cname':'l',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(2,',')))),         
             'cnull':'X',},
            {'cname':'s',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(3,',')))), 
             'cnull':'X',},
            {'cname':'p',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(4,',')))),
             'cnull':'X',},
            {'cname':'j1',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(5,',')))),
             'cnull':'X',},
            {'cname':'j2',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(6,',')))),
             'cnull':'X',},
            {'cname':'k',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(7,',')))),
             'cnull':'X',},
            {'cname':'s2',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(8,',')))),
             'cnull':'X',},
            {'cname':'jc',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(9,',')))),
             'cnull':'X',},
            ]
     }, # end of State model creation - lower states
   
    # Transition model, using the vald file    
    {'model':valdmodel.Transition,
     'fname':vald_file,
     'headlines':2,
     'commentchar':'#',
     'linemap':[
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
             'cbyte':(charrange,(218,225)),
             'references':(valdmodel.Publication,'dbref')},             
#            {'cname':'acflag',
#             'cbyte':(charrange,(225,226))},
#            {'cname':'accur',
#             'cbyte':(charrange,(226,236))},
            {'cname':'accur',
             'cbyte':(mergeCols,(',',(charrange,(225,226)),
                                     (charrange,(226,236)))),
             'debug':True},
            {'cname':'comment',
             'cbyte':(charrange,(236,252))},
            {'cname':'wave_ref',             
             'cbyte':(charrange,(252,256))},
             #'references':(valdmodel.Source,'pk')},
            {'cname':'loggf_ref',
             'cbyte':(charrange,(256,260))},
             #'references':(valdmodel.Source,'pk')},
            {'cname':'lande_ref',
             'cbyte':(charrange,(268,272))},
             #'references':(valdmodel.Source,'pk')},
            {'cname':'gammarad_ref',
             'cbyte':(charrange,(272,276))},
             #'references':(valdmodel.Source,'pk')},
            {'cname':'gammastark_ref',
             'cbyte':(charrange,(276,280))},
             #'references':(valdmodel.Source,'pk')},
            {'cname':'gammawaals_ref',  
             'cbyte':(charrange,(280,284))},
             #'references':(valdmodel.Source,'pk')},            

            {'cname':'upstateid',     #species,coup,jnum,term,energy   
             'cbyte':(idFromLine,('-',(charrange,(30,36,)),
                                      (charrange,(170,172)),
                                      (charrange,(77,82)),
                                      (charrange,(172,218)),
                                      (charrange,(63,77)) ))},
            {'cname':'lostateid',
             'cbyte':(idFromLine,('-',(charrange,(30,36)),
                                      (charrange,(122,124)),
                                      (charrange,(58,63)),
                                      (charrange,(124,170)),
                                      (charrange,(44,58)) ))},
            {'cname':'upstate',
             'cbyte':(idFromLine,('-',(charrange,(30,36,)),
                                      (charrange,(170,172)),
                                      (charrange,(77,82)),
                                      (charrange,(172,218)),
                                      (charrange,(63,77)) )),
             'references':(valdmodel.State,'charid')},
            {'cname':'lostate',
             'cbyte':(idFromLine,('-',(charrange,(30,36)),
                                      (charrange,(122,124)),
                                      (charrange,(58,63)),
                                      (charrange,(124,170)),
                                      (charrange,(44,58)) )),
             'references':(valdmodel.State,'charid')},
            ],
    } # end of vald file def

] # end of vald3 mapping file def list
