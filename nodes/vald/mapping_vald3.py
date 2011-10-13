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
base = "/vald/vamdc/raw_vald_data/"
species_list_file = base + 'VALD_list_of_species'
vald_cfg_file = base + 'VALD3.cfg'
vald_file = base + 'vald3_atoms.dat.gz' # change to vald3_molec.dat.gz for molecules
terms_file = base + 'term_atoms.dat.gz'
ref_file = base + "VALD3_ref.bib"
linelist_file = base + "VALD3linelists.txt"
outbase = "/vald/vamdc/db_input_files/"


# helper functions

def get_bibtex(linedata):
    "return the raw data"
    return ' '.join(linedata.split())

def get_bibtex_dbref(linedata):
    "extract the dbref from the bibtex entry"
    first_line = linedata.split()[0]
    typ, dbref = first_line.split('{')
    return dbref.strip(',').strip()

def parse_linelist_file(filename):
    """
    Helper method for parsing the vald3 linelist wiki file into
    a dictionary of entries. This is the only way to propely
    match certain properties of linelists that are only present
    in this list. Note that no correction for doublet linelist
    matches are done here.
    """
    f = open(filename, 'r')
    dic = {}
    for line in f:
        if not line.startswith('||'):
            continue
        cols = line.split('||')[1:]
        if not cols[0].strip() or  not cols[0].strip()[0].isalnum():
            continue
        fil = cols[0].strip() # the file name identifier
        elements = cols[1].strip()
        typ = cols[2].strip()
        try:
            refs = [element.strip().strip(']]').strip().split('|')[1] for element in cols[3].split(',') if element.strip()]
        except IndexError:
            pass
        dic[fil] = (elements, typ, refs)
    return dic
LINELIST_DICT = parse_linelist_file(base + "VALD3linelists.txt")

# obs/exp - transition between levels with experimentally known energies
# emp - relativistic Hartree-Fock calculations, normalized to the experimental lifetimes
# pred - transitions between predicted energy levels
# calc - relativistic Hartree-Fock calculations of lifetimes and transition probabilities
# mix - mixture of observation times
METHOD_DICT = {'exp':0, 'obs':1, 'emp':2, 'pred':3, 'calc':4, 'mix':5}

def get_method_type(linedata):
    """
    Extract linedata and compare with pre-cached dictionary of linelists.
    """
    global LINELIST_DICT, OBSTYPE_DICT
    file_ref = get_srcfile_ref(linedata, 0, 3)
    entry = LINELIST_DICT.get(file_ref, None)
    if entry:
        return METHOD_DICT.get(entry[1], 'X') # the type
    else:
        return 'X'

def charrange_atom(linedata, molid, ia, ib):
    """
    This method is to be used to read species data.
    It returns data only if the species currently worked on
    is an atom and not a molecule. Otherwise return 'X'
     molid - minimum species id for species to be a molecule
     ia,ib - index1, index2
    """
    if charrange2int(linedata, 0, 7) < molid:
        return charrange(linedata, ia, ib)
    return 'X'

# The mapping itself
mapping = [
    # Populate Species model, using the species input file.
    {'outfile':outbase + 'species.dat',
     'infiles':species_list_file,
     'headlines':16,
     'commentchar':'#',
     'linemap':[
            {'cname':'id',
             'cbyte':(charrange, 0,7)},
            {'cname':'name',
             'cbyte':(charrange, 9,19)},
            {'cname':'ion',
             'cbyte':(charrange, 20, 22)},
            {'cname':'inchi',
             'cbyte':(charrange, 23, 54)},
            {'cname':'inchikey',
             'cbyte':(charrange, 55, 82)},
            {'cname':'mass',
             'cbyte':(charrange, 84, 91)},
            {'cname':'massno',
             'cbyte':(charrange2int, 84, 91)},
            {'cname':'ionen',
             'cbyte':(charrange, 92, 102)},
            {'cname':'solariso',
             'cbyte':(charrange, 103,109)},
            {'cname':'dissen',
             'cbyte':(charrange, 110, 119)},
            {'cname':'ncomp',
             'cbyte':(charrange, 194, 195)},
            {'cname':'atomic',
             'cbyte':(charrange_atom, 5000, 196, 198),
             'cnull':'X'},
            {'cname':'isotope',
             'cbyte':(charrange_atom, 5000, 199, 202),
             'cnull':'X'},
            ],
     }, # end of definition for species file


    # State model read 2 lines at a time from vald3 main file term
    # files are grouped with 3 lines (lower,upper,transition_inf) for
    # every 2 lines (lower, upper) in the vald file

    # States output file appended with lower states
    {'outfile':outbase + 'lowstates.dat',
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
             'cbyte':(charrange, 84,90),
             'cnull':'99.00'},
            #{'cname':'coupling',
            # 'cbyte':(charrange, 124,126)},
            #{'cname':'term',
            # 'cbyte':(charrange, 126,212)},

            # read from 2nd open vald file (2nd line per record)
            {'filenum':1,
             'cname':'energy_ref',
             'cbyte':(charrange, 17,25)},
            {'filenum':1,
             'cname':'lande_ref',
             'cbyte':(charrange, 33,41)},
            {'filenum':1,
             'cname':'level_ref',
             'cbyte':(charrange, 65,73)},

            ## this links to linelists rather than refs directly
            #{'cname':'energy_linelist',
            # 'cbyte':(charrange, 342,346)},
            #{'cname':'lande_linelist',
            # 'cbyte':(charrange, 350,354)},
            #{'cname':'level_linelist',
            # 'cbyte':(charrange, 366,370)},

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
            #{'filenum':3, # use 2nd open term file
            # 'cname':'transition_type',
            # 'cbyte':(get_term_transtype,'ttype'),
            # 'cnull':'X',},
            #{'filenum':3, # use 2nd open term file
            # 'cname':'autoionized',
            # 'cbyte':(get_term_transtype,'autoio'),
            # 'cnull':'X',},
            ]
     }, # end of State model creation - lower states

    # upper states
    {'outfile':outbase + 'upstates.dat',
     'infiles': (vald_file, vald_file, terms_file, terms_file),
     'headlines':(2, 2, 0, 0),
     'commentchar': ('#', '#', '#','#'),
     'linestep':(2, 2, 3, 3),
     'lineoffset':(0, 1, 1, 2), # start point of step
     'errline':("Unknown", "Unknown","Unknown"),
     'linemap':[
            {'cname':'charid',        #species,coup,jnum,term,energy (upper states)
             'cbyte':(merge_cols,
                      (30,36), (212,214), (78,84), (214,300), (64,78))},
            {'cname':'species',
             'cbyte':(charrange, 30,36)},
            {'cname':'energy',
             'cbyte':(charrange, 64,78)},
            {'cname':'lande',
             'cbyte':(charrange, 90,96),
             'cnull':'99.00'},
            #{'cname':'coupling',
            # 'cbyte':(charrange, 212,214)},
            #{'cname':'term',
            # 'cbyte':(charrange, 214,300)},

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
            #{'cname':'energy_linelist',
            # 'cbyte':(charrange, 346,350)},
            #{'cname':'lande_linelist',
            # 'cbyte':(charrange, 350,354)},
            #{'cname':'level_linelist',
            # 'cbyte':(charrange, 366,370)},

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
            #{'filenum':3, # use 2nd open term file
            # 'cname':'transition_type',
            # 'cbyte':(get_term_transtype,'ttype'),
            # 'cnull':'X',},
            #{'filenum':3, # use 2nd open term file
            # 'cname':'autoionized',
            # 'cbyte':(get_term_transtype,'autoio'),
            # 'cnull':'X',},
            ]
     }, # end of upper states

    # Transition model, using the vald file
    {'outfile': outbase + 'transitions.dat',
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
                      (30,36), (212,214), (78,84), (214,300), (64,78))},
                       #(30,36), (170,172), (77,82), (172,218), (63,77))},
            {'cname':'lostate',
             'cbyte':(merge_cols,
                      (30,36), (124,126), (58,64), (126,212), (44,58))},
                      #(30,36), (122,124), (58,63), (124,170), (44,58))},
            #{'cname':'ritzwave',
            # 'cbyte':(charrange, 0,15)},
            {'cname':'wave',
             'cbyte':(charrange, 15,30)},
            {'cname':'species',
             'cbyte':(charrange, 30,36)},
            {'cname':'loggf',
             'cbyte':(charrange, 36,44)},
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
            #{'cname':'accur',
            # 'cbyte':(get_accur, (307,308), (308,314)),
            # 'debug':False},
            #{'cname':'comment',
            # 'cbyte':(charrange, 318,334)},
            #{'cname':'srctag',
            # 'cbyte':(charrange, 300,307),
            # 'skiperror':True},

            # read from every second line of the vald file
            {'filenum':1,
             'cname':'wave_ref',
             'cbyte':(charrange, 0,9)},
            {'filenum':1,
             'cname':'loggf_ref',
             'cbyte':(charrange, 9,17)},
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
            #{'cname':'wave_linelist',
            # 'cbyte':(charrange, 334,338)},
            #{'cname':'loggf_linelist',
            # 'cbyte':(charrange, 338,342)},
            #{'cname':'lande_linelist',
            # 'cbyte':(charrange, 350,354)},
            #{'cname':'gammarad_linelist',
            # 'cbyte':(charrange, 354,358)},
            #{'cname':'gammastark_linelist',
            # 'cbyte':(charrange, 358,362)},
            #{'cname':'waals_linelist',
            # 'cbyte':(charrange, 362,366)},
            # 
            # obstype is parsed from wave_linelist in post-processing
            # but we need to insert NULLs to make the DB accept the file.
            {'cname':'obstype',
             'cbyte':(constant, 'NULL'),
             'cnull':'NULL'},
            ],
    }, # end of transitions

    # Populate References with bibtex data file (block parsing)
    {'outfile':outbase + 'references.dat',
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
    {'outfile': outbase + 'linelists.dat',
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
            {'cname':'method_return',
             'cbyte':(get_method_type, ),
             'cnull':'X'},
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

# short-cutting the mapping for testing
#mapping = [mapping[0]] + mapping[2:]



# Stand-alone scrípts (cannot depend on tables created above, these
# are run first!)

def species_component(species_file, outfile):
    """
    This is a stand-alone function for creating
    a species-to-component mapping file representing
    the many2many relationship.
    """
    outstring = ""
    f = open(species_file, 'r')
    for line in f:
        if line.strip() and (line.strip().startswith('#') or line.strip().startswith('@')):
            continue
        sid = line[:7].strip()
        if int(sid) < 5000:
            continue
        #import pdb;pdb.set_trace()
        # we have a molecule
        ncomp = int(line[194:195])
        for icomp in range(ncomp):
            csid = line[196+icomp*8 : 203+icomp*8].strip()
            outstring += '\N;"%s";"%s"\n' % (sid, csid)
    f.close()
    f = open(outfile, 'w')
    f.write(outstring)
    f.close()
    print "... Created file %s." % outfile

# create many2many tables

print "Running species_component ..."
species_component(species_list_file, outbase + "species_components.dat")

import linelists_references
print "Running linelists_references ..."
linelists_references.linelists_references(vald_cfg_file, linelist_file, outfile=outbase + "linelists_references.dat")
