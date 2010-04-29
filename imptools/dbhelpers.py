#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

helper functions to create and fill the database

"""

from vamdc.db.cursors import *

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
            if hasattr(model,colconf['cname']): ## THIS IS A FOREIGN KEY
                ref=getattr(model,colconf['cname'])
                if colconf.has_key('foreignpk'):
                    qexec='q=Q(%s="%s")'%(colconf['foreignpk'],d)
                    exec(qexec)
                        
                else: q=Q(pk=d)

                try: d=ref.field.related.parent_model.objects.get(q)
                except: d=None
            
            data[colconf['cname']]=d
                

        try:
            if tconf.has_key('updatematch'):
                colconf=tconf['columns'][0]
                fu=colconf['cbyte'][0]
                args=colconf['cbyte'][1]
                d=fu(line,*args)
                exec('modelq=Q(%s="%s")'%(tconf['updatematch'],d))
                match=model.objects.get(modelq)
                for key in data.keys(): setattr(match,key,data[key])
            else:
                model.objects.create(**data)
        except IntegrityError, value:
            if 'column charid is not unique' in value: pass
            else: print data,value; sys.exit()

        except Exception, value:
            print data,value
            #sys.exit()
    print 'done.'
           

def do_all(conf):
    for fconf in conf['files']:
        do_file(fconf)
