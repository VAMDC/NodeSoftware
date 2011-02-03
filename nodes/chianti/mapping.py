# Mapping file for MyNode importing

# import models and help functions.
from chianti.node import models
from linefuncs import *

# the names of the input files
basepath = "/home/guy/NodeSoftware/nodes/chianti/raw-data/"
file1 = basepath + "chianti_data_v6_e.txt"

mapping = [
   {'model' : 'species',
    'fname' : file1,
    'commentchar' : '%',
    'headlines' : 1,
    'linemap' : [
        {'cname' : 'ioncharge',
         'cbyte' : bySepNr(2, '|')}
         ] }
   ]
