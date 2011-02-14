#!/usr/bin/python

# Helper program that takes two vald wiki input files and creates two new files,
# intended for direct reading into the database.
#
# vald3.cfg + VALD3linelists -> linelist_file, many2many_mapping
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


def merge_files(infile1, infile2, outfile1, outfile2):
    """
    Main program
    """

    f1 = open(outfile1, 'w')
    f2 = open(outfile2, 'w')

    dic1 = parse_config_file(infile1)
    dic2 = parse_wiki_linelist_file(infile2)    

    # create new file on format ID;refs,refs,refs;filename;type;elements;...
    lines1 = []
    lines2 = []
    for filekey1, tup1  in dic1.items():
        if not filekey1 in dic2:
            print "filename %s from file %s is not matched to any file in file %s." % (filekey1, infile1, infile2)
        else:
            tup2 = dic2[filekey1]
            lines1.append('"%s";"%s";"%s";"%s";"%s";"%s"\n' % (tup1[0], ','.join(tup2[2]), filekey1, tup2[1], tup2[0], ';'.join(('"%s"' % d for d in tup1[1:]))))            
            for ref in tup2[2]:                
                lines2.append('\N;"%s";"%s"\n' % (tup1[0], ref))
    f1.writelines(lines1)    
    f1.close()
    f2.writelines(lines2)
    f2.close()
    
if __name__=='__main__':

    import pdb
    #pdb.set_trace()
    argv = sys.argv
    if len(argv) < 3:
        print """
Usage: preprefs <VALD_cfg> <VALD_wiki_linelist> [<output1>, <output2>]

 This creates two output files (defaulting to linelist.dat
 and linelists2references_manytomany.dat).

 These two files should be read directly into the database tables
 for the Linelist model and to the many-to-many table relating Linelist
 with the Reference model, respectively.
"""

        sys.exit()
    if len(argv) < 5:
        output1 = "linelists.dat"
        output2 = "linelists2references_manytomany.dat"
    else:
        output1 = argv[3]
        output2 = argv[4]

    merge_files(argv[1], argv[2], output1, output2)
    print "... Output files %s and %s." % (output1, output2) 
