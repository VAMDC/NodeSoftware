"""
The implementation of the TAP class

"""

from vamdc.server import *
from vamdc.xmltools import *

valdurl="http://vamdc.fysast.uu.se:8080/DSAcat/TAP/async"
valdquery='SELECT * FROM VALD.merged WHERE VALD.merged.ref1=1'

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
        #sleep(2)
        print 'now running...'
        self.run_job()
        #sleep(2)
        print 'now fetching...'
        self.fetch_result()
        #self.readVO()

    def send_query(self):
        response = urllib.urlopen(self.requrl,self.query)
        self.job_xml=e.parse(response)
	#print e.tostring(self.job_xml)
        response.close()
	#for el in self.job_xml.iter():
        #    if 'jobId' in el.tag:
        #        self.jobid=el.text
        self.jobid=text_list(self.job_xml)[1] 

    def run_job(self):
        postdata=urllib.urlencode({'PHASE':'RUN'})
	#print self.requrl+'/'+self.jobid+'/phase'
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
