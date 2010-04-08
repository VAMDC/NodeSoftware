from vamdc.xmltools import *
import vamdc.db as db
t=db.tools
subel=e.SubElement

NS='http://www.w3.org/2001/XMLSchema-instance'
SCHEMA='http://www-amdis.iaea.org/xsams/schema/xsams-0.1.xsd'

header="""<?xml version="1.0" encoding="UTF-8"?>
<XSAMSData xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
			xsi:noNamespaceSchemaLocation="http://www-amdis.iaea.org/xsams/schema/xsams-0.1.xsd"/>"""

def xsams_root():
    location_attribute = '{%s}noNameSpaceSchemaLocation' % NS
    return e.Element('XSAMSData',attrib={location_attribute:SCHEMA})
    

def write_state(atoms,data=None):
    atom=subel(atoms,'Atom')
    nuchar=subel(atom,'NuclearCharge')
    nuchar.text='1'
    isotope=subel(atom,'Isotope')
    ionstate=subel(isotope,'IonState')
    ioncharge=subel(ionstate,'IonCharge')
    ioncharge.text='0'
    atomstate=subel(ionstate,'AtomicState')
    atomstate.set('stateID','bla')
    descr=subel(atomstate,'Description')
    descr.text='put term designation here'

    numdata=subel(atomstate,'AtomicNumericalData')
    energy=subel(numdata,'StateEnergy')
    val=subel(energy,'Value')
    val.text='5.6'
    val.set('units','1/cm')
    lande=subel(numdata,'LandeFactor')

    qnum=subel(atomstate,'AtomicQuantumNumbers')
    parit=subel(qnum,'Parity')
    parit.text='even'
    J=subel(qnum,'TotalAngularMomentum')
    J.text='2.5'

    atcomp=subel(atomstate,'AtomicComposition')
    comp=subel(atcomp,'Component')
    term=subel(comp,'Term')
    ls=subel(term,'LS')
    l=subel(ls,'L')
    val=subel(l,'Value')
    val.text='2.5'
    s=subel(ls,'S')
    val=subel(s,'Value')
    val.text='2.5'
    

def write_source(sources,data):
    pass

def write_transition(processes,data):
    pass



def getdata(curs,query):
    curs.execute(query)
    return curs.fetchall()

def tostring(xml):
    return e.tostring(xml,xml_declaration=True,encoding='UTF-8',pretty_print=True) 

def run(curs,outname=None,query=None):
    if not query: query='select * from transitions where vacwave between 86 and 86.2'

    root=xsams_root()
    sources=subel(root,'Sources')
    methods=subel(root,'Methods')
    states=subel(root,'States')
    atoms=subel(states,'Atoms')
    processes=subel(root,'Processes')

    data=getdata(curs,query)
    for d in data:
        vacwave,airwave,species,loggf,landeff,gammarad,gammastark,gammawaals,srctag,acflag,accur,comment,wave_ref,loggf_ref,lande_ref,gammarad_ref,gamastark_ref,gammawaals_ref,upcoupling,upterm,locoupling,loterm=d


        UpStateID='%s-%s-%s'%(species,upcoupling,upterm)
        UpStateID=UpStateID.replace(' ','-')
        LoStateID='%s-%s-%s'%(species,locoupling,loterm)
        LoStateID=LoStateID.replace(' ','-')
        
        loqs=getdata(curs,'SELECT * from qnums WHERE idstring="%s"'%LoStateID)
        hiqs=getdata(curs,'SELECT * from qnums WHERE idstring="%s"'%UpStateID)

        lostate=getdata(curs,'SELECT * from lostates WHERE species="%s" AND term="%s" AND coupling="%s"'%())
        print lostate

        if loqs: write_state(curs,state,loqs)
        write_state(states,data)
        write_transition(processes,data)
        write_source(sources,data)

    
    #print tostring(root)
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


    return root
