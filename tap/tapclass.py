"""
The implementation of the TAP class

"""

from __init__ import *

text_list=XPath("//text()")
parser=e.XMLParser(remove_blank_text=True)

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
valdquery='SELECT TOP 5 VALD.merged.wavel FROM VALD.merged'

class TAP(object):
    def __init__(self,requrl=valdurl,query=valdquery,parser=parser):
        self.requrl=requrl
        self.parser=parser
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
        self.readVO()

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
        self.result_xml=e.parse(res,self.parser)
        res.close()

    def readVO(self):
        t=atpy.Table()
        tfile,tname=mktmp()
        tfile.write(e.tostring(self.result_xml))
        tfile.close()
        t.read(tname,type='vo')
        unlink(tname)
        self.VoTab=t
        
        #print self.VoTab.columns
        #for col in self.VoTab.columns:
        #    print self.VoTab.data[col]
