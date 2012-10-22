#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The config file for importing the example_data dataset into
ExampleNode.

Go to http://vamdc.tmy.se/doc/importing.html
for understanding what happens below.

Use this file this way (first edit base path) :

$ cd ../imptools
$ python run_rewrite.py ../nodes/ExampleNode/mapping_examplenode.py

This will create the output files in the path defined below.

If you already have a compatible mysql database you can then import these
files directly with the ExampleNode/load.sql script (edit load.sql first
to have the right paths).

$ cd node/ExampleNode
$ mysql -u <databaseuser> -p < load.sql

"""

# import database libraries and helper methods
import os
from imptools.linefuncs import constant, bySepNr, charrange

# custom linefunctions for our example

def get_bibtex(linedata):
    "Return the raw data"
    return linedata

def get_bibtex_dbref(linedata):
    """
    Extract the dbref from the bibtex entry (e.g. REF1, REF2...)
    """
    first_line = linedata.split()[0]
    typ, dbref = first_line.split('{')
    return dbref.strip(',').strip()

def merge_cols_by_sep(linedata, *sepNr):
    """
    Merges data from several columns (separated by ,) into one, separating them with '-'.
    sepNr are the nth position of the file, separated by 'sep'.
    Assumes a single line input.
    """
    sep = ','
    return '-'.join([bySepNr(linedata, nr, sep=sep).strip() for nr in sepNr])


# Setting up filenames, finding current path as base
base = os.path.dirname(__file__) + os.path.sep
inbase = base + "example_data" + os.path.sep

# Raw indata files
species_list_file = inbase + 'species.dat'
publications_file = inbase + "references.dat"
transitions_file = inbase + 'transitions.dat'

# Parsed files intended for direct loading into database
species_out = base + 'species.in'
publications_out = base + 'references.in'
states_out = base + 'states.in'
transitions_out = base + 'transitions.in'

# The mapping itself
mapping = [
    # Populate Species model, using the species input file.
    # This file uses fixed collumns which we parse by line index.

    {'outfile':species_out,
     'infiles':species_list_file,
     'commentchar':'#',
     'headlines':1,
     'linemap':[
            {'cname':'id',
             'cbyte':(charrange, 0, 9)},
            {'cname':'name',
             'cbyte':(charrange, 10, 16),
             'cnull':'\N'},
            {'cname':'ion',
             'cbyte':(charrange, 17, 22),
             'cnull':'\N'},
            {'cname':'mass',
             'cbyte':(charrange, 23, 35),
             'cnull':'\N'},
            {'cname':'massno',
             'cbyte':(charrange, 36, 46),
             'cnull':'\N'},
            {'cname':'ionen_ev',
             'cbyte':(charrange, 47, 57),
             'cnull':'\N'},
            {'cname':'ionen_cm1',
             'cbyte':(charrange, 58, 70),
             'cnull':'\N'},
            {'cname':'atomic',
             'cbyte':(charrange, 71, 79),
             'cnull':'\N'},
            {'cname':'isotope',
             'cbyte':(charrange, 80, 87),
             'cnull':'\N'},
           ],
     }, # end of definition for species file

    # Populate Publication model with bibtex data file.  This file
    # contains bibtex block entries (we cannot parse each line
    # separately), so we need to define the possible start/end blocks
    # separating entries.

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

    # All states and transitions are stored in one file, where each
    # line contains all data for the transition:
    #
    # upper_state info   |   lower _state info   | transition info
    #
    # Each data unit is separated by ',',
    #
    # We parse this file three times to get the upper, lower and
    # transition information respectively. We must also create a
    # unique id for each state so that the transition can reference
    # the correct states properly
    #

    # State model read from transitions file - upper states
    # (first pass)
    {'outfile': states_out,
     'infiles': transitions_file,
     'commentchar': '#',
     'headlines':3,
     'linemap':[
            # creating a unique id hash by combining data from the
            {'cname':'id',        #species,coup,jnum,term,energy (upper states)
             'cbyte':(merge_cols_by_sep, 0, 4, 6, 5, 1),
             'cnull':'N/A'},
            {'cname':'species',
             'cbyte':(bySepNr, 0),
             'cnull':'N/A'},
            {'cname':'energy',
             'cbyte':(bySepNr, 1),
             'cnull':'N/A'},
            {'cname':'config',
             'cbyte':(bySepNr, 2),
             'cnull':'N/A'},
            {'cname':'lande',
             'cbyte':(bySepNr, 3),
             'cnull':'N/A'},
            {'cname':'coupling',
             'cbyte':(bySepNr, 4),
             'cnull':'N/A'},
            {'cname':'term',
             'cbyte':(bySepNr, 5),
             'cnull':'N/A'},
            {'cname':'j',
             'cbyte':(bySepNr,6),
             'cnull':'N/A'},
            {'cname':'l',
             'cbyte':(bySepNr,7),
             'cnull':'N/A'},
            {'cname':'s',
             'cbyte':(bySepNr,8),
             'cnull':'N/A'},
            {'cname':'p',
             'cbyte':(bySepNr,9),
             'cnull':'N/A'},
            {'cname':'j1',
             'cbyte':(bySepNr,10),
             'cnull':'N/A'},
            {'cname':'j2',
             'cbyte':(bySepNr,11),
             'cnull':'N/A'},
            {'cname':'k',
             'cbyte':(bySepNr,12),
             'cnull':'N/A'},
            {'cname':'s2',
             'cbyte':(bySepNr,13),
             'cnull':'N/A'},
            {'cname':'jc',
             'cbyte':(bySepNr,14),
             'cnull':'N/A'},

            # half-times
            {'cname':'tau_exp',
             'cbyte':(bySepNr,15),
             'cnull':'N/A'},
            {'cname':'tau_calc',
             'cbyte':(bySepNr,16),
             'cnull':'N/A'},
            {'cname':'tau_exp_ref',
             'cbyte':(bySepNr,17),
             'cnull':'N/A'},
            {'cname':'tau_calc_ref',
             'cbyte':(bySepNr,18),
             'cnull':'N/A'},

            {'cname':'energy_ref',
             'cbyte':(bySepNr, 19),
             'cnull':'N/A'},
            {'cname':'lande_ref',
             'cbyte':(bySepNr, 20),
             'cnull':'N/A'},
            {'cname':'level_ref',
             'cbyte':(bySepNr, 21),
             'cnull':'N/A'},
            ]
     }, # end of upper states

    # State model read from transitions file -lower states
    # (second pass)
    {'outfile': states_out,
     'infiles': transitions_file,
     'commentchar': '#',
     'headlines':3,
     'linemap':[
            {'cname':'id',        #species,coup,jnum,term,energy (lower states)
             'cbyte':(merge_cols_by_sep, 22, 26, 28, 27, 23),
             'cnull':'N/A'},
            {'cname':'species',
             'cbyte':(bySepNr, 22),
             'cnull':'N/A'},
            {'cname':'energy',
             'cbyte':(bySepNr, 23),
             'cnull':'N/A'},
            {'cname':'config',
             'cbyte':(bySepNr, 24), ##2
             'cnull':'N/A'},
            {'cname':'lande',
             'cbyte':(bySepNr, 25),
             'cnull':'N/A'},
            {'cname':'coupling',
             'cbyte':(bySepNr, 26),
             'cnull':'N/A'},
            {'cname':'term',
             'cbyte':(bySepNr, 27),
             'cnull':'N/A'},
            {'cname':'j',
             'cbyte':(bySepNr, 28),
             'cnull':'N/A'},
            {'cname':'l',
             'cbyte':(bySepNr,29),
             'cnull':'N/A'},
            {'cname':'s',
             'cbyte':(bySepNr,30),
             'cnull':'N/A'},
            {'cname':'p',
             'cbyte':(bySepNr,31),
             'cnull':'N/A'},
            {'cname':'j1',
             'cbyte':(bySepNr,32),
             'cnull':'N/A'},
            {'cname':'j2',
             'cbyte':(bySepNr,33),
             'cnull':'N/A'},
            {'cname':'k',
             'cbyte':(bySepNr,34),
             'cnull':'N/A'},
            {'cname':'s2',
             'cbyte':(bySepNr,35),
             'cnull':'N/A'},
            {'cname':'jc',
             'cbyte':(bySepNr,36),
             'cnull':'N/A'},

            # half-times
            {'cname':'tau_exp',
             'cbyte':(bySepNr,37),
             'cnull':'N/A'},
            {'cname':'tau_calc',
             'cbyte':(bySepNr,38),
             'cnull':'N/A'},
            {'cname':'tau_exp_ref',
             'cbyte':(bySepNr,39),
             'cnull':'N/A'},
            {'cname':'tau_calc_ref',
             'cbyte':(bySepNr,40),
             'cnull':'N/A'},

            {'cname':'energy_ref',
             'cbyte':(bySepNr, 41),
             'cnull':'N/A'},
            {'cname':'lande_ref',
             'cbyte':(bySepNr, 42),
             'cnull':'N/A'},
            {'cname':'level_ref',
             'cbyte':(bySepNr, 43),
             'cnull':'N/A'},
            ]
     }, # end of lower states


    # Transition model, from the transitions file
    # (third pass)
    {'outfile':transitions_out,
     'infiles':transitions_file,
     'commentchar':'#',
     'headlines':3,
     'linemap':[
            {'cname':'id',
             'cbyte':(constant, 'NULL'),
             'cnull':'NULL'},
            # here we recreate the same ids we used for the upper/lower states before
            {'cname':'upstate',
             'cbyte':(merge_cols_by_sep, 0, 4, 6, 5, 1),
             'cnull':'N/A'},
            {'cname':'lostate',
             'cbyte':(merge_cols_by_sep, 22, 26, 28, 27, 23),
             'cnull':'N/A'},
            {'cname':'vacwave',
             'cbyte':(bySepNr, 44),
             'cnull':'N/A'},
            {'cname':'species', # we pick this from the start of the line
             'cbyte':(bySepNr, 0),
             'cnull':'N/A'},
            {'cname':'loggf',
             'cbyte':(bySepNr, 45),
             'cnull':'N/A'},
            {'cname':'landeff',
             'cbyte':(bySepNr, 46),
             'cnull':'N/A'},
            {'cname':'gammarad',
             'cbyte':(bySepNr, 47),
             'cnull':'N/A'},
            {'cname':'gammastark',
             'cbyte':(bySepNr, 48),
             'cnull':'N/A'},
            {'cname':'gammawaals',
             'cbyte':(bySepNr, 49),
             'cnull':'N/A'},
            {'cname':'wave_accur',
             'cbyte':(bySepNr, 50),
             'cnull':'N/A'},
            {'cname':'loggf_accur',
             'cbyte':(bySepNr, 51),
             'cnull':'N/A'},
            {'cname':'comment',
             'cbyte':(bySepNr, 52),
             'cnull':'N/A'},
            {'cname':'wave_ref',
             'cbyte':(bySepNr, 53),
             'cnull':'N/A'},
            {'cname':'loggf_ref',
             'cbyte':(bySepNr, 54),
             'cnull':'N/A'},
            {'cname':'lande_ref',
             'cbyte':(bySepNr, 55),
             'cnull':'N/A'},
            {'cname':'gammarad_ref',
             'cbyte':(bySepNr, 56),
             'cnull':'N/A'},
            {'cname':'gammastark_ref',
             'cbyte':(bySepNr, 57),
             'cnull':'N/A'},
            {'cname':'waals_ref',
             'cbyte':(bySepNr, 58),
             'cnull':'N/A'},
            ],
    }, # end of transitions file reading
]
