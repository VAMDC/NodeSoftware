#!/usr/bin/env python

import gevent
from gevent import monkey
monkey.patch_all()

import sys
import requests
from vamdc.other.registry import getNodeList

try:
    QUERY = sys.argv[1]
except:
    print "Please give a query string as an argument, in double quotes."
    sys.exit(1)

PARAMS = {\
    'QUERY':QUERY,
    'FORMAT':'XSAMS',
    'LANG':'VSS2'
    }
TIMEOUT = 5

def headreq(node):
    return requests.head(node['url']+'sync',params=PARAMS,timeout=TIMEOUT)

def run():
    nodes = getNodeList()
    jobs = [gevent.spawn(headreq,node) for node in nodes]
    gevent.joinall(jobs, timeout=TIMEOUT+1)
    results = [job.value for job in jobs if job.value]
    for result in results:
        if result.status_code != 200: continue
        print '\n',result.url
        for head in result.headers:
            if head.lower().startswith('vamdc'):
                print head, result.headers[head]

if __name__ == '__main__':
    run()
