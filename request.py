#!/usr/bin/env python

import urllib

url="http://localhost:8080/query"

data={'query': 'FROM bla SELECT *','bla':'hurz'}
data=urllib.urlencode(data)

response = urllib.urlopen(url,data)
print response.read()
response.close()
