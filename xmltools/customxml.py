from vamdc.xmltools import *
import vamdc.db as db
t=db.tools

metatab='meta'
cname='cname'
tname='tname'
ccom='ccom'
cunit='cunit'
cfmt='cfmt'

cols='%s,%s,%s,%s,%s'%(cname,tname,ccom,cunit,cfmt)
colsl=cols.split(',')
colst=tuple(colsl)

def getvalddata(curs,cols,where=None,order=None):
    sql='SELECT %s FROM valddata'%cols
    if where: sql+=' WHERE (%s)'%where
    if order: sql+=' ORDER BY %s'%order
    #print sql
    curs.execute(sql)
    return curs.fetchall()

def getvaldrefs(curs,cols):
    sql='SELECT * FROM refs'
    

def run(curs,outname=None):
    meta=t.cols2lists(curs,metatab,colsl)
    exec('%s=meta'%cols)

    xvald=e.Element('vald')
    xdata=e.SubElement(xvald,'data')

    datacols=cname[:13]
    data=getvalddata(curs,s.join(datacols,','))
    
    for d in data:
        xtrans=e.SubElement(xdata,'transition')
        for i,col in enumerate(datacols):
            xcol=e.SubElement(xtrans,'%s'%col)
            fmt='%'+cfmt[i]
            xcol.text=fmt%d[i]
            xcol.set('ref','1')

    xrefs=e.SubElement(xvald,'refs')


    xmeta=e.SubElement(xvald,'meta')
    for i,name in enumerate(cname):
        xcol=e.SubElement(xmeta,'column')
        xcol.set('name',name)
        xcol.set('unit',cunit[i] or '')
        xcol.set('table',tname[i] or '')
        xcol.set('comment',ccom[i] or '')
        xcol.set('format',cfmt[i] or '')      

    #print e.tostring(xvald,pretty_print=True)
    #print xvald.xpath('//text()')
    #for trans in xvald.iter('wavel'):
    #    print 'wavel: %s'%str(trans.text)
    
    if outname:
        f=open(outname,'w')
        f.write("""<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="http://tmy.se/t/vald2xsams.xsl"?>
""")
        f.write(e.tostring(xvald,pretty_print=True))
        f.close()
