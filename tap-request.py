#!/usr/bin/env python
"""

tap-request.py

Attempt to query the TAP-interface of DSA/catalog.
It's a asynchronous request and the replies are XML
documents (that can be tranformed into html).

The scripts sends a (hardcoded) request to my
DSA/catalog installation with VALD data. It then
tells DSA to run the query, checks if it has completed
and fetches the result.

Not yet working: read the result into ATPy's implementation
of VOTable.

"""
import urllib
from os import environ
environ["http_proxy"]=''
import sgmllib
from lxml import etree as e
from lxml.etree import XPath
text_list=XPath("//text()")
parser=e.XMLParser(remove_blank_text=True)

from time import sleep
#import atpy
from StringIO import StringIO
import threading

# XML schema
xsl_job2html_url='http://vamdc.tmy.se:8080/DSAcat/TAP/uws-job-to-html.xsl'
xsl_job2html = e.parse(xsl_job2html_url)
job2html= e.XSLT(xsl_job2html)

xsl_data2html_url='http://vamdc.tmy.se:8080/DSAcat/TAP/uws-results-to-html.xsl'
xsl_data2html = e.parse(xsl_data2html_url)
data2html= e.XSLT(xsl_data2html)

xsl_xsams_url='http://vamdc.tmy.se:8080/DSAcat/xsams-0.1.xsd'
xsl_xsams= e.parse(xsl_xsams_url)


# where exactly to query
url="http://vamdc.tmy.se:8080/DSAcat/TAP/async"

# the query
quer={}
quer['LANG']='ADQL'
quer['FORMAT']='application/x-votable+xml'
quer['VERSION']='1.0'
quer['QUERY']='SELECT TOP 5 VALD.merged.wavel,VALD.merged.ion FROM VALD.merged'

#
#  Helper functions
#
def runquery(quer):
    quer=urllib.urlencode(quer)
    response = urllib.urlopen(url,quer) # making the actual request
    xml_res=e.parse(response)
    response.close()
    # old way to find out the JobId:
    #for el in xml_res.iter():
    #    if 'jobId' in el.tag:
    #        jobid=el.text
    jobid=text_list(xml_res)[1] 
    postdata=urllib.urlencode({'PHASE':'RUN'})
    urllib.urlopen(url+'/'+jobid+'/phase',postdata)

    return jobid

def fetchresult(jobid):
    # check if result is there
    while urllib.urlopen(url+'/'+jobid+'/phase').read() != 'COMPLETED':
        print 'waiting...'
        sleep(1)

    resulturl=url+'/'+jobid+'/results/result'
    data=urllib.urlopen(resulturl).read()
    return data

def readVO(vodata):
    t=atpy.Table()
    t.read(StringIO(vodata),type='vo')

    print t.wavel[2]
    print t.columns



def main():
    jobid=runquery(quer)
    vodata=fetchresult(jobid)
    vo=e.parse(StringIO(vodata),parser)
    for el in vo.iter():
        if 'TR' in el.tag: print
        if 'TD' in el.tag: print el.text,
    #open('data.vo','w').write(vodata)
    #t=readVO(vodata) # this does not yet work yet since the vald-metadata are incomplete

class MyThread ( threading.Thread ):
    def run ( self ): main()


if __name__=='__main__': main()
#    for i in xrange(20):
#        MyThread().start()

