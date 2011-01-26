# import the "line functions" that
# extract data in various ways from
# a line in the input file
from imptools.linefuncs import *

mapping = [ \
    # Reading some columns from a fixed-record-length file
    {'outfile':'species.dat',
     'infiles':'yourspecieslist.file',
     'headlines':0,
     'commentchar':'#',
     'linemap':[
            {'cname':'id',
             'cbyte':(charrange, 0,7)},
            {'cname':'name',
             'cbyte':(charrange, 9,19)},
            {'cname':'ion',
             'cbyte':(charrange, 20,22)},
            {'cname':'mass',
             'cbyte':(charrange, 23,30)},
            {'cname':'massno',
             'cbyte':(charrange2int, 23,30)},
           ],
     }, # end of definition for species file

    # Reading two files at a time where the second has two lines
    # for each one in the first.
    {'outfile':'states.dat',    
     'infiles': ('statesfile1','statesfile2'),
     'headlines':(2, 0),
     'commentchar': ('#', '#'),
     'linestep':(1, 2),
     'lineoffset':(0,1),
     'errline':("Unknown", "Unknown"),
     'linemap':[
            {'cname':'id',
             'cbyte':(merge_cols,
                      (30,36), (170,172), (77,82), (172,218), (63,77))}, 
            {'cname':'species',
             'cbyte':(charrange, 30,36)},
            {'cname':'energy',
             'cbyte':(charrange, 63,77)},

            # the following values are read from the second file
            {'cname':'j',
             'filenum':1,
             'cbyte':(get_term_val,1),
             'cnull':'X',},
            {'cname':'l',
             'filenum':1,
             'cbyte':(get_term_val,2),
             'cnull':'X',},
            {'cname':'s',
             'filenum':1,
             'cbyte':(get_term_val,3),
             'cnull':'X',},
            ]
     }, # end of states
] # list of mappings ends
