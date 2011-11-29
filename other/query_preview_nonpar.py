#!/usr/bin/env python
import sys
import requests
from vamdc.other.registry import getNodeList

TIMEOUT = 5
QUERY = sys.argv[1]
PARAMS = {'QUERY':QUERY, 'FORMAT':'XSAMS', 'LANG':'VSS2'}

nodes = getNodeList()

for node in nodes:
    result = requests.head(node['url']+'sync',
                params=PARAMS,timeout=TIMEOUT)
    if result.status_code != 200: continue
    print '\n*%s*'%node['name']
    for head in result.headers:
        if head.lower().startswith('vamdc'):
            print '%s: %s'%(head, result.headers[head])
    print result.url
