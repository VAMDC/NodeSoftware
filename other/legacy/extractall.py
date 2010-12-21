#!/usr/bin/env python

"""

extractall.py

This file is not really a member of "mini-VAMDC", but uses the 
VALD extraction tools to generate ascii-files that then are used by
import.py

Automatic generation of the config-dictionaries would be nice.

"""

from string import *
from os.path import join
from os import system

valdhome='/vald'
presexe=join(valdhome,'db','pres3_2')
presin=join(valdhome,'db','pres.in')
outdir=join(valdhome,'db','asci')
allconf=join(valdhome,'db','all.cfg')

def makecfg(what,filename='my.cfg'):
    f=open(filename,'w')
    f.write('0.01,50,500.\n')
    f.write(what)
    f.close

def makepresin(filename='pres.in'):
    pass

def alldatafiles():
    f=open(allconf)
    lines=f.readlines()
    f.close()
    return lines[12:]

def run():
    whatlines=alldatafiles()
    for what in whatlines:
        makecfg(what)
        fname=what.split(',')[0][1:-1].split('/')[-1] + '.dat'
        print fname
        outfile=join(outdir,fname)
        system('%s < %s > %s'%(presexe,presin,outfile))


if __name__=='__main__':
    run()
