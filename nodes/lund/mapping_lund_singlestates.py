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

def bySepNr(linedata, number):
    "parse by separator"
    return string.split(linedata, ';')[number].strip()
        
# Setting up filenames
base = "/home/griatch/Devel/Work/VAMDC-git/nodes/lund/"
states_file = base + 'singlestates.dat'
states_out = base + 'singlestates.out'

# The mapping itself
mapping = [
    # State model read from single-state file
    {'outfile': states_out,    
     'infiles': states_file,
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
]
