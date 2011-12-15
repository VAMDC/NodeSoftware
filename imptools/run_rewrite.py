#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This program implements a database importer that reads from
ascii-input files to the django database. It's generic and is
controlled from a mapping file.
"""


import os, os.path, sys, imp, optparse
from time import time
from multiprocessing import Pool

#sys.path.append(os.environ['VAMDCROOT'])
sys.path.append(os.path.abspath(os.pardir))
sys.path.append(os.path.abspath(os.curdir))
sys.path.append(os.path.abspath(os.path.join(os.pardir,'nodes')))

DEBUG = False

def numCPUs():
    if not hasattr(os, "sysconf"):
        raise RuntimeError("No sysconf detected.")
    return os.sysconf("SC_NPROCESSORS_ONLN")

if numCPUs() > 2:
    nProc = numCPUs() - 1
else: nProc = 1

def mod_import(mod_path):
    """
    Takes filename of a module, converts it to a python path
    and imports it.
    """
    if not os.path.isabs(mod_path):
        mod_path = os.path.abspath(mod_path)
    path, filename = mod_path.rsplit(os.path.sep, 1)
    modname = filename.rstrip('.py')

    # for good measure, add given path to sys so one can for example import 
    # modules in the same directory from inside the mapping file.
    sys.path.append(os.path.abspath(path))

    try:
        result = imp.find_module(modname, [path])
    except ImportError:
        print "Could not find module '%s' (%s.py) at path '%s'" % (modname, modname, path)
        return None
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

def do_rewrite():
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

    # check for old output files and warn if they were found
    found_files = []
    for map_dict in mapping:
        outfile = map_dict.get("outfile", None)
        try:
            f = open(outfile, 'r')
            found_files.append(outfile)
            f.close()
        except IOError:
            pass
    if found_files:
        print "  Warning: output files already exists:"
        print "  " + ", ".join(found_files)
        print "  You should remove these before continuing (or they will be appended to)!"
        inp = raw_input("Continue Y/[N]? > ")
        if not inp.lower() == 'y':
            sys.exit()

    # import our rewrite library
    import rewrite as R

    if not R.validate_mapping(mapping):  return
    t0 = time()

    ProcPool = Pool(nProc)
    ProcPool.map(R.make_outfile,mapping)

    print "Total time used: %s" % R.ftime(t0, time())


if __name__ == '__main__':
    do_rewrite()
