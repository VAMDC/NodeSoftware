#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

helper functions to create and fill the database

"""

from __future__ import with_statement
import contextlib
import sys
from django.db.models import Q
#from django.db.utils import IntegrityError
#import string as s

@contextlib.contextmanager
def handler():
    try:
        yield
    except Exception, e:
        print e

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
           any(True for fdict in mapping if type(fdict) != dict): 
        raise Exception("Mapping must be a list of dictionaries, one for each file to convert.")
    for fdict in mapping: 
        if len(True for key in fdict.keys() if key in required_fdict_keys) < len(required_fdict_keys):
            string = "Mapping error: One of the keys %s is missing from the mapping %s."
            raise Exception(string % (required_fdict_keys, fdict.keys()))
        if not fdict.columns:
            raise Exception("No column matchings defined.")
        if not type(fdict.columns) == list or not type(fdict.columns[0]) == dict:
            raise Exception("Mapping error: 'column' must be a list of dicts.")        
        if len(True for key in fdict.columns.keys() if key in required_col_keys) < len(required_col_keys):
            string = "Mapping error: Columns must have at least keys %s" % required_col_keys
            raise Exception(string)
    return True 

    
def process_line(line, colconf):
    "Process one line of data"
    colfunc = colconf['cbyte'][0]
    args = colconf['cbyte'][1]
    dat = colfunc(line, *args)
    if not dat or colconf.has_key('cnull') \
           and dat == colconf['cnull']:
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
        except:
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
    # this defines 'modelq' as a quertyset 
    exec('modelq=Q(%s="%s")' % (tconf['updatematch'], dat))
    try:
        match=model.objects.get(modelq)
    except Exception, e: 
        sys.stderr.write(str(e)+'\n')
        return
    
    for key in data.keys(): setattr(match,key,data[key])
    try: match.save()
    except Exception, e:
        sys.stderr.write(str(e)+'\n')


def create_new(model, data):
    """
    Create a new object of type model and store
    it in the database. 
    """
    try:
        model.objects.create(**data)
    except Exception, e:
        sys.stderr.write(str(e)+'\n')

def parse_fdict(fdict):
    """
    Process one file definition from a config dictionary by
    processing the file name stored in it and parse it according
    to the mapping. 

    fdict - config dictionary representing one input file structure
    (for an example see e.g. mapping_vald3.py)
    """
    
    print 'working on %s ...' % fdict['fname'],
    model = fdict['model']
    f = open(fdict['fname'])
    for i in range(fdict['headlines']):
        # skip header lines 
        f.readline()

    data={'pk':None}

    for line in f:
        if line.startswith(fdict['commentchar']):
            # wean out comments 
            continue
        for column in fdict['columns']:
            # process this line extracting all columns
            # and converting them to db fields
            func = column['cbyte'][0]
            args = column['cbyte'][1]
            dat = func(line, *args)
            if not dat or \
                   (column.has_key('cnull') and dat == column['cnull']):
                # not a valid line for whatever reason 
                continue

            #if hasattr(model,column['cname']): ## THIS IS A FOREIGN KEY
            if column.has_key('references'):
                # this collumn references another field
                # (i.e. a foreign key)
                refmodel = column['references'][0]
                refcol = column['references'][1]            
                # create a query object q for locating
                # the referenced model and field
                exec('q=Q(%s="%s")' % (refcol, dat))
                try:
                    dat = refmodel.objects.get(q)
                except: 
                    dat = None            
            data[column['cname']] = dat
                
        if fdict.has_key('updatematch'):
            # Model was already created; this run is for
            # updating it properly (e.g. for vald 
            find_match_and_update(fdict, data, line)
        else:
            # create a new instance of model and store it in database,
            # populated with the relevant fields. 
            create_new(model, data)
        
    print 'done.'
           

def parse_mapping(mapping):
    """
    Step through a list of mappings describing
    the relation between (usually ascii-)files and
    django database fields. This should ideally
    not have to be changed for different database types.
    """
    if validate_mapping(mapping):    
        for fdict in mapping:
            parse_fdict(fdict) 
