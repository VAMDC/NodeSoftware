#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This program implements a database importer that reads from
ascii-input files to the django database. It's generic and is
controlled from a mapping file.
"""

import os
import sys

# making the import non-dependent on main folder name
sys.path.append("..")
os.environ['DJANGO_SETTINGS_MODULE']="DjVALD.settings"

# the mapping file
import imptools
import mapping_vald3


# The main program
#        
        
def import_to_db():
    """
    Starts the importer.
    """
    if len(sys.argv) < 2:
        print "Usage: import.py dummy|vald|<path-to-mapping-file>"  
        return

    if sys.argv[1] == 'dummy':
        print "This feature is not yet implemented."
        return
    
    elif sys.argv[1] == 'vald':
        mapping = mapping_vald3.mapping
        
    else:
        # read file 
        mapping = imptools.readcfg(sys.argv[1])

    if mapping:
        # do the import 
        imptools.parse_mapping(mapping, debug=False)
    else:
        # likely an error in reading a mapping file. 
        return 
    
if __name__ == '__main__':    
    import_to_db()



