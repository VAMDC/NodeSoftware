#!/usr/bin/env python

import urllib2
import sys

TAPURL = 'http://vamdc.fysast.uu.se:8080/node/vald/tap/sync'
QUERY = '?FORMAT=XSAMS&LANG=VSS2&QUERY='
QUERY += urllib2.quote(sys.argv[1])

class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"

try: response = urllib2.urlopen(HeadRequest(TAPURL + QUERY))
except urllib2.HTTPError,e:
    print e
else:
    print response.info()
