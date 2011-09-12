#!/usr/bin/env python

import sys
import requests
from multiprocessing import Pool
from vamdc.other.registry import getNodeList

try:
    QUERY = sys.argv[1]
except:
    print "Please give the complete query string as an argument, in double quotes."
    sys.exit(1)

PARAMS = {\
    'QUERY':QUERY,
    'FORMAT':'XSAMS',
    'LANG':'VSS2'
    }

def headreq(nodes):
    return requests.head(nodes['url']+'sync',params=PARAMS,timeout=5)

def run():
    nodes = getNodeList()
    n = len(nodes)
    pool = Pool(processes=n)

    pardict = {'url':[node['url']+'sync' for node in nodes],
               'params':(PARAMS,)*n,
               'timeout':(5,)*n
            }

    res = pool.map(headreq,nodes)
    print res

if __name__ == '__main__':
    run()
