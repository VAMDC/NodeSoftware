#!/usr/bin/python
#
# Helper program that creates a many2many mappings file 
# based on the species file (for molecular species concisting
# of other species)

import sys, pdb

# parse VALD3linlists

def parse_species_file(filename):
    """
    Parses the lines of the VALD_list_of_species
    """
    f = open(filename, 'r')

    dic = {}
    string = ""
    for line in f:        
        if line.strip().startswith('#') or line.strip().startswith('@'):
            continue                
        if int(line[20:22]) != 0:
            continue
        if int(line[132:133]) == 1:
            # an atom
            dic[line[134:136].strip()] = line[0:7].strip()
        else:
            # a molecule - at this point we should already have
            # a full range of (neutral) atoms to search for
            # atommasses of up to four component species
            dbref = line[0:7].strip()
            cdbrefs = [dic.get(line[134:136].strip()),
                       dic.get(line[141:143].strip()),
                       dic.get(line[148:150].strip()),
                       dic.get(line[155:157].strip())]
            for cdbref in [cm for cm in set(cdbrefs) if cm]:
                string += '\N;"%s";"%s"\n' % (dbref, cdbref)
    return string
    
                
if __name__=='__main__':

    #pdb.set_trace()
    argv = sys.argv
    if len(argv) < 2:
        print """
Usage: species_species.py <VALD_list_of_species>

Creates an output file "species_species.dat" for direct
reading into the database table as a many2many field mapping. 
"""
        sys.exit()
    infile = argv[1]        
    output = "species_species.dat"
    string = parse_species_file(infile)
    # writing file 
    fout = open(output, 'w')
    fout.write(string)
    fout.close()
    print "... Created file %s." % (output) 
