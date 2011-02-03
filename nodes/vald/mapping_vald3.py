#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The config file for importing VALD into a database.

Go to http://vamdc.tmy.se/doc/importing.html
for understanding what happens below.
"""
import os, sys

from imptools.linefuncs import *


# Setting up filenames
base = "/vald/"
species_list_file = base + 'VALD_list_of_species'
vald_cfg_file = base + 'VALD3_config_2010.cfg'
vald_file = base + 'vald3.dat'
terms_file = base + 'terms'
publications_file = base + "publications_preprocessed.dat"
pub2source_file = base + "publications_to_sources_map.dat"

# The mapping itself
mapping = [
    # Populate Species model, using the species input file.
    {'outfile':'species.dat',
     'infiles':species_list_file,
     'headlines':0,
     'commentchar':'#',
     'linemap':[
            {'cname':'id',
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


# State model read from states_file -upper states
    # (first section) 
    {'outfile':'states.dat',    
     'infiles': (vald_file, terms_file),
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
             'cbyte':(charrange, 30,36)},
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
             'cbyte':(get_term_val,1),
             'cnull':'X',},
            {'cname':'l',
             'filenum':1, # use term file
             'cbyte':(get_term_val,2),
             'cnull':'X',},
            {'cname':'s',
             'filenum':1, # use term file
             'cbyte':(get_term_val,3),
             'cnull':'X',},
            {'cname':'p',
             'filenum':1, # use term file
             'cbyte':(get_term_val,4),
             'cnull':'X',},
            {'cname':'j1',
             'filenum':1, # use term file
             'cbyte':(get_term_val,5),
             'cnull':'X',},
            {'cname':'j2',
             'filenum':1, # use term file
             'cbyte':(get_term_val,6),
             'cnull':'X',},
            {'cname':'k',
             'filenum':1, # use term file
             'cbyte':(get_term_val,7),
             'cnull':'X',},
            {'cname':'s2',
             'filenum':1, # use term file
             'cbyte':(get_term_val,8),
             'cnull':'X',},
            {'cname':'jc',
             'filenum':1, # use term file
             'cbyte':(get_term_val,9),
             'cnull':'X',},
            ]
     }, # end of State-model creation - upper states
    
    # State model read from states_file - lower states
    # (second section)
    {'outfile':'states2.dat',
     'infiles':(vald_file, terms_file),
     'headlines':(2, 0), 
     'commentchar':('#','#'),
     'linestep':(1, 2),     
     'errline':("Unknown", "Unknown"),
     'linemap':[
            {'cname':'charid',         #species,coup,jnum,term,energy (lower states) 
             'cbyte':(merge_cols,
                      (30,36), (122,124), (58,63), (124,170), (44,58))},
            {'cname':'species',
             'cbyte':(charrange, 30,36)},
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
             'cbyte':(get_term_val,1),           
             'cnull':'X',},
            {'cname':'l',
             'cbyte':(get_term_val,2),
             'cnull':'X',},
            {'cname':'s',
             'cbyte':(get_term_val,3),
             'cnull':'X',},
            {'cname':'p',
             'cbyte':(get_term_val,4),
             'cnull':'X',},
            {'cname':'j1',
             'cbyte':(get_term_val,5),
             'cnull':'X',},
            {'cname':'j2',
             'cbyte':(get_term_val,6),
             'cnull':'X',},
            {'cname':'k',
             'cbyte':(get_term_val,7),
             'cnull':'X',},
            {'cname':'s2',
             'cbyte':(get_term_val,8),
             'cnull':'X',},
            {'cname':'jc',
             'cbyte':(get_term_val,9),
             'cnull':'X',},
            ]
     }, # end of State model creation - lower states
   
    # Transition model, using the vald file    
    {'outfile':'transitions.dat',
     'infiles':vald_file,
     'headlines':2,
     'commentchar':'#',
     'linemap':[
            {'cname':'id',
             'cbyte':(constant, 'NULL'),
             'cnull':'NULL'},
            {'cname':'vacwave',
             'cbyte':(charrange, 0,15)},
            {'cname':'airwave',
             'cbyte':(charrange, 15,30)},
            {'cname':'species',
             'cbyte':(charrange, 30,36)},
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
             'skiperror':True},             
            {'cname':'accur',
             'cbyte':(get_accur, (225,226), (226,236)),
             'debug':False},
            {'cname':'comment',
             'cbyte':(charrange, 236,252)},
            {'cname':'wave_ref',             
             'cbyte':(charrange, 252,256)},
            {'cname':'loggf_ref',
             'cbyte':(charrange, 256,260)},
            {'cname':'lande_ref',
             'cbyte':(charrange, 268,272)},
            {'cname':'gammarad_ref',
             'cbyte':(charrange, 272,276)},
            {'cname':'gammastark_ref',
             'cbyte':(charrange, 276,280)},
            {'cname':'waals_ref',  
             'cbyte':(charrange, 280,284)},
            {'cname':'upstateid',
             'cbyte':(merge_cols,
                      (30,36), (170,172), (77,82), (172,218),(63,77))},
            {'cname':'lostateid',
             'cbyte':(merge_cols,
                      (30,36), (122,124), (58,63), (124,170), (44,58))},
            {'cname':'upstate',
             'cbyte':(merge_cols,
                      (30,36), (170,172), (77,82), (172,218), (63,77))},
            {'cname':'lostate',
             'cbyte':(merge_cols,
                      (30,36), (122,124), (58,63), (124,170), (44,58))},
            ],
    }, # end of transitions


######### REFERENCES START HERE

    # Populate Publication model with pre-processed bibtex data file
    {'outfile':'publications.dat',    
     'infiles':publications_file,
     'headlines':0,        
     'commentchar':'#',    
     'linemap':[           
            {'cname':'dbref',
             'cbyte':(bySepNr, 0,'||')},
            {'cname':'bibref',
             'cbyte':(bySepNr, 1,'||')},  
            {'cname':'title',
             'cbyte':(bySepNr, 3,'||')},  
            {'cname':'author',
             'cbyte':(bySepNr, 2,'||')},  
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
    {'outfile':'sources.dat',
     'infiles':vald_cfg_file,
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
             'cbyte':(bySepNr, 2)},
            {'cname':'spechi',
             'cbyte':(bySepNr, 3)},
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
    {'outfile':'sources_publ.dat',
     'infiles':pub2source_file,
     'headlines':3,
     'commentchar':'#',
     'updatematch': 'srcfile_ref',
     'linemap':[
            {'cname':'srcfile_ref',
             'cbyte':(bySepNr, 1,'||'),
             'debug':False},
            {'cname':'publications',
             'cbyte':(get_publications, ), # must return a list!
#             'multireferences':(models.Publication, 'dbref'),
             'debug':False}
             ]
    },


]

mapping=mapping[0:4]
