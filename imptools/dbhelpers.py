#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

helper functions to create and fill the database

"""

from vamdc.db.cursors import *

import string as s
import sys

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
        
def do_file(tconf):
    model=tconf['model']
    f=open(tconf['fname'])
    for i in range(tconf['headlines']):
        f.readline()

    for line in f:
        if line.startswith(tconf['commentchar']): continue
        data=[]
        for colconf in tconf['columns']:
            fu=colconf['cbyte'][0]
            args=colconf['cbyte'][1]
            d=fu(line,*args)
            if d:
                if colconf.has_key('cnull'):
                    if d==colconf['cnull']: continue
                data.append('%s="%s"'%(colconf['cname'],d))
        ms='m=model(%s)'%','.join(data)
        try:
            exec(ms)
            m.save()
        except Exception, value:
            print ms, value
            sys.exit()
        
            

def do_all(conf):
    for fconf in conf['files']:
        do_file(fconf)
