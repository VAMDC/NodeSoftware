#!/usr/bin/env python

from string import strip
from sys import exit

#v=open('vald3.dat')
#q=open('terms500.dat')
v=open('/vald/vald3_atomic_obs.dat')
out=open('/vald/states.dat','w')


from vamdc.imptools import *

upperconf=        {'model':valdmodel.State,   ######### FIRST PASS FOR THE UPPER STATES
         'fname':'/vald/vald3.dat',
         'headlines':2,       
         'commentchar':'#',   
         'columns':[          
                {'cname':'charid',  
                 'cbyte':(makeValdUpperStateKey,())},
                {'cname':'species',
                 'cbyte':(charrange,(30,36))},
                {'cname':'energy',
                 'cbyte':(charrange,(63,77))},
                #{'cname':'j',   # J comes later again with the other q-numbers
                # 'cbyte':(charrange,(77,82)),},
                {'cname':'lande',
                 'cbyte':(charrange,(88,94)),
                 'cnull':'99.00'},
                {'cname':'coupling',
                 'cbyte':(charrange,(170,172))},
                {'cname':'term',
                 'cbyte':(charrange,(172,218))},
                {'cname':'energy_ref',
                 'cbyte':(charrange,(264,268))},
                {'cname':'lande_ref',
                 'cbyte':(charrange,(268,272))},
                {'cname':'level_ref',
                 'cbyte':(charrange,(284,288))},
                ]
         }
lowerconf=        {'model':valdmodel.State, ######### SECOND PASS FOR THE LOWER STATES
         'fname':'/vald/vald3.dat',
         'headlines':2,    
         'commentchar':'#',   
         'columns':[          
                {'cname':'charid',  
                 'cbyte':(makeValdLowerStateKey,())},
                {'cname':'species',
                 'cbyte':(charrange,(30,36))},
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
                 'cbyte':(charrange,(260,264))},
                {'cname':'lande_ref',
                 'cbyte':(charrange,(268,272))},
                {'cname':'level_ref',
                 'cbyte':(charrange,(284,288))},
                ],
        }


v.readline()
v.readline()

for line in v:

    for conf in [upperconf,lowerconf]:
        for colconf in conf['columns']:
            fu=colconf['cbyte'][0]
            args=colconf['cbyte'][1]
            d=fu(line,*args)
            if d: out.write(d)
            out.write(';')
        out.write('\n')
