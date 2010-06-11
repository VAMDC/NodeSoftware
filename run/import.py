#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

# making the import non-dependent on main folder name
sys.path.append("..")
os.environ['DJANGO_SETTINGS_MODULE']="DjVALD.settings"

from imptools import dbhelpers
from imptools import mapping_vald3

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
        mapping = dbhelpers.readcfg(sys.argv[1])

    if mapping:
        # do the import 
        dbhelpers.parse_mapping(mapping)
    else:
        # likely an error in reading a mapping file. 
        return 
    
if __name__ == '__main__':
    import_to_db()



