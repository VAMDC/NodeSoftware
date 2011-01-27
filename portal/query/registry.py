#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

routines for querying the registry

"""

#REL_REG='http://registry.vamdc.eu/vamdc_registry/services/RegistryQueryv1_0'
#DEV_REG='http://casx019-zone1.ast.cam.ac.uk/registry/services/RegistryQueryv1_0'
#REGURL=DEV_REG
#WSDL=REGURL+'?wsdl'

WSDL = 'http://www.tmy.se/t/devreg_wsdl.xml'

from suds.client import Client
from suds.xsd.doctor import Doctor
class RegistryDoctor(Doctor):    
    TNS = 'http://www.ivoa.net/wsdl/RegistrySearch/v1.0'
    def examine(self, node):
        tns = node.get('targetNamespace')
        # find a specific schema
        if tns != self.TNS:
            return
        for e in node.getChildren('element'):
            # find our response element
            if e.get('name') != 'XQuerySearchResponse':
                continue
            # fix the <xs:any/> by adding maxOccurs
            any = e.childAtPath('complexType/sequence/any')
            any.set('maxOccurs', 'unbounded')
            break


def getNodeList():

    d = RegistryDoctor()
    client = Client(WSDL,doctor=d)

    qr="""declare namespace ri='http://www.ivoa.net/xml/RegistryInterface/v1.0';
for $x in //ri:Resource
where $x/capability[@standardID='ivo://vamdc/std/TAP-XSAMS']
and $x/@status='active'
return ($x/title, $x/capability[@standardID='ivo://vamdc/std/TAP-XSAMS']/interface/accessURL)"""

    v=client.service.XQuerySearch(qr)
    nameurls=[]
    while v:
	nameurls.append({\
			'name':v.pop(1),
			'url':v.pop(0)['value'],
			})
    return nameurls



if __name__ == '__main__':
    print getNodeList()
