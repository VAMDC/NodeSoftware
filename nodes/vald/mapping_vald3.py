#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The config file for importing VALD into a database.

Go to http://vamdc.tmy.se/doc/importing.html
for understanding what happens below.
"""
import os, sys

from imptools.linefuncs import *

# bibtex-reading helper functions

def get_bibtex(linedata):
    "return the raw data"
    return ' '.join(linedata.split())

def get_bibtex_dbref(linedata):
    "extract the dbref from the bibtex entry"
    first_line = linedata.split()[0]
    typ, dbref = first_line.split('{')
    return dbref.strip(',').strip()
    
# Setting up filenames
base = "/vald/"
species_list_file = base + 'VALD_list_of_species'
vald_cfg_file = base + 'VALD3.cfg'
vald_file = base + 'vald3.dat'
terms_file = base + 'terms'
ref_file = base + "VALD3_ref.bib"

# The mapping itself
mapping = [
    # Populate Species model, using the species input file.
    {'outfile':base + 'species.dat',
     'infiles':species_list_file,
     'headlines':0,
     'commentchar':'#',
     'linemap':[
            {'cname':'id',
             'cbyte':(charrange, 0,7)},
            {'cname':'name',
             'cbyte':(charrange, 9,19)},
            {'cname':'inchi',
             'cbyte':(constant, 'NULL'),
             'cnull':'NULL'},
            {'cname':'inchikey',
             'cbyte':(constant, 'NULL'),
             'cnull':'NULL'},
            {'cname':'ion',
             'cbyte':(charrange, 20,22)},
            {'cname':'mass',
             'cbyte':(charrange, 23,30)},
            {'cname':'massno',
             'cbyte':(charrange2int, 23,30)},
            {'cname':'ionen',
             'cbyte':(charrange, 31,40)},
            {'cname':'solariso',
             'cbyte':(charrange, 41,47)},
            {'cname':'dissen',
             'cbyte':(charrange, 48,57)},            
            {'cname':'ncomp',
             'cbyte':(charrange, 132,133)},
            {'cname':'atomic',
             'cbyte':(charrange, 134,136)},
            {'cname':'isotope',
             'cbyte':(charrange, 137,140)},
            # many2many field "species" handled by separate table
            ],
     }, # end of definition for species file
    
    # State model read 2 lines at a time from vald3 main file
    # term files are grouped with 3 lines for every 2 line in the 
    # vald file - lower, upper, transition_info

    # States output file appended with lower states
    {'outfile':base + 'states.dat',
     'infiles':(vald_file, vald_file, terms_file, terms_file),
     'headlines':(2, 2, 0, 0), 
     'commentchar':('#','#','#','#'),
     'linestep':(2, 2, 3, 3),   # step lengh in each file
     'lineoffset':(0, 1, 0, 2), # start point of step in each file
     'errline':("Unknown", "Unknown", "Unknown", "Unknown"),
     'linemap':[
            {'cname':'charid',         #species,coup,jnum,term,energy (lower states) 
             'cbyte':(merge_cols,
                      (30,36), (124,126), (58,64), (126,212), (44,58))},
            {'cname':'species',
             'cbyte':(charrange, 30,36)},
            {'cname':'energy',
             'cbyte':(charrange, 44,58)},
            #{'cname':'j',
            # 'cbyte':(charrange, 58,63)},
            {'cname':'lande',
             'cbyte':(charrange, 86,92),
             'cnull':'99.00'},
            {'cname':'coupling',
             'cbyte':(charrange, 124,126)},
            {'cname':'term',
             'cbyte':(charrange, 126,212)},

            # read from 2nd open vald file (2nd line per record)
            {'filenum':1,
             'cname':'energy_ref',
             'cbyte':(charrange, 17,25)},
             #'references':(models.Source,'pk')},
            {'filenum':1,
             'cname':'lande_ref',
             'cbyte':(charrange, 33,41)},
             #'references':(models.Source,'pk')},
            {'filenum':1,
             'cname':'level_ref',
             'cbyte':(charrange, 65,73)},


            ## this links to linelists rather than refs directly
            #{'cname':'energy_ref',
            # 'cbyte':(charrange, 264,268)},
            # #'references':(models.Source,'pk')},
            #{'cname':'lande_ref',
            # 'cbyte':(charrange, 268,272)},
            # #'references':(models.Source,'pk')},
            #{'cname':'level_ref',
            # 'cbyte':(charrange, 284,288)},
            #'references':(models.Source,'pk')},

            # these are read from 1st open term file
            {'filenum':2, # use term file
             'cname':'j',
             'cbyte':(get_term_val,'J'),           
             'cnull':'X',},
            {'filenum':2, # use term file
             'cname':'l',
             'cbyte':(get_term_val,'L'),
             'cnull':'X',},
            {'filenum':2, # use term file
             'cname':'s',
             'cbyte':(get_term_val,'S'),
             'cnull':'X',},
            {'filenum':2, # use term file
             'cname':'p',
             'cbyte':(get_term_val,'parity'),
             'cnull':'X',},
            {'filenum':2, # use term file
             'cname':'j1',
             'cbyte':(get_term_val,'J1'),
             'cnull':'X',},
            {'filenum':2, # use term file
             'cname':'j2',
             'cbyte':(get_term_val,'J2'),
             'cnull':'X',},
            {'filenum':2, # use term file
             'cname':'k',
             'cbyte':(get_term_val,'K'),
             'cnull':'X',},
            {'filenum':2, # use term file
             'cname':'s2',
             'cbyte':(get_term_val,'S2'),
             'cnull':'X',},
            {'filenum':2, # use term file
             'cname':'jc',
             'cbyte':(get_term_val,'Jc'),
             'cnull':'X',},
            {'filenum':2, # use term file
             'cname':'sn',             
             'cbyte':(get_term_val,'seniority'),
             'cnull':'X',},            

            # read extra info from 2nd open term file
            {'filenum':3, # use 2nd open term file
             'cname':'transition_type',             
             'cbyte':(get_term_transtype,'ttype'),
             'cnull':'X',},                        
            {'filenum':3, # use 2nd open term file
             'cname':'autoionized',             
             'cbyte':(get_term_transtype,'autoio'),
             'cnull':'X',},                        
            ]
     }, # end of State model creation - lower states

    # upper states  
    {'outfile':base + 'states.dat',    
     'infiles': (vald_file, vald_file, terms_file, terms_file),
     'headlines':(2, 2, 0, 0),
     'commentchar': ('#', '#', '#','#'),
     'linestep':(2, 2, 3, 3),
     'lineoffset':(0, 1, 1, 2), # start point of step
     'errline':("Unknown", "Unknown","Unknown"),
     'linemap':[
            {'cname':'charid',        #species,coup,jnum,term,energy (upper states)             
             'cbyte':(merge_cols,
                      (30,36), (212,214), (78,84), (214,300), (63,77))}, 
            {'cname':'species',
             'cbyte':(charrange, 30,36)},
            {'cname':'energy',
             'cbyte':(charrange, 63,77)},
            #{'cname':'j',   
            # 'cbyte':(charrange, 77,82),},
            {'cname':'lande',
             'cbyte':(charrange, 92,96),
             'cnull':'99.00'},
            {'cname':'coupling',
             'cbyte':(charrange, 212,214)},
            {'cname':'term',
             'cbyte':(charrange, 214,300)},

            # read from 2nd open vald file (2nd line per record)
            {'filenum':1,
             'cname':'energy_ref',
             'cbyte':(charrange, 25,33)},
             #'references':(models.Source,'pk')},
            {'filenum':1,
             'cname':'lande_ref',
             'cbyte':(charrange, 33,41)},
             #'references':(models.Source,'pk')},
            {'filenum':1,
             'cname':'level_ref',
             'cbyte':(charrange, 65,73)},

            ## links to linelist rather than reference directly
            #{'cname':'energy_ref',
            # 'cbyte':(charrange, 264,268)},
            # #'references':(models.Source,'pk')},
            #{'cname':'lande_ref',
            # 'cbyte':(charrange, 268,272)},
            # #'references':(models.Source,'pk')},
            #{'cname':'level_ref',
            # 'cbyte':(charrange, 284,288)},
            # #'references':(models.Source,'pk')},
            
            # these are read from term file
            {'cname':'j',
             'filenum':2, # use term file
             'cbyte':(get_term_val,'J'),
             'cnull':'X',},
            {'cname':'l',
             'filenum':2, # use term file
             'cbyte':(get_term_val,'L'),
             'cnull':'X',},
            {'cname':'s',
             'filenum':2, # use term file
             'cbyte':(get_term_val,'S'),
             'cnull':'X',},
            {'cname':'p',
             'filenum':2, # use term file
             'cbyte':(get_term_val,'parity'), 
             'cnull':'X',}, 
            {'cname':'j1',
             'filenum':2, # use term file
             'cbyte':(get_term_val,'J1'),
             'cnull':'X',},
            {'cname':'j2',
             'filenum':2, # use term file
             'cbyte':(get_term_val,'J2'),
             'cnull':'X',},
            {'cname':'k',
             'filenum':2, # use term file
             'cbyte':(get_term_val,'K'),
             'cnull':'X',},
            {'cname':'s2',
             'filenum':2, # use term file
             'cbyte':(get_term_val,'S2'),
             'cnull':'X',},
            {'cname':'jc',
             'filenum':2, # use term file
             'cbyte':(get_term_val,'Jc'),
             'cnull':'X',},
            {'cname':'sn',
             'filenum':2, # use term file
             'cbyte':(get_term_val,'seniority'),
             'cnull':'X',},            
            # read extra info from every third line in term file
            {'filenum':3, # use 2nd open term file
             'cname':'transition_type',             
             'cbyte':(get_term_transtype,'ttype'),
             'cnull':'X',},                        
            {'filenum':3, # use 2nd open term file
             'cname':'autoionized',             
             'cbyte':(get_term_transtype,'autoio'),
             'cnull':'X',},                        
            ]
     }, # end of upper states
       
    # Transition model, using the vald file    
    {'outfile': base + 'transitions.dat',
     'infiles':(vald_file,vald_file),
     'headlines':(2,2),
     'commentchar':('#','#'),
     'linestep':(2,2),
     'lineoffset':(0,1),
     'linemap':[
            {'cname':'id',
             'cbyte':(constant, 'NULL'),
             'cnull':'NULL'},
            {'cname':'upstate',
             'cbyte':(merge_cols,
                      (30,36), (212,214), (78,84), (214,300), (63,77))}, 
                       #(30,36), (170,172), (77,82), (172,218), (63,77))},
            {'cname':'lostate',
             'cbyte':(merge_cols,
                      (30,36), (124,126), (58,64), (126,212), (44,58))},
                      #(30,36), (122,124), (58,63), (124,170), (44,58))},
            {'cname':'vacwave',
             'cbyte':(charrange, 0,15)},
            {'cname':'airwave',
             'cbyte':(charrange, 15,30)},
            {'cname':'species',
             'cbyte':(charrange, 30,36)},
            {'cname':'loggf',
             'cbyte':(charrange, 36,44)},
            # removed since it can be reconstructed from upper/lower state anyway
            #{'cname':'landeff',
            # 'cbyte':(charrange, 96,102), # lande combined for upper/lower level
            # 'cnull':'99.00'},
            {'cname':'gammarad',
             'cbyte':(charrange, 102,109),
             'cnull':'0.0'},
            {'cname':'gammastark',
             'cbyte':(charrange, 109,116),
             'cnull':'0.000'},            
            {'cname':'gammawaals',
             'cbyte':(get_gammawaals, 116,124),
             'cnull':'0.000',
             'debug':False},
            {'cname':'sigmawaals', # only filled if raw value > 0.  
             'cbyte':(get_sigmawaals, 116,124),
             'cnull':'0.000',
             'debug':False},
            {'cname':'alphawaals',
             'cbyte':(get_alphawaals, 116,124),
             'cnull':'0.000',
             "debug":False},
            {'cname':'accur',
             'cbyte':(get_accur, (307,308), (308,314)),
             'debug':False},
            {'cname':'comment',
             'cbyte':(charrange, 318,334)},
            {'cname':'srctag',
             'cbyte':(charrange, 300,307),
             'skiperror':True},             
            
            # read from every second line of the vald file
            {'filenum':1,
             'cname':'wave_ref',             
             'cbyte':(charrange, 0,9)},
            {'filenum':1,
             'cname':'loggf_ref',       
             'cbyte':(charrange, 9,17)},
            # removed - see comment about lande factor above
            #{'filenum':1,
            # 'cname':'lande_ref',
            # 'cbyte':(charrange, 33,41)},
            {'filenum':1,
             'cname':'gammarad_ref',
             'cbyte':(charrange, 41,49)},
            {'filenum':1,
             'cname':'gammastark_ref',
             'cbyte':(charrange, 49,57)},
            {'filenum':1,
             'cname':'waals_ref',  
             'cbyte':(charrange, 57,65)},
            ## These are the old connections to linelists rather than refs directly
            #{'cname':'wave_ref',             
            # 'cbyte':(charrange, 252,256)},
            #{'cname':'loggf_ref',
            # 'cbyte':(charrange, 256,260)},
            #{'cname':'lande_ref',
            # 'cbyte':(charrange, 268,272)},
            #{'cname':'gammarad_ref',
            # 'cbyte':(charrange, 272,276)},
            #{'cname':'gammastark_ref',
            # 'cbyte':(charrange, 276,280)},
            #{'cname':'waals_ref',  
            # 'cbyte':(charrange, 280,284)},
            ],
    }, # end of transitions

    # Populate References with bibtex data file (block parsing)
    {'outfile':base + 'references.dat',    
     'infiles':ref_file,
     'headlines':0,        
     'commentchar':'%',
     'startblock':('@article','@book','@techreport','@inproceedings','@misc','@ARTICLE','@phdthesis','@unpublished'),
     'endblock':('@article','@book','@techreport','@inproceedings','@misc','@ARTICLE','@phdthesis','@unpublished'),
     'linemap':[           
            {'cname':'dbref',
             'cbyte':(get_bibtex_dbref,)},
            {'cname':'bibtex',
             'cbyte':(get_bibtex,)}, 
          ], 
      }, # end of bibtex 
    
    # Populate LineList model from vald_cfg file
    {'outfile': base + 'linelists.dat',
     'infiles':vald_cfg_file,
     'headlines':1,
     'commentchar':';',
     'linemap':[
            {'cname':'id',
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
    
    

    ]

#mapping = [mapping[-2]]
