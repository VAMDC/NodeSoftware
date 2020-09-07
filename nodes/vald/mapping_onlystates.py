#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The config file for importing VALD into a database.

Go to http://vamdc.tmy.se/doc/importing.html
for understanding what happens below.
"""
from imptools.linefuncs import *
from xml.sax.saxutils import escape

# Setting up filenames
base = "/vald/vamdc/raw_vald_data/"
species_list_file = base + 'VALD_list_of_species.csv'
vald_cfg_file = base + 'VALD3.cfg'
vald_file = base + 'vald3_atoms_all.dat.gz' # change to vald3_molec.dat.gz for molecules
terms_file = base + 'terms_atoms_all.dat'
#vald_file = base + 'vald3_atoms_2000.dat' # change to vald3_molec.dat.gz for molecules
#terms_file = base + 'terms_atoms_3000.dat'
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
# mix - mixture of observation times/compilation
METHOD_DICT = {'exp':0, 'obs':1, 'emp':2, 'pred':3, 'calc':4, 'mix':5, 'comp':5}

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

def get_wave(linedata):
    """
    Get measured wavelengths if available, otherwise use RITZ wls.
    """
    wavemeasured = charrange(linedata, 15,30)
    waveritz = charrange(linedata, 0,15)
    return wavemeasured == waveritz and waveritz or wavemeasured

def get_wave_ref(linedata):
    """
    Get the correct reference for wave (either from measured or ritz)
    """
    if charrange(linedata, 15,30) == charrange(linedata, 0,15): # use ritz ref
       return charrange(linedata, 25,33)
    return charrange(linedata, 0,9) # use measured ref


NIST_MAP = {"AAA":0.003,"AA":0.01,"A+":0.02,"A":0.03,"B+":0.07,
            "B":0.1,"C+":0.18,"C":0.25,"D+":0.40,"D":0.5,"E":1.0}
def get_accur(linedata):
    """
    Extract VALD accur data and convert it to a VAMDC equivalent.
    Each flag also maps to a given xsams tag as follows:
    VALD   VAMDC
    N (NIST)                 AccuracyType:estimated, AccuracyRelative:true
    E (error in dex)         AccuracyType:estimated, AccuracyRelative:true
    C (cancellation factor)  AccuracyType:arbitrary, AccurayRelative:true
    P (predicted line)       AccuracyType:systematic, AccuracyRelative:false
    """
    flag = charrange(linedata, 307,308)
    value = charrange(linedata, 308, 314)
    if flag == 'N': # NIST quality flag
        value = NIST_MAP.get(value, "E")
    elif flag in ('E','P'):
        value = float(value)
    elif flag == 'C':
        value = value # this is incorrect, conversion is non-trivial
    else:
        value = 'X'
    return value

def get_term_transtype(linedata):
    """
    Get transition type info from term file.

    line consists of either
     Allowed_transition:<vacuumwl>, E1, Extra_info:none
     Forbidden_transition:<vacuumwl>,XX, Extra_info:none
     or
     Autoionization, Extra_info:none
    """
    try:
        info, term, extra = linedata.split(":", 2)
        # term section consists of "wacumwavelength, transtype"
        wl, ttype, einfo = term.split(",", 2)
        return ttype.strip()
    except ValueError:
        # autoionizing or malformed line
        return 'X'

def get_species_part(linedata, ipos, retint=False, sep=","):
    """
    Variation to sepByNumber taking into account that
    inchi can sometimes also contain a comma - in that
    case all following positions must be shifted accordingly.
    retint (bool) - return as integer rather than string
    """
    splits = linedata.split(sep)
    if splits[4].startswith('"'):
        # inchicode starts with ", this means it contains a comma
        if ipos == 4:
            return (splits[4] + splits[5]).strip('"')
        elif ipos > 4:
            # shift position
            ipos += 1
    # return normally
    return retint and int(round(float(splits[ipos].strip()))) or splits[ipos].strip()

MOLECULE_START = 10000 # starting id for molecules in species file (atoms lower than this value)
def get_species_part_atom(linedata, pos):
    """
    This method is to be used to read species data.
    It returns data only if the species currently worked on
    is an atom and not a molecule. Otherwise return '0'

     pos - comma-position in linedata
     ia,ib - index1, index2
    """
    if bySepNr2int(linedata, 1) < MOLECULE_START:
       return get_species_part(linedata, pos)
    return '0'

def get_auto_ionization(linedata):
    """
    In the case of Autoionization, the line looks like this:
      Autoionization, Extra_information:none
    """
    return linedata.count(":") == 1


def charrange_escape(linedata, ia, ib):
    """
    This works like charrange except it also escapes the resulting
    string to make it safe for use in xsams.
    """
    return escape(charrange(linedata, ia, ib))

def species_component(species_file, outfile):
    """
    This is a stand-alone function for creating
    a species-to-component mapping file representing
    the many2many relationship. It is called automatically
    last in this file.
    """
    outstring = ""
    f = open(species_file, 'r')
    f.readline() # skip header
    for line in f:
        if line.strip() and (line.strip().startswith('#') or line.strip().startswith('@')):
            continue
        lineparts = line.split(",")
        #print  len(lineparts), lineparts
        sid = lineparts[1]
        # ignore for atoms
        if int(sid) < MOLECULE_START:
            continue
        # we have a molecule
        ncomp = int(lineparts[9])
        for icomp in range(ncomp):
            csid = lineparts[10 + icomp]
            outstring += '\N;"%s";"%s"\n' % (sid, csid)

        #sid = line[:7].strip()
        #if int(sid) < MOLECULE_START:
        #    continue
        ##import pdb;pdb.set_trace()
        ## we have a molecule
        #ncomp = int(line[198:199])
        #for icomp in range(ncomp):
        #    csid = line[200+icomp*8 : 208+icomp*8].strip()
        #    outstring += '\N;"%s";"%s"\n' % (sid, csid)
    f.close()
    f = open(outfile, 'w')
    f.write(outstring)
    f.close()
    print "... Created file %s." % outfile

# Multiprocess id-creator mechanism using a dictionary and multiprocess-locks to make sure
# state ids are unique already at the import stage. The state table is pretty small and can thus fit in
# memory; Using the old MySQL-based mapper (now deleted) took 4157 mins (2 days 21 hours)
# for a rewrite. Using this solution takes 3442 mins (2 days 9 hours) on the same data.

from multiprocessing import Manager, Lock
from ctypes import c_int
MANAGER = Manager()
LOCK1 = Lock()
LOCK2 = Lock()
DBID = MANAGER.Value(c_int, 0)
STATEDICT = MANAGER.dict()
def unique_state_id(linedata, processid, *ranges):
    "alternative line function using dictionary"
    global STATEDICT
    charid = merge_cols(linedata, *ranges)
    idnum = None

    with LOCK1:
        # lock things down and set an updated id
        if not charid in STATEDICT:
            global DBID
            idnum = DBID.value + 1
            DBID.value = idnum
            STATEDICT[charid] = (idnum, processid)
            return idnum
    with LOCK2:
        idnum, setproc = STATEDICT[charid]
        if processid in (0, 1) and setproc in (0, 1):
            # don't store a new one if the value was set by up/lowstate parsing
            raise RuntimeError
        return idnum


#------------------------------------------------------------
# The mapping itself
#------------------------------------------------------------
mapping = [
    # State model read 2 lines at a time from vald3 main file. the term
    # file is grouped with 3 lines (lower,upper,transition_info) for
    # every 2 lines (the first line of which contains both lower,
    # upper info, the second which contains refs) in the vald file. We
    # loop over the files twice; first to retrieve the lower states,
    # then the upper (see next block).

    # States output file appended with lower states
    {'outfile':outbase + 'lowstates.dat',
     'infiles':(vald_file, vald_file, terms_file),
     'headlines':(2, 2, 0),
     'commentchar':('#','#','#'),
     'linestep':(2, 2, 3),   # step length in each file
     'lineoffset':(0, 1, 0), # start point of step in each file
     'errlines':("Unknown", "Unknown", "X"), # termfile errline must not be 'Unknown' since some good lines start with that.
     'linemap':[
            {'cname':'id',         #species,coup,jnum,lande,term,energy (lower states)
             'cbyte':(unique_state_id, 0,
                      (30,36), (124,126), (58,64), (84,90), (126,212), (44,58))},
            {'cname':'species',
             'cbyte':(charrange, 30,36)},
            {'cname':'energy',
             'cbyte':(charrange, 44,58)},
            #{'cname':'j',
            # 'cbyte':(charrange, 58,64)},
            {'cname':'lande',
             'cbyte':(charrange, 84,90),
             'cnull':'99.00'},
            {'cname':'term_desc',
             'cbyte':(charrange_escape, 126,212)},
            # read from 2nd open vald file (2nd line per record)
            {'filenum':1,
             'cname':'energy_ref_id',
             'cbyte':(charrange, 17,25)},
            {'filenum':1,
             'cname':'lande_ref_id',
             'cbyte':(charrange, 33,41)},
            {'filenum':1,
             'cname':'level_ref_id',
             'cbyte':(charrange, 65,73)},
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
            {'filenum':2, # use term file
             'cname':'n',
             'cbyte':(get_term_val,'n'),
             'cnull':'X',},
            ]
     }, # end of State model creation - lower states

    # re-importing upper states
    {'outfile':outbase + 'upstates.dat',
     'infiles': (vald_file, vald_file, terms_file),
     'headlines':(2, 2, 0),
     'commentchar': ('#', '#', '#'),
     'linestep':(2, 2, 3),
     'lineoffset':(0, 1, 1), # start point of step
     'errlines':("Unknown", "Unknown","X"),
     'linemap':[
            {'cname':'id',        #species,coup,jnum,lande,term,energy (upper states)
             'cbyte':(unique_state_id, 1,
                      (30,36), (212,214), (78,84), (90,96), (214,300), (64,78))},
            {'cname':'species',
             'cbyte':(charrange, 30,36)},
            {'cname':'energy',
             'cbyte':(charrange, 64,78)},
            {'cname':'lande',
             'cbyte':(charrange, 90,96),
             'cnull':'99.00'},
            {'cname':'term_desc',
             'cbyte':(charrange_escape, 214,300)},
            # read from 2nd open vald file (2nd line per record)
            {'filenum':1,
             'cname':'energy_ref_id',
             'cbyte':(charrange, 25,33)},
             #'references':(models.Source,'pk')},
            {'filenum':1,
             'cname':'lande_ref_id',
             'cbyte':(charrange, 33,41)},
             #'references':(models.Source,'pk')},
            {'filenum':1,
             'cname':'level_ref_id',
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
            {'filenum':2, # use term file
             'cname':'n',
             'cbyte':(get_term_val,'n'),
             'cnull':'X',},
            ]
     }, # end of upper states

     ]
