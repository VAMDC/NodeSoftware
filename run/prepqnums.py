#!/usr/bin/env python

from string import strip
from sys import exit

#v=open('vald3.dat')
#q=open('terms500.dat')
v=open('vald3_atomic_obs.dat')
q=open('terms')

out=open('myterms_all.dat','w')


def charrange(line,start,end):
    return line[start:end]

def bySepNr(line,number,sep=','):
    return line.split(sep)[number]

def makeValdUpperStateKey(line):
    species=charrange(line,30,36)
    coup=charrange(line,170,172)
    term=charrange(line,172,218)
    d=map(strip,(species,coup,term))
    if not (d[1] and d[2]): return 'Unknown'
    return '%s-%s-%s'%tuple(d)

def makeValdLowerStateKey(line):
    species=charrange(line,30,36)
    coup=charrange(line,122,124)
    term=charrange(line,124,170)
    d=map(strip,(species,coup,term))
    #print d
    if not (d[1] and d[2]): return 'Unknown'
    return '%s-%s-%s'%tuple(d)

for i,l in enumerate(v):
    if i <2:
        q.readline()
	q.readline()
	continue

    for hl in ['lo','hi']:
        qs=strip(q.readline())
	if qs=='Unknown' or qs=='': continue
	
	qcoup,qnames,qvals=qs.split(':')

	if hl=='lo': idstring=makeValdLowerStateKey(l)
	else: idstring=makeValdUpperStateKey(l)

	
	exec('%s=%s'%(qnames,qvals))
	if not 'J' in qnames.split(','): J='X'
	if not 'L' in qnames.split(','): L='X'
	if not 'S' in qnames.split(','): S='X'
	if not 'parity' in qnames.split(','): parity='X'
	if not 'J1' in qnames.split(','): J1='X'
	if not 'J2' in qnames.split(','): J2='X'
	if not 'K' in qnames.split(','): K='X'
	if not 'S2' in qnames.split(','): S2='X'
	if not 'Jc' in qnames.split(','): Jc='X'

	out.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(idstring,J,L,S,parity,J1,J2,K,S2,Jc))
            
        
        #print species,locoup,loterm,hicoup,hiterm


