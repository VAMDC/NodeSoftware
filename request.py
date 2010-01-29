#!/usr/bin/env python
"""

request.py

Make a simple HTTP POST request wich contains a data request. 
Get back the reply and print the data to the terminal.

Make sure server.py runs on the same machine, before running
this script.

"""
import urllib
import simplejson as j

# where to send the request
url="http://localhost:8080/query"

# server.py for the time being understands the keywords
# "table", "columns", "where" and "order". Anything else
# is ignored.

data={'table': 'dummy1','columns':'id,c1,c2,c3','hurz':'bla bla'}
#data={'table': 'merged','columns':'m2,m6','hurz':'bla bla'}
#'where':'id <15',,'order':'m6'

data=urllib.urlencode(data)
response = urllib.urlopen(url,data) # making the actual request

data=j.load(response)
response.close()

for d in data:
    for k in d.keys():
        print '%s: %s'%(k,d[k])
    print
