#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

routines for querying the registry

"""

#REL_REG='http://registry.vamdc.eu/registry-11.12/services/RegistryQueryv1_0'
REL_REG='http://registry.vamdc.eu/registry-12.07/services/RegistryQueryv1_0'
DEV_REG='http://casx019-zone1.ast.cam.ac.uk/registry/services/RegistryQueryv1_0'
REL_REG='http://registry.vamdc.eu/registry-12.07/services/RegistryQueryv1_0'

REGURL=DEV_REG
REGURL=REL_REG
REGURL='http://casx019-zone1.ast.cam.ac.uk/registry/services/RegistryQueryv1_0'
WSDL=REGURL+'?wsdl'

# this is a copy of the URL above but with
# schema locations fixed:
#WSDL = 'http://tmy.se/t/devreg_wsdl.xml'

from suds.client import Client

def getNodeList():

#    d = RegistryDoctor()
    client = Client(WSDL) #,doctor=d)

    qr="""declare namespace ri='http://www.ivoa.net/xml/RegistryInterface/v1.0';
<nodes>
{
   for $x in //ri:Resource
   where $x/capability[@standardID='ivo://vamdc/std/VAMDC-TAP']
   and $x/@status='active'
   and $x/capability[@standardID='ivo://vamdc/std/VAMDC-TAP']/versionOfStandards='12.07'
   return  <node><title>{$x/title/text()}</title><url>{$x/capability[@standardID='ivo://vamdc/std/VAMDC-TAP']/interface/accessURL/text()}</url></node>   
}
</nodes>"""


    v=client.service.XQuerySearch(qr)
    nameurls=[]
    for node in v.node:
        # take only the first url
        try:
            url = node.url.split(" ")[0]
        except:
            url = None
            
	nameurls.append({\
			'name':node.title,
    			'url':url,
			})
    return nameurls

if __name__ == '__main__':
    print getNodeList()
