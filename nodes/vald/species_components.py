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
    outstring = ""
    for line in f:
        if line.strip().startswith('#') or line.strip().startswith('@'):
            continue
        sid = int(line[:7].strip())
        ncomp = int(line[132:133].strip())
        if sid < 5000:
            # store atomic components only
            anum = line[134:136]
            isot = line[137:140]
            key = "%s-%s" % (anum, isot)
            if not key in dic:
                dic[key] = sid        
            continue
        else:
            # a molecule (we also know that these come AFTER atoms in the file)
            for icomp in range(ncomp):
                offset = icomp*7
                anum = line[134+offset: 136+offset]
                isot = line[137+offset: 140+offset]
                key = "%s-%s" % (anum, isot)
                # match against atom
                asid = dic.get(key, None)
                if asid:
                    outstring += '\N;"%s";"%s"\n' % (sid, asid)
                else:
                    outstring += '\N;"%s";\N\n' % sid
    return outstring

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
    output = "species_components.dat"
    string = parse_species_file(infile)
    # writing file 
    fout = open(output, 'w')
    fout.write(string)
    fout.close()
    print "... Created file %s." % (output)
