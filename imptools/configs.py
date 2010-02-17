#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
config dictionaries and corresponding functions

"""

### FUCTIONS TO APPLY TO DATA AFTER READING
def fixvald(data):
    return data

def fixrefs(data):
    return data

def fixnothing(data):
    return data

### CONFIG "FILES"
dummycfg = {\
    'tables':[\
        {'fname':'dummy.dat',
         'delim':' ',
         'tname':'dummy1',
         'headlines':0,
         'commentchar':'',
         'function':fixnothing,
         'columns':[\
                {'cname':'c1',
                 'cfmt':'d',
                 'ccom':'column 1',
                 'cunit':None,
                 'cbyte':0,
                 'cnull':None,
                 'ctype':'UNSIGNED INT',
                 },
                {'cname':'c2',
                 'cfmt':'.2f',
                 'ccom':'column 2',
                 'cunit':'Å',
                 'cbyte':1,
                 'cnull':0.0,
                 'ctype':'FLOAT',
                 },
                ]
         },
        {'fname':'dummy.dat',
         'delim':' ',
         'tname':'dummy2',
         'headlines':0,
         'commentchar':'',
         'function':fixnothing,
         'columns':[\
                {'cname':'c1',
                 'cfmt':'d',
                 'ccom':'column 1',
                 'cunit':None,
                 'cbyte':0,
                 'cnull':None,
                 'ctype':'UNSIGNED INT',
                 },
                {'cname':'c2',
                 'cfmt':'.2f',
                 'ccom':'column 2',
                 'cunit':'eV',
                 'cbyte':2,
                 'cnull':0.0,
                 'ctype':'FLOAT',
                 },
                ],
         'relations':[{\
                'table1':'dummy1',
                'column1':'c1',
                'table2':'dummy2',
                'column2':'c1'
                }]
      
         }
        ]
    }

valdcfg={\
    'tables':[\
        {'tname':'merged',
         'fname':'merged.dat',
         'delim':'fixedcol', # delimiter character or 'fixedcol'
         'headlines':2,      # this many lies ignored in file header
         'commentchar':'#',   # lines that start with this are ignored
         'function':fixvald,  # to be applied on each line
         'columns':[\
                {'cname':'wavel',     # column name
                 'cfmt':'.5f',       # print format
                 'ccom':'Wavelength', # description
                 'cunit':'Å',         # Units
                 'cbyte':(0,13),       # place in the line
                 'cnull':None,        # value to be converted to NULL
                 'ctype':'FLOAT', # data format in database
                 },
                {'cname':'atomic',
                 'cfmt':'d',
                 'ccom':'Atomic number',
                 'cunit':None,
                 'cbyte':(13,16),
                 'cnull':None,
                 'ctype':'TINYINT UNSIGNED'},
                {'cname':'ion',
                 'cfmt':'d',
                 'ccom':'Ionization stage, 0 is neutral',
                 'cunit':None,
                 'cbyte':(17,19),
                 'cnull':None,
                 'ctype':'SMALLINT UNSIGNED'},
                {'cname':'ref4',
                 'cfmt':'d',
                 'ccom':'reference to VALD source file, i.e. reference',
                 'cunit':None,
                 'cbyte':(135,139),
                 'cnull':None,
                 'ctype':'SMALLINT UNSIGNED'},
                {'cname':'ref5',
                 'cfmt':'d',
                 'ccom':'reference to VALD source file, i.e. reference',
                 'cunit':None,
                 'cbyte':(139,143),
                 'cnull':None,
                 'ctype':'SMALLINT UNSIGNED'},
                {'cname':'ref6',
                 'cfmt':'d',
                 'ccom':'reference to VALD source file, i.e. reference',
                 'cunit':None,
                 'cbyte':(143,147),
                 'cnull':None,
                 'ctype':'SMALLINT UNSIGNED'},
                {'cname':'ref7',
                 'cfmt':'d',
                 'ccom':'reference to VALD source file, i.e. reference',
                 'cunit':None,
                 'cbyte':(147,151),
                 'cnull':None,
                 'ctype':'SMALLINT UNSIGNED'},
                {'cname':'ref8',
                 'cfmt':'d',
                 'ccom':'reference to VALD source file, i.e. reference',
                 'cunit':None,
                 'cbyte':(151,155),
                 'cnull':None,
                 'ctype':'SMALLINT UNSIGNED'},
                {'cname':'ref9',
                 'cfmt':'d',
                 'ccom':'reference to VALD source file, i.e. reference',
                 'cunit':None,
                 'cbyte':(155,159),
                 'cnull':None,
                 'ctype':'SMALLINT UNSIGNED'},
                ]
         },
        {'tname':'refs',
         'fname':'all.cfg',
         'delim':',',
         'headlines':1,
         'commentchar':';',
         'function':fixrefs,
         'columns':[\
                {'cname':'srcfile',
                 'cfmt':'s',
                 'ccom':'vald source file name',
                 'cunit':None,
                 'cbyte':0,
                 'cnull':None,
                 'ctype':'VARCHAR(64)'},
                {'cname':'d1',
                 'cfmt':'d',
                 'ccom':'',
                 'cunit':None,
                 'cbyte':1,
                 'cnull':None,
                 'ctype':'TINYINT UNSIGNED'},
                {'cname':'d2',
                 'cfmt':'d',
                 'ccom':'',
                 'cunit':None,
                 'cbyte':2,
                 'cnull':None,
                 'ctype':'TINYINT UNSIGNED'},
                {'cname':'d3',
                 'cfmt':'d',
                 'ccom':'',
                 'cunit':None,
                 'cbyte':3,
                 'cnull':None,
                 'ctype':'TINYINT UNSIGNED'},
                {'cname':'d4',
                 'cfmt':'d',
                 'ccom':'',
                 'cunit':None,
                 'cbyte':4,
                 'cnull':None,
                 'ctype':'TINYINT UNSIGNED'},
                {'cname':'d5',
                 'cfmt':'d',
                 'ccom':'',
                 'cunit':None,
                 'cbyte':5,
                 'cnull':None,
                 'ctype':'TINYINT UNSIGNED'},
                {'cname':'d6',
                 'cfmt':'d',
                 'ccom':'',
                 'cunit':None,
                 'cbyte':6,
                 'cnull':None,
                 'ctype':'TINYINT UNSIGNED'},
                {'cname':'d7',
                 'cfmt':'d',
                 'ccom':'',
                 'cunit':None,
                 'cbyte':7,
                 'cnull':None,
                 'ctype':'TINYINT UNSIGNED'},
                {'cname':'d8',
                 'cfmt':'d',
                 'ccom':'',
                 'cunit':None,
                 'cbyte':8,
                 'cnull':None,
                 'ctype':'TINYINT UNSIGNED'},
                {'cname':'d9',
                 'cfmt':'d',
                 'ccom':'',
                 'cunit':None,
                 'cbyte':9,
                 'cnull':None,
                 'ctype':'TINYINT UNSIGNED'},
                {'cname':'d10',
                 'cfmt':'d',
                 'ccom':'',
                 'cunit':None,
                 'cbyte':10,
                 'cnull':None,
                 'ctype':'TINYINT UNSIGNED'},
                {'cname':'d11',
                 'cfmt':'d',
                 'ccom':'',
                 'cunit':None,
                 'cbyte':11,
                 'cnull':None,
                 'ctype':'TINYINT UNSIGNED'},
                {'cname':'d12',
                 'cfmt':'d',
                 'ccom':'',
                 'cunit':None,
                 'cbyte':12,
                 'cnull':None,
                 'ctype':'TINYINT UNSIGNED'},
                {'cname':'srcdescr',
                 'cfmt':'s',
                 'ccom':'vald source comment',
                 'cunit':None,
                 'cbyte':13,
                 'cnull':None,
                 'ctype':'VARCHAR(128)'},
                ]
         },
        ],
    'relations':[ # descibe which table.column is related to another
        {'table1':'merged',
         'column1':'ref1',
         'table2':'meta',
         'column2':'d1',
         }
        ]
    }

