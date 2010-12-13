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
from os import environ
from sys import argv
environ["http_proxy"]=''

# where to send the request
fallbackurl="http://localhost:8081/query"

if len(argv) < 2: url=fallbackurl
else: url=argv[1]

# server.py for the time being understands the keywords
# "table", "columns", "where" and "order". Anything else
# is ignored.

# example for dummy data
data={'table': 'dummy1','columns':'c11,c12'}

# example for vald
#data={'table':'valddata','columns':'wavel,atomic,ion','order':'wavel'}

data=urllib.urlencode(data)
response = urllib.urlopen(url,data) # making the actual request
data=j.load(response)
response.close()

for d in data:
    for k in d.keys():
        print '%s: %s'%(k,d[k])
    print
