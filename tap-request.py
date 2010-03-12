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
# don't use a proxy
from os import environ
environ["http_proxy"]=''

import urllib
from lxml import etree as e
from lxml.etree import XPath
text_list=XPath("//text()")
parser=e.XMLParser(remove_blank_text=True)

from time import sleep
#import atpy
from StringIO import StringIO
import threading

# XML schemata
xsl_job2html_url='http://vamdc.tmy.se:8080/DSAcat/TAP/uws-job-to-html.xsl'
xsl_job2html = e.parse(xsl_job2html_url)
job2html= e.XSLT(xsl_job2html)

xsl_data2html_url='http://vamdc.tmy.se:8080/DSAcat/TAP/uws-results-to-html.xsl'
xsl_data2html = e.parse(xsl_data2html_url)
data2html= e.XSLT(xsl_data2html)

xsl_xsams_url='http://vamdc.tmy.se:8080/DSAcat/xsams-0.1.xsd'
xsl_xsams= e.parse(xsl_xsams_url)


valdurl="http://vamdc.tmy.se:8080/DSAcat/TAP/async"
valdquery='SELECT TOP 5 VALD.merged.wavel,VALD.merged.ion FROM VALD.merged'

class TAP(object):
    def __init__(self,requrl=valdurl,query=valdquery):
        self.requrl=requrl
        quer={}
        quer['LANG']='ADQL'
        quer['FORMAT']='application/x-votable+xml'
        quer['VERSION']='1.0'
        quer['QUERY']=query
        self.query=urllib.urlencode(quer)

    def __repr__(self):
        s=''
        if self.result_xml:
            for element in self.result_xml.iter():
                if 'TR' in element.tag: s+='\n'
                if 'TD' in element.tag: s+=element.text+'\t'
        else:
            s+="Not data here yet!"
        return s

    def run(self):
        self.send_query()
        self.run_job()
        self.fetch_result()

    def send_query(self):
        response = urllib.urlopen(self.requrl,self.query)
        self.job_xml=e.parse(response)
        response.close()
        # old way to find out the JobId:
        #for el in xml_res.iter():
        #    if 'jobId' in el.tag:
        #        jobid=el.text
        self.jobid=text_list(self.job_xml)[1] 

    def run_job(self):
        postdata=urllib.urlencode({'PHASE':'RUN'})
        urllib.urlopen(self.requrl+'/'+self.jobid+'/phase',postdata)


    def fetch_result(self):
        # check if result is there
        while urllib.urlopen(self.requrl+'/'+self.jobid+'/phase').read() != 'COMPLETED':
            print 'waiting...'
            sleep(1)

        resulturl=self.requrl+'/'+self.jobid+'/results/result'
        res=urllib.urlopen(resulturl)
        self.result_xml=e.parse(res,parser)
        res.close()

    def readVO(vodata):
        t=atpy.Table()
        t.read(StringIO(self.vodata),type='vo')
        print t.wavel[2]
        print t.columns
    #open('data.vo','w').write(vodata)
    #t=readVO(vodata) # this does not yet work yet since the vald-metadata are incomplete



def main():
    
    for el in vo.iter():
        if 'TR' in el.tag: print
        if 'TD' in el.tag: print el.text,

class MyThread ( threading.Thread ):
    def run ( self ):
        tap=TAP()
        tap.run()
        print tap


if __name__=='__main__': 
    for i in xrange(1):
        MyThread().start()

