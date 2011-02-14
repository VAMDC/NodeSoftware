#!/usr/bin/python

# Helper program that creates a many2many mappings file 
# based on the vald3 config file and the linelists wiki page.
#
# VALD3.cfg + VALD3linelists -> many2many_mapping
#

import sys


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


def merge_files(infile1, infile2, outfile):
    """
    Main program
    """

    fout = open(outfile, 'w')

    dic1 = parse_config_file(infile1)
    dic2 = parse_wiki_linelist_file(infile2)    

    # create new file on format ID;refs,refs,refs;filename;type;elements;...
    lines = []
    for filekey1, tup1  in dic1.items():
        if not filekey1 in dic2:
            print "filename %s from file %s is not matched to any file in file %s." % (filekey1, infile1, infile2)
        else:
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
Usage: linelists2references.py <VALD3.cfg> <VALD3linelists.txt> [<output>]

 This creates an output files (default is linelists_references.dat).

 This file should be read directly into the database
 many-to-many table relating Linelist  with the Reference model.
 (probably linelistreferences_columns)
"""
        sys.exit()
    if len(argv) < 4:
        output = "linelists_references.dat"
    else:
        output1 = argv[3]

    merge_files(argv[1], argv[2], output)
    print "... Created file %s." % (output) 
