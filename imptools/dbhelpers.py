#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

helper functions to create and fill the database

"""

from __future__ import with_statement
import contextlib

@contextlib.contextmanager
def handler():
    try:
        yield
    except Exception, e:
        print e

#import string as s
import sys

#from django.db.utils import IntegrityError
from django.db.models import Q

def readcfg(fname):
    """
       Read the config dictionary from a file.
       Note: very unsafe, since the content gets executed.
       Have a look at createcfg() to see how it should look like.
    """
    f=open(fname)
    #exec(s.join(f.readlines()))
    exec(f.read())
    return config

def process_line(line, colconf):
    "Process one line of data"
    colfunc = colconf['cbyte'][0]
    args = colconf['cbyte'][1]
    dat = colfunc(line, *args)
    if not dat or colconf.has_key('cnull') \
           and dat == colconf['cnull']:
        return None
    return dat

def getdata(tconf, line, model):
    """
    Get data, alternatively create new model
    """
    if tconf.has_key('updatematch'):
        dat = process_line(line, tconf['columns'][0])
        if not dat:
            return
        exec('modelq=Q(%s="%s")'%(tconf['updatematch'], dat))
        try:
             data = model.objects.get(modelq)
        except:
            data = None
    else: 
        data=model()
    return data
                    
def findMatchAndUpdate(tconf, data, line):
    """
    Don't create a new object, instead find and update
    and old one.
    """
    model = tconf['model']
    dat = process_line(line, tconf['columns'][0])
    if not dat:
        return 
    # this defines modelq as a quertyset 
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


def saveAsNew(model, data):
    """
    Create a new object of type model and store
    it in the database. 
    """
    try:
        model.objects.create(**data)
    except Exception, e:
        sys.stderr.write(str(e)+'\n')

def do_file(tconf):
    """
    Process one file definition from a config dictionary 

    tconf - config dictionary (see e.g. config.py)
    """
    
    print 'working on %s ...' % tconf['fname'],
    model = tconf['model']
    f = open(tconf['fname'])
    for i in range(tconf['headlines']):
        # skip header lines 
        f.readline()

    data={'pk':None}

    for line in f:
        if line.startswith(tconf['commentchar']):
            # wean out comments 
            continue
        for colconf in tconf['columns']:
            # process all columns, converting to fields


            if not dat:
                # not a valid line for whatever reason 
                continue

            #if hasattr(model,colconf['cname']): ## THIS IS A FOREIGN KEY
            if colconf.has_key('references'):
                # this collumn references another field
                # (i.e. a foreign key)
                refmodel = colconf['references'][0]
                refcol = colconf['references'][1]            
                # create a query object q for locating
                # the referenced model and field
                exec('q=Q(%s="%s")' % (refcol, dat))
                try:
                    dat = refmodel.objects.get(q)
                except: 
                    dat = None            
            data[colconf['cname']] = dat
                
        if tconf.has_key('updatematch'):
            findMatchAndUpdate(tconf, data, line)
        else:
            saveAsNew(model, data)
        
    print 'done.'
           

def do_all(conf):
    for fconf in conf:
        do_file(fconf)
