#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
config dictionaries and corresponding functions

"""

from string import strip
import os

### FUCTIONS TO APPLY TO DATA AFTER READING
def charrange(line,start,end):
    return strip(line[start:end])

def bySepNr(line,number,sep=','):
    return strip(line.split(sep)[number])

def makeValdUpperStateKey(line):
    species=charrange(line,30,36)
    coup=charrange(line,170,172)
    term=charrange(line,172,218)
    if not (coup and term and species): return None
    return '%s-%s-%s'%(species,coup,term)

def makeValdLowerStateKey(line):
    species=charrange(line,30,36)
    coup=charrange(line,122,124)
    term=charrange(line,124,170)
    if not (coup and term and species): return None
    return '%s-%s-%s'%(species,coup,term)


os.environ['DJANGO_SETTINGS_MODULE']="vamdc.DjVALD.settings"
from DjVALD.vald import models as valdmodel

vald3cfg={     
    'files':[  
        {'model':valdmodel.Species,     
         'fname':'/vald/VALD_list_of_species', 
         'headlines':0,   
         'commentchar':'#',   
         'columns':[          
                {'cname':'pk',  
                 'cbyte':(charrange,(0,7))},   
                {'cname':'name',  
                 'cbyte':(charrange,(9,19))},   
                {'cname':'ion',  
                 'cbyte':(charrange,(20,22))},   
                {'cname':'mass',  
                 'cbyte':(charrange,(23,30))},   
                {'cname':'ionen',  
                 'cbyte':(charrange,(31,40))},   
                {'cname':'solariso',  
                 'cbyte':(charrange,(41,46))},   
                {'cname':'ncomp',  
                 'cbyte':(charrange,(132,133))},   
                {'cname':'atomic',  
                 'cbyte':(charrange,(134,136))},   
                {'cname':'isotope',  
                 'cbyte':(charrange,(137,140))},   
               ],
         },
        {'model':valdmodel.Source,
         'fname':'/vald/vald3_test.cfg',
         'headlines':1,
         'commentchar':';',
         'columns':[\
                {'cname':'pk',
                 'cbyte':(bySepNr,(1,))},
                {'cname':'srcfile',
                 'cbyte':(bySepNr,(0,))},
                {'cname':'speclo',
                 'cbyte':(bySepNr,(2,))},
                {'cname':'spechi',
                 'cbyte':(bySepNr,(3,))},
                {'cname':'listtype',
                 'cbyte':(bySepNr,(4,))},
                {'cname':'r1',
                 'cbyte':(bySepNr,(5,))},
                {'cname':'r2',
                 'cbyte':(bySepNr,(6,))},
                {'cname':'r3',
                 'cbyte':(bySepNr,(7,))},
                {'cname':'r4',
                 'cbyte':(bySepNr,(8,))},
                {'cname':'r5',
                 'cbyte':(bySepNr,(9,))},
                {'cname':'r6',
                 'cbyte':(bySepNr,(10,))},
                {'cname':'r7',
                 'cbyte':(bySepNr,(11,))},
                {'cname':'r8',
                 'cbyte':(bySepNr,(12,))},
                {'cname':'r9',
                 'cbyte':(bySepNr,(13,))},
                {'cname':'srcdescr',
                 'cbyte':(bySepNr,(14,)),},
                ],
        },
        {'model':valdmodel.State,   ######### FIRST PASS FOR THE UPPER STATES
         'fname':'/vald/states_u.dat',
         'headlines':0,     
         'commentchar':'#',   
         'columns':[          
                {'cname':'charid',  
                 'cbyte':(bySepNr,(0,';'))},
                {'cname':'species',
                 'cbyte':(bySepNr,(1,';'))},
                {'cname':'energy',
                 'cbyte':(bySepNr,(2,';'))},
                {'cname':'lande',
                 'cbyte':(bySepNr,(3,';')),
                 'cnull':'99.00'},
                {'cname':'coupling',
                 'cbyte':(bySepNr,(4,';'))},
                {'cname':'term',
                 'cbyte':(bySepNr,(5,';'))},
                {'cname':'energy_ref',
                 'cbyte':(bySepNr,(6,';'))},
                {'cname':'lande_ref',
                 'cbyte':(bySepNr,(7,';'))},
                {'cname':'level_ref',
                 'cbyte':(bySepNr,(8,';'))},
                ]
         },
        {'model':valdmodel.Transition,    
         'fname':'/vald/vald3.dat', 
         'headlines':2,        
         'commentchar':'#',    
         'columns':[           
                {'cname':'vacwave',
                 'cbyte':(charrange,(0,15))},  
                {'cname':'airwave',
                 'cbyte':(charrange,(15,30))},  
                {'cname':'species',
                 'cbyte':(charrange,(30,36))},
                {'cname':'loggf',
                 'cbyte':(charrange,(36,44))},
                {'cname':'landeff',
                 'cbyte':(charrange,(94,100)),
                 'cnull':'99.00'},
                {'cname':'gammarad',
                 'cbyte':(charrange,(100,107)),
                 'cnull':'0.0'},
                {'cname':'gammastark',
                 'cbyte':(charrange,(107,114)),
                 'cnull':'0.0'},
                {'cname':'gammawaals',
                 'cbyte':(charrange,(114,122)),
                 'cnull':'0.0'},
                {'cname':'srctag',
                 'cbyte':(charrange,(218,225))},
                {'cname':'acflag',
                 'cbyte':(charrange,(225,226))},
                {'cname':'accur',
                 'cbyte':(charrange,(226,236))},
                {'cname':'comment',
                 'cbyte':(charrange,(236,252))},
                {'cname':'wave_ref',
                 'cbyte':(charrange,(252,256))},
                {'cname':'loggf_ref',
                 'cbyte':(charrange,(256,260))},
                {'cname':'lande_ref',
                 'cbyte':(charrange,(268,272))},
                {'cname':'gammarad_ref',
                 'cbyte':(charrange,(272,276))},
                {'cname':'gammastark_ref',
                 'cbyte':(charrange,(276,280))},
                {'cname':'gammawaals_ref',
                 'cbyte':(charrange,(280,284))},
                {'cname':'upstateid',
                 'cbyte':(makeValdUpperStateKey,())},
                {'cname':'lostateid',
                 'cbyte':(makeValdLowerStateKey,())},
                {'cname':'upstate',
                 'cbyte':(makeValdUpperStateKey,()),
                 'foreignpk':'charid'},
                {'cname':'lostate',
                 'cbyte':(makeValdLowerStateKey,()),
                 'foreignpk':'charid'},
                ],
        },
        {'model':valdmodel.State,
         'fname':'/vald/myterms.dat',
         'headlines':0,
         'commentchar':'#',
         'updatematch':'charid',
         'columns':[\
                {'cname':'charid',
                 'cbyte':(bySepNr,(0,';'))},
                {'cname':'J',
                 'cbyte':(bySepNr,(1,';')),
                 'cnull':'X',},
                {'cname':'L',
                 'cbyte':(bySepNr,(2,';')),
                 'cnull':'X',},
                {'cname':'S',
                 'cbyte':(bySepNr,(3,';')),
                 'cnull':'X',},
                {'cname':'P',
                 'cbyte':(bySepNr,(4,';')),
                 'cnull':'X',},
                {'cname':'J1',
                 'cbyte':(bySepNr,(5,';')),
                 'cnull':'X',},
                {'cname':'J2',
                 'cbyte':(bySepNr,(6,';')),
                 'cnull':'X',},
                {'cname':'K',
                 'cbyte':(bySepNr,(7,';')),
                 'cnull':'X',},
                {'cname':'S2',
                 'cbyte':(bySepNr,(8,';')),
                 'cnull':'X',},
                {'cname':'Jc',
                 'cbyte':(bySepNr,(9,';')),
                 'cnull':'X',},
 
                ] # end column list
         }, # end dictionay for last table
        ], # end table list
   }  # end config dict


