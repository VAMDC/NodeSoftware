#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This program implements a database importer that reads from
ascii-input files to the django database. It's generic and is
controlled from a mapping file.
"""

import os, os.path, sys, imp, optparse
sys.path.append(os.path.abspath(os.pardir))
sys.path.append(os.path.abspath(os.curdir))
sys.path.append(os.path.abspath(os.path.join(os.pardir,'nodes')))

DEBUG = False

def mod_import(mod_path):
    """
    Takes filename of a module, converts it to a python path
    and imports it. 
    """
    if not os.path.isabs(mod_path):
        mod_path = os.path.abspath(mod_path)
    path, filename = mod_path.rsplit(os.path.sep, 1)
    modname = filename.rstrip('.py')
    
    try:
        result = imp.find_module(modname, [path])
    except ImportError:
        print "Could not find module '%s' (%s.py) at path '%s'" % (modname, modname, path)
        return None 
    print result
    try:
        mod = imp.load_module(modname, *result)
    except ImportError,e:
        print "Could not find or import module %s at path '%s'" % (modname, path)
        print e
        return None 
    finally:
        # we have to close the file handle manually
        result[0].close()
    return mod 



        
def import_to_db():
    """
    Starts the importer.
    """
    parser = optparse.OptionParser(usage="Usage: %prog [options] <mapping file>")
    parser.add_option("-d", "--debug", action="store_true", default=False, dest="debug",
                      help="activate verbose debug messages")
    options, args = parser.parse_args()   
    if len(args) < 1:
        print "Usage: import.py <mapping file>"  
        return

    # import the mapping from the given filename
    mapping_module = mod_import(args[0])
    try:
        mapping = eval("mapping_module.mapping")
    except AttributeError:
        print "ERROR: The mapping file must contain a variable called 'mapping'!"
        return

    # run the full import        
    import imptools
    imptools.parse_mapping(mapping, debug=options.debug)
    
if __name__ == '__main__':       
    import_to_db()
