#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Defines a mapping dictionary that maps between data columns 
in raw ascii data files and defines how they should be stored
into a relational (django) database.

A file like this should be created for every unique database.
It should normally contain a global list, conventionally named
'mappings', that define how data fields are to be translated into
django fields. To properly map, a custom processor also probably
has to be constructed in dbhelper as well.

"""

from string import strip
import os
import pdb

#
# Utility functions applied to data after reading
#

def charrange(linedata, start, end, filenum=0):
    """
    Cut out part of a line of texts based on indices
    """
    try:
        return strip(linedata[filenum][start:end])
    except Exception, e:
        print "charrange skipping '%s': %s" % (linedata, e)
    
def charrange2int(linedata, start, end, filenum=0):
    return int(round(float(charrange(linedata[filenum], start, end))))

def bySepNr(linedata, number, sep=',',filenum=0):
    """
    Split a text line by sep argument and return
    the split section with given number
    """
    try:
        return strip(linedata[filenum].split(sep)[number])
    except Exception, e:
        print "bySepNr skipping line '%s': %s" % (linedata, e)

def chainCmds(linedata, *linefuncs):
    """
    This command allows for chaining together several line functions in
    sequence. The results of the first function will be passed to the second
    one etc.

    linefuncs should be a list [(func1, (arg1,arg2,...)), (func2,(arg1,arg2,..)),...]
    """

    data = linedata
    for func, args in linefuncs:
        data = [func(data, *args)]
    if data:
        return data[0]
    print "chainCommands skipping line." 
         
def idFromLine(linedata, sep, *linefuncs):
    """
    Extract strings from a line in order to build a unique id-string,
    using one or more line functions to extract parts of a line and
    paste them together with a separator given by 'sep'.
    The line functions must be stored as tuples (func, (arg1,arg2,..)). 

    Example of call:
      idFromLine('-', (bySepNr,(3,';'), (charrange2int,(45,67))) )    
    """
    #print linedata
    #pdb.set_trace()
    if not sep:
        sep = "-"
    dbref = []
    for func, args in linefuncs:
        string = str(func(linedata, *args)).strip()        
        if not string:
            string = sep
        #print string 
        dbref.append(string)
    print sep.join(dbref)
    return sep.join(dbref)
    
# 
# Create a config, a list of file definitions. Each entry in this
# list is a dictionary describing an input ascii file to build from.
# Each file dict definition supports the following keys
#   model       (django.db.model) - which Django model this file should populate
#   fname       (str)             - the file name
#   headlines   (int)             - number of header lines to skip   
#   commentchar (str)             - comment symbol (like #, ; etc) used in file
#   updatematch (str)             - TODO
#   cnull       (str/value)       - if defined, defines a str/value that should be ignored (e.g. 'N/A')
#   columns     (dict)
#                cname (str)      - collumn name
#                cbyte (tup)      - method to process the line and tuple to be fed to this method
#                references (tup) - which django model referenced by this collumn, and which field name
# 

# Import models for one particular node
os.environ['DJANGO_SETTINGS_MODULE']="vamdc.DjVALD.settings"
from DjVALD.node import models as valdmodel

# Base directory for the data files

base = "/vald/"
#base = "/home/samreg/vamdc-git/imptools/vald_raw/"

# species_list_file = base + 'VALD_list_of_species'
# vald_cfg_file = base + 'vald3_test.cfg'
# states_file = base + 'states_preprocessed.dat'
# transitions_file = base + 'transitions_preprocessed.dat'
# terms_file = base + 'terms_preprocessed.dat'
# publications_file = base + "publications_preprocessed.dat"

species_list_file = base + 'VALD_list_of_species'
vald_cfg_file = base + 'vald3_test.cfg'
states_file = base + 'states_u.dat'
vald_file = base + 'vald3_500.dat'
terms_file = base + 'terms'
publications_file = base + "publications_preprocessed.dat"

mapping = [
    # Populate Species model, using the species input file.
    {'model':valdmodel.Species,
     'fname':species_list_file,
     'headlines':0,
     'commentchar':'#',
     'linemap':[
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
     }, # end of definition for species file

    # Populate Publication model with 
    # pre-processed bibtex data file
    {'model':valdmodel.Publication,    
     'fname':publications_file,
     'headlines':0,        
     'commentchar':'#',    
     'linemap':[           
            {'cname':'dbref',
             'cbyte':(bySepNr, (0,'||')),},  
            {'cname':'bibref',
             'cbyte':(bySepNr, (1,'||')),},  
            {'cname':'author',
             'cbyte':(bySepNr, (2,'||')),},  
            {'cname':'bibtex',
             'cbyte':(bySepNr, (3,'||')),},            
          ], 
      }, # end of bibtex publication data

    # Populate Source model from vald_cfg file
    {'model':valdmodel.Source,
     'fname':vald_cfg_file,
     'headlines':1,
     'commentchar':';',
     'linemap':[
            {'cname':'pk',
             'cbyte':(bySepNr,(1,))},
            {'cname':'srcfile',
             'cbyte':(bySepNr,(0,))},
            {'cname':'speclo',
             'cbyte':(bySepNr,(2,)),
             'references':(valdmodel.Species,'pk')},
            {'cname':'spechi',
             'cbyte':(bySepNr,(3,)),
             'references':(valdmodel.Species,'pk')},
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
    }, # end of definition for vald_cnf file

# State model read from states_file -upper states
    # (first section) 
    {'model':valdmodel.State,    
     'fname': (vald_file, terms_file),
     'headlines':(2, 0),
     'commentchar': ('#', '#'),
     'linestep':(1, 2),
     'lineoffset':(0,1),
     'errline':("Unknown", "Unknown"),
     'linemap':[
            {'cname':'charid',        #species,coup,jnum,term,energy (upper states)             
             'cbyte':(idFromLine,('-',(charrange,(30,36)),
                                      (charrange,(170,172)),
                                      (charrange,(77,82)),
                                      (charrange,(172,218)),
                                      (charrange,(63,77)) ))},           
            {'cname':'species',
             'cbyte':(charrange,(30,36)),
             'references':(valdmodel.Species,'pk')},
            {'cname':'energy',
             'cbyte':(charrange,(63,77))},
            #{'cname':'j',   
            # 'cbyte':(charrange,(77,82)),},
            {'cname':'lande',
             'cbyte':(charrange,(88,94)),
             'cnull':'99.00'},
            {'cname':'coupling',
             'cbyte':(charrange,(170,172))},
            {'cname':'term',
             'cbyte':(charrange,(172,218))},
            {'cname':'energy_ref',
             'cbyte':(charrange,(264,268)),
             'references':(valdmodel.Source,'pk')},
            {'cname':'lande_ref',
             'cbyte':(charrange,(268,272)),
             'references':(valdmodel.Source,'pk')},
            {'cname':'level_ref',
             'cbyte':(charrange,(284,288)),
             'references':(valdmodel.Source,'pk')},
            # these are read from term file
            {'cname':'J',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(1,',')))),
             'cnull':'X',},
            {'cname':'L',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(2,',')))),         
             'cnull':'X',},
            {'cname':'S',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(3,',')))), 
             'cnull':'X',},
            {'cname':'P',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(4,',')))),
             'cnull':'X',},
            {'cname':'J1',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(5,',')))),
             'cnull':'X',},
            {'cname':'J2',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(6,',')))),
             'cnull':'X',},
            {'cname':'K',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(7,',')))),
             'cnull':'X',},
            {'cname':'S2',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(8,',')))),
             'cnull':'X',},
            {'cname':'Jc',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(9,',')))),
             'cnull':'X',},
            ]
     }, # end of State-model creation - upper states
    
    # State model read from states_file - lower states
    # (second section)
    {'model':valdmodel.State,
     'fname':(vald_file, terms_file),
     'headlines':(2, 0), 
     'commentchar':('#','#'),
     'linestep':(1, 2),
     'updatematch':'charid',
     'errline':("Unknown", "Unknown"),
     'linemap':[
            {'cname':'charid',         #species,coup,jnum,term,energy (lower states)
             'cbyte':(idFromLine,('-',(charrange,(30,36)),
                                      (charrange,(170,172)), # use upper state as id
                                      (charrange,(77,82)),
                                      (charrange,(172,218)),
                                      (charrange,(63,77)) ))},           
             #'cbyte':(idFromLine,('-',(charrange,(30,36)),
             #                         (charrange,(122,124)),
             #                         (charrange,(58,63)),
             #                         (charrange,(124,170)),
             #                         (charrange,(44,58)) ))},            
            {'cname':'species',
             'cbyte':(charrange,(30,36)),
             'references':(valdmodel.Species,'pk')},
            {'cname':'energy',
             'cbyte':(charrange,(44,58))},
            #{'cname':'j',
            # 'cbyte':(charrange,(58,63))},
            {'cname':'lande',
             'cbyte':(charrange,(82,88)),
             'cnull':'99.00'},
            {'cname':'coupling',
             'cbyte':(charrange,(122,124))},
            {'cname':'term',
             'cbyte':(charrange,(124,170))},
            {'cname':'energy_ref',
             'cbyte':(charrange,(264,268)),
             'references':(valdmodel.Source,'pk')},
            {'cname':'lande_ref',
             'cbyte':(charrange,(268,272)),
             'references':(valdmodel.Source,'pk')},
            {'cname':'level_ref',
             'cbyte':(charrange,(284,288)),
             'references':(valdmodel.Source,'pk')},
            # these are read from term file
            {'cname':'J',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(1,',')))),
             'cnull':'X',},
            {'cname':'L',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(2,',')))),         
             'cnull':'X',},
            {'cname':'S',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(3,',')))), 
             'cnull':'X',},
            {'cname':'P',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(4,',')))),
             'cnull':'X',},
            {'cname':'J1',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(5,',')))),
             'cnull':'X',},
            {'cname':'J2',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(6,',')))),
             'cnull':'X',},
            {'cname':'K',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(7,',')))),
             'cnull':'X',},
            {'cname':'S2',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(8,',')))),
             'cnull':'X',},
            {'cname':'Jc',
             'cbyte':(chainCmds, ((bySepNr,(2,':',1)),
                                  (bySepNr,(9,',')))),
             'cnull':'X',},
            ]
     }, # end of State model creation - lower states
   
    # Transition model, using the vald file    
    {'model':valdmodel.Transition,
     'fname':vald_file,
     'headlines':2,
     'commentchar':'#',
     'linemap':[
            {'cname':'vacwave',
             'cbyte':(charrange,(0,15))},
            {'cname':'airwave',
             'cbyte':(charrange,(15,30))},
            {'cname':'species',
             'cbyte':(charrange,(30,36)),
             'references':(valdmodel.Species,'pk')},
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
             'cbyte':(charrange,(218,225)),
             'references':(valdmodel.Publication,'dbref','skiperror')},
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
            {'cname':'upstateid',     #species,coup,jnum,term,energy   
             'cbyte':(idFromLine,('-',(charrange,(30,36,)),
                                      (charrange,(170,172)),
                                      (charrange,(77,82)),
                                      (charrange,(172,218)),
                                      (charrange,(63,77)) ))},
            {'cname':'lostateid',
             'cbyte':(idFromLine,('-',(charrange,(30,36)),
                                      (charrange,(122,124)),
                                      (charrange,(58,63)),
                                      (charrange,(124,170)),
                                      (charrange,(44,58)) ))},
            {'cname':'upstate',
             'cbyte':(idFromLine,('-',(charrange,(30,36,)),
                                      (charrange,(170,172)),
                                      (charrange,(77,82)),
                                      (charrange,(172,218)),
                                      (charrange,(63,77)) )),
             'references':(valdmodel.State,'charid')},
            {'cname':'lostate',
             'cbyte':(idFromLine,('-',(charrange,(30,36)),
                                      (charrange,(122,124)),
                                      (charrange,(58,63)),
                                      (charrange,(124,170)),
                                      (charrange,(44,58)) )),
             'references':(valdmodel.State,'charid')},


     # {'cname':'upstateid',
            #  'cbyte':(makeValdUpperStateKey,())},
            # {'cname':'lostateid',
            #  'cbyte':(makeValdLowerStateKey,())},
            # {'cname':'upstate',
            #  'cbyte':(makeValdUpperStateKey,()),
            #  'references':(valdmodel.State,'charid')},
            # {'cname':'lostate',
            #  'cbyte':(makeValdLowerStateKey,()),
            #  'references':(valdmodel.State,'charid')},
            ],
    } # end of vald file def

] # end of vald3 mapping file def list



# mapping = [
#     # species file 
#     {'model':valdmodel.Species,     
#      'fname':species_list_file,
#      'headlines':0,   
#      'commentchar':'#',   
#      'columns':[          
#             {'cname':'pk',  
#              'cbyte':(charrange,(0,7))},   
#             {'cname':'name',  
#              'cbyte':(charrange,(9,19))},   
#             {'cname':'ion',  
#              'cbyte':(charrange,(20,22))},   
#             {'cname':'mass',  
#              'cbyte':(charrange,(23,30))},   
#             {'cname':'massno',  
#              'cbyte':(charrange2int,(23,30))},   
#             {'cname':'ionen',  
#              'cbyte':(charrange,(31,40))},   
#             {'cname':'solariso',  
#              'cbyte':(charrange,(41,47))},   
#             {'cname':'ncomp',  
#              'cbyte':(charrange,(132,133))},   
#             {'cname':'atomic',  
#              'cbyte':(charrange,(134,136))},   
#             {'cname':'isotope',  
#              'cbyte':(charrange,(137,140))},   
#            ],
#      }, # end of definition for species file

#     # publication bibtex data file
#     {'model':valdmodel.Publication,    
#      'fname':publications_file,
#      'headlines':0,        
#      'commentchar':'#',    
#      'columns':[           
#             {'cname':'dbref',
#              'cbyte':(bySepNr, (0,'||')),},  
#             {'cname':'bibref',
#              'cbyte':(bySepNr, (1,'||')),},  
#             {'cname':'author',
#              'cbyte':(bySepNr, (2,'||')),},  
#             {'cname':'bibtex',
#              'cbyte':(bySepNr, (3,'||')),},            
#           ], 
#       }, # end of bibtex publication data

#     # vald_cfg file
#     {'model':valdmodel.Source,
#      'fname':vald_cfg_file,
#      'headlines':1,
#      'commentchar':';',
#      'columns':[\
#             {'cname':'pk',
#              'cbyte':(bySepNr,(1,))},
#             {'cname':'srcfile',
#              'cbyte':(bySepNr,(0,))},
#             {'cname':'speclo',
#              'cbyte':(bySepNr,(2,)),
#              'references':(valdmodel.Species,'pk')},
#             {'cname':'spechi',
#              'cbyte':(bySepNr,(3,)),
#              'references':(valdmodel.Species,'pk')},
#             {'cname':'listtype',
#              'cbyte':(bySepNr,(4,))},
#             {'cname':'r1',
#              'cbyte':(bySepNr,(5,))},
#             {'cname':'r2',
#              'cbyte':(bySepNr,(6,))},
#             {'cname':'r3',
#              'cbyte':(bySepNr,(7,))},
#             {'cname':'r4',
#              'cbyte':(bySepNr,(8,))},
#             {'cname':'r5',
#              'cbyte':(bySepNr,(9,))},
#             {'cname':'r6',
#              'cbyte':(bySepNr,(10,))},
#             {'cname':'r7',
#              'cbyte':(bySepNr,(11,))},
#             {'cname':'r8',
#              'cbyte':(bySepNr,(12,))},
#             {'cname':'r9',
#              'cbyte':(bySepNr,(13,))},
#             {'cname':'srcdescr',
#              'cbyte':(bySepNr,(14,)),},
#             ],
#     }, # end of definition for vald_cnf file

#     # reading from preprocessed files (create these with run/prepvald.py)   

#  # state file - this takes two passes, one for upper and one for lower state

#     {'model':valdmodel.State,   
#      'fname':states_file,
#      'headlines':0,     
#      'commentchar':'#',   
#      'columns':[          
#             {'cname':'charid',  
#              'cbyte':(bySepNr,(0,';'))},
#             {'cname':'species',
#              'cbyte':(bySepNr,(1,';')),
#              'references':(valdmodel.Species,'pk')},
#             {'cname':'energy',
#              'cbyte':(bySepNr,(2,';'))},
#             {'cname':'lande',
#              'cbyte':(bySepNr,(3,';')),
#              'cnull':'99.00'},
#             {'cname':'coupling',
#              'cbyte':(bySepNr,(4,';'))},
#             {'cname':'term',
#              'cbyte':(bySepNr,(5,';'))},
#             {'cname':'energy_ref',
#              'cbyte':(bySepNr,(6,';')),
#              'references':(valdmodel.Source,'pk')},
#             {'cname':'lande_ref',
#              'cbyte':(bySepNr,(7,';')),
#              'references':(valdmodel.Source,'pk')},
#             {'cname':'level_ref',
#              'cbyte':(bySepNr,(8,';')),
#              'references':(valdmodel.Source,'pk')}
#             ]
#      }, # end of state file    

#     # term file - preprocessed data from vald file 
#     {'model':valdmodel.State,
#      'fname':terms_file,
#      'headlines':0,
#      'commentchar':'#',
#      'updatematch':'charid', #don't create a new State - update an existing State object retrieved by charid
#      'columns':[\
#             {'cname':'charid',
#              'cbyte':(bySepNr,(0,';'))},
#             {'cname':'J',
#              'cbyte':(bySepNr,(1,';')),
#              'cnull':'X',},
#             {'cname':'L',
#              'cbyte':(bySepNr,(2,';')),
#              'cnull':'X',},
#             {'cname':'S',
#              'cbyte':(bySepNr,(3,';')),
#              'cnull':'X',},
#             {'cname':'P',
#              'cbyte':(bySepNr,(4,';')),
#              'cnull':'X',},
#             {'cname':'J1',
#              'cbyte':(bySepNr,(5,';')),
#              'cnull':'X',},
#             {'cname':'J2',
#              'cbyte':(bySepNr,(6,';')),
#              'cnull':'X',},
#             {'cname':'K',
#              'cbyte':(bySepNr,(7,';')),
#              'cnull':'X',},
#             {'cname':'S2',
#              'cbyte':(bySepNr,(8,';')),
#              'cnull':'X',},
#             {'cname':'Jc',
#              'cbyte':(bySepNr,(9,';')),
#              'cnull':'X',},
#             ]
#      }, # end of term def  

#     # transitions file - preprocessed data from vald file 
#     {'model':valdmodel.Transition,    
#      'fname':transitions_file,
#      'headlines':0,        
#      'commentchar':'#',    
#      'columns':[           
#             {'cname':'vacwave',
#              'cbyte':(bySepNr, (0,';'))},  
#             {'cname':'airwave',
#              'cbyte':(bySepNr,(1, ';'))},  
#             {'cname':'species',
#              'cbyte':(bySepNr,(2, ';')),
#              'references':(valdmodel.Species,'pk')},
#             {'cname':'loggf',
#              'cbyte':(bySepNr,(3, ';'))},
#             {'cname':'landeff',
#              'cbyte':(bySepNr,(4, ';')),
#              'cnull':'99.00'},
#             {'cname':'gammarad',
#              'cbyte':(bySepNr,(5, ';')),
#              'cnull':'0.0'},
#             {'cname':'gammastark',
#              'cbyte':(bySepNr,(6, ';')),
#              'cnull':'0.0'},
#             {'cname':'gammawaals',
#              'cbyte':(bySepNr,(7, ';')),
#              'cnull':'0.0'},
#             {'cname':'srctag',
#              'cbyte':(bySepNr,(8, ';')),
#              'references':(valdmodel.Publication,'dbref','skiperror')},
#             {'cname':'acflag',
#              'cbyte':(bySepNr,(9, ';'))},
#             {'cname':'accur',
#              'cbyte':(bySepNr,(10, ';'))},
#             {'cname':'comment',
#              'cbyte':(bySepNr,(11, ';'))},
#             {'cname':'wave_ref',
#              'cbyte':(bySepNr,(12, ';')),
#              'references':(valdmodel.Source,'pk')},
#             {'cname':'loggf_ref',
#              'cbyte':(bySepNr,(13, ';')),
#              'references':(valdmodel.Source,'pk')},
#             {'cname':'lande_ref',
#              'cbyte':(bySepNr,(14, ';')),
#              'references':(valdmodel.Source,'pk')},
#             {'cname':'gammarad_ref',
#              'cbyte':(bySepNr,(15, ';')),
#              'references':(valdmodel.Source,'pk')},
#             {'cname':'gammastark_ref',
#              'cbyte':(bySepNr,(16, ';')),
#              'references':(valdmodel.Source,'pk')},
#             {'cname':'gammawaals_ref',
#              'cbyte':(bySepNr,(17, ';')),
#              'references':(valdmodel.Source,'pk')},
#             {'cname':'upstateid',
#              'cbyte':(bySepNr, (18, ';'))},
#             {'cname':'lostateid',
#              'cbyte':(bySepNr, (19, ';'))},
#             {'cname':'upstate',
#              'cbyte':(bySepNr, (20, ';')),
#              'references':(valdmodel.State,'charid')},
#             {'cname':'lostate',
#              'cbyte':(bySepNr, (21, ';')),
#              'references':(valdmodel.State,'charid')},
#             ],
#      }, # end of transition file def
       
# ] # end of vald3 mapping file def list



