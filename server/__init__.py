import simple
"""
Tools to query the TAP-interface of DSA/catalog.
It's a asynchronous request and the replies are XML
documents (that can be tranformed into html).

The scripts sends a (hardcoded) request to my
DSA/catalog installation with VALD data. It then
tells DSA to run the query, checks if it has completed
and fetches the result.

Not yet working: read the result into ATPy's implementation
of VOTable.

"""

# don't use a proxy
from os import environ,unlink,fdopen
environ["http_proxy"]=''

import urllib

from time import sleep
import atpy
from StringIO import StringIO
import threading

from tempfile import mkstemp
def mktmp():
    fd,name=mkstemp()
    return fdopen(fd,'w'),name

from tapclass import *
