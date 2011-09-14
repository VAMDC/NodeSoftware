#!/usr/bin/env python
# -*- coding: utf-8 -*-
# validate_xsams.py

# Christian Hill, 14/9/11
# Download the XSAMS for sources, states and transitions of a single
# molecule and check that it validates against the released Schema.

import os
import sys
import argparse
from subprocess import call

HOME = os.getenv('HOME')
xsd_file = os.path.join(HOME, 'research/VAMDC/XSAMS/release-0.2/xsams.xsd')

# command line arguments:
parser = argparse.ArgumentParser(description='Validate the XSAMS produced'
            ' by the node for a single molecular species')
parser.add_argument('-l', '--local', dest='local', action='store_const',
        const=True, default=False,
        help='make the query of the localhost server')
parser.add_argument('molec_name', metavar='<molecule name>',
        help='the name of the molecule')
args = parser.parse_args()
local = args.local
molec_name = args.molec_name

url_prefix = 'http://vamdc.mssl.ucl.ac.uk/node/hitran/tap/sync/'
if local:
   url_prefix = 'http://127.0.0.1:8000/tap/sync/' 

query = 'REQUEST=doQuery&LANG=VSS2&FORMAT=XSAMS&QUERY=SELECT%%20ALL%%20'\
        'WHERE%%20MoleculeChemicalName="%s"' % molec_name

url = '%s?%s' % (url_prefix, query)
print url

# get the XSAMS using curl and send it to the file <molec_name>.xsams
xsams_name = '%s.xsams' % molec_name
fo = open(xsams_name, 'w')
call(['curl', '-L', url], stdout=fo)
fo.close()

ret = call(['validate.py', xsd_file, xsams_name])
print 'return code was:',ret

