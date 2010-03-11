#!/usr/bin/env python
"""

tap-request.py

Attempt to query the TAP-interface of DSA/catalog.
It's a asynchronous request and the replies are XML
documents that can be tranformed into html

Below script does not work yet.

"""
import urllib
from os import environ
environ["http_proxy"]=''
import sgmllib
from lxml import etree as e
from lxml.etree import XPath
text_list=XPath("//text()")

from time import sleep
import atpy
from StringIO import StringIO

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
# The base of the tap interface
url="http://vamdc.tmy.se:8080/DSAcat/TAP/"
suffix='async'

def runquery(quer):
    quer=urllib.urlencode(quer)
    response = urllib.urlopen(url+suffix,quer) # making the actual request
    xml_res=e.parse(response)
    response.close()
    # old way to find out the JobId:
    #for el in xml_res.iter():
    #    if 'jobId' in el.tag:
    #        jobid=el.text
    jobid=text_list(xml_res)[1] 
    postdata=urllib.urlencode({'PHASE':'RUN'})
    urllib.urlopen(url+suffix+'/'+jobid+'/phase',postdata)

    return jobid

def fetchresult(jobid):
    # check if result is there
    while urllib.urlopen(url+suffix+'/'+jobid+'/phase').read() != 'COMPLETED':
        print 'waiting...'
        sleep(1)

    resulturl=url+suffix+'/'+jobid+'/results/result'
    data=urllib.urlopen(resulturl).read()
    return data

def readVO(vodata):
    t=atpy.Table()
    t.read(StringIO(vodata),type='vo')

    print t.wavel[2]
    print t.columns


# construct the query
quer={}
quer['LANG']='ADQL'
quer['FORMAT']='application/x-votable+xml'
quer['VERSION']='1.0'
quer['QUERY']='SELECT TOP 5 VALD.merged.wavel FROM VALD.merged'

jobid=runquery(quer)
vodata=fetchresult(jobid)
#open('data.vo','w').write(vodata)
#t=readVO(vodata) # this does not yet work yet since the vald-metadata are incomplete
