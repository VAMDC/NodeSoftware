#!/usr/bin/python

# Helper program that creates a many2many mappings file 
# based on the vald3 config file and the linelists wiki page.
#
# VALD3.cfg + VALD3linelists -> many2many_mapping
#
# If a bibtex file is given, a cross-reference match will be
# performed between the three files as part of the file
# creation and validation.

import sys, pdb
import itertools

# parse VALD3linlists

def parse_wiki_linelist_file(filename):
    """
    Parses the lines of the VALD3linelists
    """
    f = open(filename, 'r')

    dic = {}
    for line in f:        
        if not line.startswith('||'):
            continue
        cols = line.split('||')[1:]
        if not cols[0].strip() or  not cols[0].strip()[0].isalnum():
            continue
        fil = cols[0].strip()
        if fil in dic:
            raise Exception("Non-unique filename in %s: %s" % (filename, fil))
        else:    
            elements = cols[1].strip()
            typ = cols[2].strip()
            try:
                refs = [element.strip().strip(']]').strip().split('|')[1] for element in cols[3].split(',') if element.strip()]
            except IndexError:
                print "Error parsing line \n%s\n" % line 
                raise 
            dic[fil] = (elements, typ, refs)        
    return dic
    
def parse_config_file(filename):
    """
    Parses the lines of the VALD3.cfg
    """

    f = open(filename, 'r')

    dic = {}
    for line in f:
        if not line.startswith("'"):
            continue
        cols = [entry.strip() for entry in line.split(',')]
        fil = cols[0].split('/')[-1].strip("'")
        if fil in dic:
            raise Exception("Non-unique filename in %s: %s" % (filename, fil))
        else:
            ID = cols[1]            
            dic[fil] = [ID]  + [cols[i] for i in range(2,14)]

    return dic

def parse_bibtex_file(filename):
    """
    Parses a bibtex file, extracting all dbrefs
    """
    f = open(filename, 'r')
    #lines = " ".join([line.strip() for line in f.readlines() if line.strip and not line.strip().startswith('%')])
    entries = [line for line in f.readlines() if line.strip().startswith('@')]

    #pdb.set_trace()
    
    blist = []
    for entry in entries:
        dum, rest = entry.split('{', 1)
        dbref = rest.strip().strip(',')
        blist.append(dbref)
    bset = set(blist)
    if len(bset) != len(blist):
        print " ==== Warning: Bibtex file %s contains non-unique dbrefs:" % filename
        doublets = set([(entry, blist.count(entry)) for entry in blist if blist.count(entry) > 1])
        print ", ".join(["%s (x%s)" % (entry[0], entry[1]) for entry in doublets])
    return bset
        
def merge_files(infile1, infile2, bibtex_file=None, outfile=None):
    """
    Main program
    """

    fout = open(outfile, 'w')

    dic1 = parse_config_file(infile1)
    dic2 = parse_wiki_linelist_file(infile2)    
    if bibtex_file:
        # cross-correlation mode         
        print "\n ==== Begin Cross-correlation mode ===="
        blist = parse_bibtex_file(bibtex_file)
        warn1, warn2, warn3, warn4  = [], [], [], []
        wiki = set(itertools.chain.from_iterable([tup[2] for tup in dic2.values()]))        
        #pdb.set_trace()        
        for filekey1 in dic1:
            if not filekey1 in dic2: warn1.append(filekey1) # config filename not in wiki page
        for filekey2 in dic2:
            if not filekey2 in dic1: warn2.append(filekey2) # wiki page filename not in config
            for dbref in dic2[filekey2][2]:
                if not dbref in blist: warn3.append(dbref) # wiki dbref not in bibtex file
        for dbref in blist:            
            if dbref not in wiki: warn4.append(dbref) # bibtex entry not in wiki page
        if warn1:
            print " ==== filenames in %s but not in %s:" % (infile1, infile2)
            print ", ".join(warn1)
        if warn2:
            print " ==== filenames in %s but not in %s" % (infile2, infile1)
            print ", ".join(warn2)
        if warn3:
            print " ==== dbrefs in %s but not in %s" % (infile2, bibtex_file)
            print ", ".join(warn3)
        if warn4:
            print " ==== dbrefs entries in %s but not in %s:" % (bibtex_file, infile2)
            print ", ".join(warn4)
        print " ==== End Cross-correlation mode ====\n"    
            
    # create new file on format ID;refs,refs,refs;filename;type;elements;...
    lines = []
    for filekey1, tup1  in dic1.items():
        if filekey1 in dic2:            
            tup2 = dic2[filekey1]            
            for ref in tup2[2]:                
                lines.append('\N;"%s";"%s"\n' % (tup1[0], ref))           
    fout.writelines(lines)    
    fout.close()
    
if __name__=='__main__':

    import pdb
    #pdb.set_trace()
    argv = sys.argv
    if len(argv) < 3:
        print """
Usage: linelists_references.py <VALD3.cfg> <VALD3linelists.txt> [VALD3_ref.bib]

Creates an output file "linelists_references.dat" for direct
reading into the database. If the bibtex file is also given, the three
files are fully cross-referenced to make sure there is a complete set
of references represented in all files. If there are discrepancies,
these will be printed.
"""
        sys.exit()
    if len(argv) < 4:
        bibtex_file = None
    else:
        bibtex_file = argv[3]
    output = "linelists_references.dat"        
    merge_files(argv[1], argv[2], bibtex_file=bibtex_file, outfile=output)
    print "... Created file %s." % (output) 
