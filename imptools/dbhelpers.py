#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

helper functions to create and fill the database

"""
from __future__ import with_statement
import sys
from traceback import format_exc
from django.db.models import Q
import contextlib
from time import time 

#from django.db.utils import IntegrityError
#import string as s

TOTAL_ERRS = 0

@contextlib.contextmanager
def handler():
    try:
        yield
    except Exception, e:
        print e

def ftime(t0, t1):
    "formats time to nice format."
    ds = t1 - t0
    dm, ds = int(ds) / 60, ds % 60
    return "%s min, %s s." % (dm, ds)

def log_trace(e, info=""):
    """
    Intended to be called from inside a traceback exception with
    the exception object as first argument.
    Captures the latest traceback. 
    """
    #exc = format_exc()
    sys.stderr.write("%s%s\n" % (info, str(e)))

def readcfg(fname):
    """
    Read the config dictionary from a file.
    Note: very unsafe, since the content gets executed.
    Have a look at createcfg() to see how it should look like.
    """
    try:
        f=open(fname)
    except IOError:
        print "Error: File name '%s' not found." % fname
        return None
    exec(f.read()) # this should define a variable "mapping"
    try:
        return mapping
    except NameError:
        print "Error: mapping_file must contain a global variable called 'mapping'."
        return None

def validate_mapping(mapping):
    """
    Check the mapping definition to make sure it contains
    a structure suitable for the parser.
    """
    required_fdict_keys = ("model", "fname", "headlines", "commentchar", "columns")
    required_col_keys = ("cname", "cbyte")
    if not mapping:
        raise Exception("Empty/malformed mapping.")
    if not type(mapping) == list or \
           any([True for fdict in mapping if type(fdict) != dict]): 
        raise Exception("Mapping must be a list of dictionaries, one for each file to convert.")
    for fdict in mapping: 
        if len([True for key in fdict.keys() if key in required_fdict_keys]) < len(required_fdict_keys):
            string = "Mapping error: One of the keys %s is missing from the mapping %s."
            raise Exception(string % (required_fdict_keys, fdict.keys()))
        if not fdict['columns'] or type(fdict['columns']) != list:
            raise Exception("Mapping error: 'column' must be a list of dicts.")     
        for col in fdict['columns']:            
            if not type(col) == dict or \
                len([True for key in col.keys()
                     if key in required_col_keys]) < len(required_col_keys):
                string = "Mapping error: Columns must have at least keys %s" 
                raise Exception(string % required_col_keys)
    return True 

    
def process_line(line, column_dict):
    "Process one line of data"
    colfunc = column_dict['cbyte'][0]
    args = column_dict['cbyte'][1]
    dat = colfunc(line, *args)
    if not dat or (column_dict.has_key('cnull') \
                   and dat == column_dict['cnull']):
        return None
    return dat

def get_model_instance(tconf, line, model):
    """
    Get model instance to update, alternatively create new model
    """
    if tconf.has_key('updatematch'):
        # we want to update an existing model instance.
        dat = process_line(line, tconf['columns'][0])
        if not dat:
            return
        # this defines 'modelq' as a queryset
        exec('modelq=Q(%s="%s")' % (tconf['updatematch'], dat))
        try:
             data = model.objects.get(modelq)
        except Exception:
            data = None
    else: 
        # create a new instance of the model
        data=model()
    return data
                    
def find_match_and_update(tconf, data, line):
    """
    Don't create a new database object, instead search
    the database and update an existing one.
    """
    model = tconf['model']
    dat = process_line(line, tconf['columns'][0])
    if not dat:
        return 
    # this instances variable 'modelq' as a quertyset 
    modelq = eval('Q(%s="%s")' % (tconf['updatematch'], dat))

    try:
        match=model.objects.get(modelq) 
    except Exception, e:
        raise Exception("%s: Q(%s=%s)" % (e, tconf['updatematch'], dat))
    #print data
    for key in (key for key in data.keys()
                if key != tconf['updatematch']):
        #sys.stderr.write("%s=%s, " % (key, data[key]))
        setattr(match, key, data[key])
        try:
            match.save(force_update=True) 
        except Exception, e:       
            sys.stderr.write("%s: model.%s=%s\n" % (e, key, data[key]))
            #continue
            #raise Exception("%s: model.%s=%s" % (e, key, data[key]))

def create_new(model, inpdict):
    """
    Create a new object of type model and store
    it in the database.

    model - django model type
    inpdict - dictionary of fieldname:value that should be created.
    """
    try:
        model.objects.create(**inpdict)
    except Exception, e:
        raise Exception("%s: %s" % (e, inpdict))
    
def parse_file_dict(file_dict):
    """
    Process one file definition from a config dictionary by
    processing the file name stored in it and parse it according
    to the mapping. 

    file_dict - config dictionary representing one input file structure
    (for an example see e.g. mapping_vald3.py)
    """    
    
    fname = file_dict['fname']
    fname_short = fname.split('/')[-1]
    
    print 'working on %s ...' % fname 

    model = file_dict['model']
    f = open(file_dict['fname'])
    for i in range(file_dict['headlines']):
        # skip header lines 
        f.readline()

    data = {}
    total = 0
    errors = 0

    for line in f:
        if line.startswith(file_dict['commentchar']):
            # wean out comments 
            continue
        total += 1
        for column_dict in file_dict['columns']:
            # process this line extracting all columns
            # and converting them to db fields
            dat = process_line(line, column_dict)
           
            if not dat or \
                   (column_dict.has_key('cnull') and dat == column_dict['cnull']):
                # not a valid line for whatever reason 
                continue

            #if hasattr(model,column_dict['cname']): ## THIS IS A FOREIGN KEY
            if column_dict.has_key('references'):
                # this collumn references another field
                # (i.e. a foreign key)
                refmodel = column_dict['references'][0]
                refcol = column_dict['references'][1]            
                # create a query object q for locating
                # the referenced model and field
                Qquery = eval('Q(%s="%s")' % (refcol, dat))
                try:
                    dat = refmodel.objects.get(Qquery)
                except:
                    errors += 1
                    if len(column_dict['references']) > 2 \
                            and column_dict['references'][2] == 'skiperror':
                        # Don't create an entry for this (this requires
                        # null=True in the relevant field)
                        string = "Skipping not found db reference %s.%s='%s'.\n"
                        sys.stderr.write(string % (refmodel, refcol, dat))                        
                        continue
                    string = "reference %s.%s='%s' not found.\n"                     
                    sys.stderr.write(string % (refmodel,refcol, dat))
                    raw_input("paused...")
                    dat = None            

            data[column_dict['cname']] = dat
                
        if file_dict.has_key('updatematch'):
            # Model was already created; this run is for
            # updating it properly (e.g. for vald)
            try:            
                find_match_and_update(file_dict, data, line)
            except Exception, e:
                errors += 1
                log_trace(e, "ERROR %s: updating %s: " % (fname_short, model))
        else:
            # create a new instance of model and store it in database,
            # populated with the relevant fields. 
            if not data.has_key('pk'):
                data['pk'] = None
            try:
                create_new(model, data)
            except Exception, e:                
                errors += 1
                log_trace(e, "ERROR %s: creating %s: " % (fname_short, model))
                
    print 'done. %i collisions/errors/not founds out of %i lines.' % (errors, total)
           

def parse_mapping(mapping):
    """
    Step through a list of mappings describing
    the relation between (usually ascii-)files and
    django database fields. This should ideally
    not have to be changed for different database types.
    """
    if validate_mapping(mapping):    
        t0 = time()
        for file_dict in mapping:
            t1 = time()
            parse_file_dict(file_dict)
            print "Time used: %s" % ftime(t1, time())
        print "Total time used: %s" % ftime(t0, time())
