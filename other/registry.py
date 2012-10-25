#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

routines for querying the registry

"""

#REL_REG='http://registry.vamdc.eu/registry-11.12/services/RegistryQueryv1_0'
REL_REG='http://registry.vamdc.eu/registry-12.07/services/RegistryQueryv1_0'
DEV_REG='http://casx019-zone1.ast.cam.ac.uk/registry/services/RegistryQueryv1_0'
REGURL=REL_REG
WSDL=REGURL+'?wsdl'

# this is a copy of the URL above but with
# schema locations fixed:
#WSDL = 'http://tmy.se/t/devreg_wsdl.xml'

from suds.client import Client

def getNodeList():
    client = Client(WSDL)

    qr="""declare namespace ri='http://www.ivoa.net/xml/RegistryInterface/v1.0';
for $x in //ri:Resource
where $x/capability[@standardID='ivo://vamdc/std/VAMDC-TAP']
and $x/@status='active'
return ($x/capability[@standardID='ivo://vamdc/std/VAMDC-TAP']/interface/accessURL)"""

    v=client.service.XQuerySearch(qr)
    urls=[]
    while v:
        urls.append(v.pop(0)['value'])
    return urls



if __name__ == '__main__':
    print getNodeList()
