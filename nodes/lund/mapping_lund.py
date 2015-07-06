#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The config file for importing Lund data into a database.

Go to http://vamdc.tmy.se/doc/importing.html
for understanding what happens below.
"""

import string
from imptools.linefuncs import merge_cols_by_sep, constant

# reading helper functions

def get_bibtex(linedata):
    "return the raw data"
    return linedata
def get_bibtex_dbref(linedata):
    "extract the dbref from the bibtex entry"
    first_line = linedata.split()[0]
    typ, dbref = first_line.split('{')
    return dbref.strip(',').strip()

def bySepNr(linedata, number):
    "parse by separator"
    return string.split(linedata, ';')[number].strip()
        
def convert_wave(linedata, to_type="wacwave"):
    """
    Convert wavenum/wacwave/airwave data. to_type
    is either wavenum, wacwave or airwave. Data from
    one of the other two types are used to fill
    in the the other, if applicable.
    """
    wacwave = bySepNr(linedata, 54)
    wavenum = bySepNr(linedata, 55)
    airwave = bySepNr(linedata, 56)
    
    if to_type=='wacwave':
        if wacwave != '\N': return float(wacwave)
        if wavenum != '\N': return 10**8 / float(wavenum)
        # skipping airwave for now
    elif to_type=='wavenum':
        if wavenum != '\N': return float(wavenum)
        if wacwave != '\N': return 10**8 / float(wacwave)
    elif to_type == 'airwave':
        return airwave # this needs to be fixed with correct formula
        

# Setting up filenames
base = "/home/vamdc/NodeSoftware/nodes/lund/"
outbase = base + "db_indata/"
species_list_file = base + 'species.dat'
publications_file = base + "references.dat"
transitions_file = base + 'transitions.dat'
species_out = outbase + 'species.in'
publications_out = outbase + 'references.in'
states_out = outbase + 'states.in'
transitions_out = outbase + 'transitions.in'

# The mapping itself
mapping = [
    # Populate Species model, using the species input file.
    {'outfile':species_out,
     'infiles':species_list_file,
     'commentchar':'#',
     'headlines':1,
     'linemap':[
            {'cname':'id',
             'cbyte':(bySepNr, 0)},
            {'cname':'name',
             'cbyte':(bySepNr, 1),
             'cnull':'\N'},
            {'cname':'ion',
             'cbyte':(bySepNr, 2),
             'cnull':'\N'},
            {'cname':'mass',
             'cbyte':(bySepNr, 3),
             'cnull':'\N'},
            {'cname':'massno',
             'cbyte':(bySepNr, 4),
             'cnull':'\N'},
            {'cname':'ionen_ev',
             'cbyte':(bySepNr, 5),
             'cnull':'\N'},
            {'cname':'ionen_cm1',
             'cbyte':(bySepNr, 6),
             'cnull':'\N'},
            {'cname':'atomic',
             'cbyte':(bySepNr, 7),
             'cnull':'\N'},
            {'cname':'isotope',
             'cbyte':(bySepNr, 8),
             'cnull':'\N'},
           ],
     }, # end of definition for species file

    # Populate Publication model with bibtex data file (block parsing)
    {'outfile':publications_out,    
     'infiles':publications_file,
     'headlines':0,        
     'commentchar':'%',
     'startblock':('@article','@book','@techreport','@inproceedings','@misc','@ARTICLE'),
     'endblock':('@article','@book','@techreport','@inproceedings','@misc','@ARTICLE'),
     'linemap':[           
            {'cname':'dbref',
             'cbyte':(get_bibtex_dbref,)},
            {'cname':'bibtex',
             'cbyte':(get_bibtex,)}, 
            ], 
     }, # end of bibtex publication data

    # State model read from transitions file -upper states
    # (first section) 
    {'outfile': states_out,    
     'infiles': transitions_file,
     'commentchar': '#',
     'headlines':3,
     'linemap':[
            {'cname':'id',        #species,coup,jnum,term,energy (upper states)             
             'cbyte':(merge_cols_by_sep, 0, 4, 6, 5, 1),
             'cnull':'\N'},
            {'cname':'species',
             'cbyte':(bySepNr, 0),
             'cnull':'\N'},
            {'cname':'energy',
             'cbyte':(bySepNr, 1),
             'cnull':'\N'},
            {'cname':'config',
             'cbyte':(bySepNr, 2), ##1
             'cnull':'\N'},
            {'cname':'lande',
             'cbyte':(bySepNr, 3),
             'cnull':'\N'},
            {'cname':'coupling',
             'cbyte':(bySepNr, 4),
             'cnull':'\N'},
            {'cname':'term',
             'cbyte':(bySepNr, 5),
             'cnull':'\N'},
            {'cname':'j',
             'cbyte':(bySepNr,6),
             'cnull':'\N'},
            {'cname':'l',
             'cbyte':(bySepNr,7),
             'cnull':'\N'},
            {'cname':'s',
             'cbyte':(bySepNr,8),
             'cnull':'\N'},
            {'cname':'p',
             'cbyte':(bySepNr,9),
             'cnull':'\N'},
            {'cname':'j1',
             'cbyte':(bySepNr,10),
             'cnull':'\N'},
            {'cname':'j2',
             'cbyte':(bySepNr,11),
             'cnull':'\N'},
            {'cname':'k',
             'cbyte':(bySepNr,12),
             'cnull':'\N'},
            {'cname':'s2',
             'cbyte':(bySepNr,13),
             'cnull':'\N'},
            {'cname':'jc',
             'cbyte':(bySepNr,14),
             'cnull':'\N'},
            {'cname':'f_hfs',
             'cbyte':(bySepNr,15),
             'cnull':'\N'},

            # hyperfine structure
            {'cname':'hfs_a',
             'cbyte':(bySepNr,16),
             'cnull':'\N'},
            {'cname':'hfs_b',
             'cbyte':(bySepNr,17),
             'cnull':'\N'},
            {'cname':'hfs_accur',
             'cbyte':(bySepNr,18),
             'cnull':'\N'},
            {'cname':'hfs_ref',
             'cbyte':(bySepNr,19),
             'cnull':'\N'},

            # half-times
            {'cname':'tau_exp',
             'cbyte':(bySepNr,20),
             'cnull':'\N'},
            {'cname':'tau_calc',
             'cbyte':(bySepNr,21),
             'cnull':'\N'},
            {'cname':'tau_accur',
             'cbyte':(bySepNr,22),
             'cnull':'\N'},
            {'cname':'tau_exp_ref', 
             'cbyte':(bySepNr,23),
             'cnull':'\N'},
            {'cname':'tau_calc_ref',
             'cbyte':(bySepNr,24),
             'cnull':'\N'},
                        
            {'cname':'energy_ref',
             'cbyte':(bySepNr, 25),
             'cnull':'\N'},
            {'cname':'lande_ref',
             'cbyte':(bySepNr, 26),
             'cnull':'\N'},
            {'cname':'level_ref',
             'cbyte':(bySepNr, 27),
             'cnull':'\N'},
            ]
     }, # end of upper states

    # State model read from transitions file -lower states
    # (second section) 
    {'outfile': states_out,    
     'infiles': transitions_file,
     'commentchar': '#',
     'headlines':3,
     'linemap':[
            {'cname':'id',        #species,coup,jnum,term,energy (lower states)             
             'cbyte':(merge_cols_by_sep, 28, 32, 34, 33, 29),
             'cnull':'\N'},
            {'cname':'species',
             'cbyte':(bySepNr, 28),
             'cnull':'\N'},
            {'cname':'energy',
             'cbyte':(bySepNr, 29),
             'cnull':'\N'},
            {'cname':'config',
             'cbyte':(bySepNr, 30), ##2
             'cnull':'\N'},
            {'cname':'lande',
             'cbyte':(bySepNr, 31),
             'cnull':'\N'},
            {'cname':'coupling',
             'cbyte':(bySepNr, 32),
             'cnull':'\N'},
            {'cname':'term',
             'cbyte':(bySepNr, 33),
             'cnull':'\N'},
            {'cname':'j',
             'cbyte':(bySepNr, 34),
             'cnull':'\N'},
            {'cname':'l',
             'cbyte':(bySepNr,35),
             'cnull':'\N'},
            {'cname':'s',
             'cbyte':(bySepNr,36),
             'cnull':'\N'},
            {'cname':'p',
             'cbyte':(bySepNr,37),
             'cnull':'\N'},
            {'cname':'j1',
             'cbyte':(bySepNr,38),
             'cnull':'\N'},
            {'cname':'j2',
             'cbyte':(bySepNr,39),
             'cnull':'\N'},
            {'cname':'k',
             'cbyte':(bySepNr,40),
             'cnull':'\N'},
            {'cname':'s2',
             'cbyte':(bySepNr,41),
             'cnull':'\N'},
            {'cname':'jc',
             'cbyte':(bySepNr,42),
             'cnull':'\N'},
            {'cname':'f_hfs',
             'cbyte':(bySepNr,43),
             'cnull':'\N'},

            # hyperfine structure
            {'cname':'hfs_a',
             'cbyte':(bySepNr,44),
             'cnull':'\N'},
            {'cname':'hfs_b',
             'cbyte':(bySepNr,45),
             'cnull':'\N'},
            {'cname':'hfs_accur',
             'cbyte':(bySepNr,46),
             'cnull':'\N'},
            {'cname':'hfs_ref',
             'cbyte':(bySepNr,47),
             'cnull':'\N'},

            # half-times
            {'cname':'tau_exp',
             'cbyte':(bySepNr,48),
             'cnull':'\N'},
            {'cname':'tau_calc',
             'cbyte':(bySepNr,48),
             'cnull':'\N'},
            {'cname':'tau_accur',
             'cbyte':(bySepNr,49),
             'cnull':'\N'},
            {'cname':'tau_exp_ref',
             'cbyte':(bySepNr,50),
             'cnull':'\N'},
            {'cname':'tau_calc_ref',
             'cbyte':(bySepNr,50),
             'cnull':'\N'},
                        
            {'cname':'energy_ref',
             'cbyte':(bySepNr, 51),
             'cnull':'\N'},
            {'cname':'lande_ref',
             'cbyte':(bySepNr, 52),
             'cnull':'\N'},
            {'cname':'level_ref',
             'cbyte':(bySepNr, 53),
             'cnull':'\N'},
            ]
     }, # end of lower states
    
   
    # Transition model, from the transitions file 
    # (third section)
    {'outfile':transitions_out,
     'infiles':transitions_file,
     'commentchar':'#',
     'headlines':3,
     'linemap':[
            {'cname':'id',
             'cbyte':(constant, 'NULL'),
             'cnull':'NULL'},
            {'cname':'upstate',
             'cbyte':(merge_cols_by_sep, 0, 4, 6, 5, 1),
             'cnull':'\N'},
            {'cname':'lostate',
             'cbyte':(merge_cols_by_sep, 28, 32, 34, 33, 29),
             'cnull':'\N'},
            {'cname':'vacwave',
             'cbyte':(convert_wave, "wacwave"), #pos 54
             'cnull':'\N'},
            {'cname':'wavenum',
             'cbyte':(convert_wave, "wavenum"), #pos 55
             'cnull':'\N'},            
            {'cname':'airwave',
             'cbyte':(convert_wave, "airwave"), #pos 56
             'cnull':'\N'},
            {'cname':'species',
             'cbyte':(bySepNr, 0),
             'cnull':'\N'},
            {'cname':'loggf',
             'cbyte':(bySepNr, 57),
             'cnull':'\N'},
            {'cname':'loggf_method',
             'cbyte':(bySepNr, 58),
             'cnull':'\N'},
            {'cname':'landeff',
             'cbyte':(bySepNr, 59),
             'cnull':'\N'},
            {'cname':'gammarad',
             'cbyte':(bySepNr, 60),
             'cnull':'\N'},
            {'cname':'gammastark',
             'cbyte':(bySepNr, 61),
             'cnull':'\N'},
            {'cname':'gammawaals',
             'cbyte':(bySepNr, 62),
             'cnull':'\N'},
            {'cname':'wave_accur',
             'cbyte':(bySepNr, 63),
             'cnull':'\N'},
            {'cname':'loggf_accur',
             'cbyte':(bySepNr, 64),
             'cnull':'\N'},
            {'cname':'comment',
             'cbyte':(bySepNr, 65),
             'cnull':'\N'}, 
            {'cname':'transition_ref',
             'cbyte':(bySepNr, 66),
             'cnull':'\N'},
            {'cname':'wave_ref',             
             'cbyte':(bySepNr, 67),
             'cnull':'\N'}, 
            {'cname':'loggf_ref', 
             'cbyte':(bySepNr, 68),
             'cnull':'\N'}, 
            {'cname':'lande_ref',
             'cbyte':(bySepNr, 69),
             'cnull':'\N'}, 
            {'cname':'gammarad_ref',
             'cbyte':(bySepNr, 70),
             'cnull':'\N'}, 
            {'cname':'gammastark_ref',
             'cbyte':(bySepNr, 71),
             'cnull':'\N'}, 
            {'cname':'waals_ref',  
             'cbyte':(bySepNr, 72),
             'cnull':'\N'}, 
            ],
    }, # end of transitions file reading
]
