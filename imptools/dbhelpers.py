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

import string as s
import sys

from django.db.utils import IntegrityError
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

def getdata(tconf,line,model):
    if tconf.has_key('updatematch'):
        colconf=tconf['columns'][0]
        fu=colconf['cbyte'][0]
        args=colconf['cbyte'][1]
        d=fu(line,*args)
        if not d: return None
        exec('modelq=Q(%s="%s")'%(tconf['updatematch'],d))
        try:
             data=model.objects.get(modelq)
        except: data=None
    else: 
        data=model()
    return data
                    
def findMatchAndUpdate(tconf,data,line):
    model=tconf['model']
    colconf=tconf['columns'][0]
    fu=colconf['cbyte'][0]
    args=colconf['cbyte'][1]
    d=fu(line,*args)
    exec('modelq=Q(%s="%s")'%(tconf['updatematch'],d))
    try:
        match=model.objects.get(modelq)
    except Exception, e: 
        sys.stderr.write(str(e)+'\n')
        return
    
    for key in data.keys(): setattr(match,key,data[key])
    try: match.save()
    except Exception, e:
        sys.stderr.write(str(e)+'\n')


def saveAsNew(model,data):
    try:
        model.objects.create(**data)
    except Exception, e:
        sys.stderr.write(str(e)+'\n')

def do_file(tconf):
    print 'working on %s ...'%tconf['fname'],
    model=tconf['model']
    f=open(tconf['fname'])
    for i in range(tconf['headlines']): f.readline()

    data={'pk':None}
    for line in f:
        if line.startswith(tconf['commentchar']): continue
        for colconf in tconf['columns']:
            fu=colconf['cbyte'][0]
            args=colconf['cbyte'][1]
            d=fu(line,*args)
            if not d: continue
            if colconf.has_key('cnull'):
                if d==colconf['cnull']: continue
            #if hasattr(model,colconf['cname']): ## THIS IS A FOREIGN KEY
            if colconf.has_key('references'):
                refmodel=colconf['references'][0]
                refcol=colconf['references'][1]
                #ref=getattr(model,colconf['cname'])
                
                qexec='q=Q(%s="%s")'%(refcol,d)
                exec(qexec)
                try: d=refmodel.objects.get(q)
                except: 
                    d=None
            
            data[colconf['cname']]=d
                

        if tconf.has_key('updatematch'):
            findMatchAndUpdate(tconf,data,line)
        else:
            saveAsNew(model,data)
        
    print 'done.'
           

def do_all(conf):
    for fconf in conf['files']:
        do_file(fconf)
