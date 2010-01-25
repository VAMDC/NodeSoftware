#!/usr/bin/env python

import urllib
import simplejson as j

url="http://localhost:8080/query"

data={'table': 'dummy1','columns':'id,c1,c2,c3','hurz':'bla bla'}
#'where':'id <15',,'order':'m6'
data=urllib.urlencode(data)

response = urllib.urlopen(url,data)
data=j.load(response)
response.close()

for d in data:
    for k in d.keys():
        print '%s: %s'%(k,d[k])
    print
