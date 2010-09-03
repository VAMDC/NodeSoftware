"""

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

# the submodules
import tap
import simple
