#!/usr/bin/python
# -*- coding: UTF-8 -*-

from models import *
from django.core.exceptions import ValidationError

def getSpeciesList(spids = None):
    """
    """
    molecules = Species.objects.filter(origin=0,archiveflag=0).exclude(molecule__numberofatoms__exact='Atomic').order_by('molecule__stoichiometricformula','speciestag')

    if spids:
        molecules = molecules.filter(pk__in=spids)
        
    return molecules


def getSpecie(id = None):
    """
    """
    specie = Species.objects.get(pk=id)
    return specie


def getSources4specie(id):
    """
    """

    # get Source-Ids (rId's)
    slist = SourcesIDRefs.objects.filter(specie=id).distinct()
    sourceids = slist.values_list('source',flat=True)

    # get Sources
    sources = Sources.objects.filter(pk__in=sourceids)
    return sources


def getDatasets4specie(id):
    """
    """

    # get Datasets
    datasets = Datasets.objects.filter(specie=id)
    return datasets


def getParameters4specie(id, paramtype=None):
    """
    Queries the parameters for a specie.
    If paramtype is given only parameters of this type are returned,
    otherwise all parameter for this species will be returned.
    
    id = identifier of the species object in the database
    paramtype = Type of parameter {"Rotational Constant", "Dipole Moment", ...}

    """

    # get Parameters
    parameters = Parameter.objects.filter(specie=id)

    # if a specific parameter.type is given: filter accordingly
    if type:
        parameters = parameters.filter(type=paramtype).order_by('parameter')
        
    return parameters


def getPartitionf4specie(id, format='html'):
    """
    Queries the partition functions for this specie and creates a html-table.
    (This is done because it seems to be simpler than using a template; issue: ordering)

    id: Database - ID of the specie

    returns:
       string with html-table as content
    """
    partitionFunctions = Partitionfunctions.objects.filter(specie=id)
    temps=partitionFunctions.values_list("temperature", flat=True).distinct().order_by("temperature")
    states=partitionFunctions.values_list("state", flat=True).distinct().order_by("state")
    pftableHtml = "<table class='full'><thead><tr><th>&nbsp;</th>"

    for s in states:
        pftableHtml += "<th> %s </th>" % s

    pftableHtml += "</tr></thead><tbody>"
    
    for t in temps:
        pftableHtml+= "<tr><th scope='row' class='sub'> Q(%s /K) </th>" % t
        for s in states:
            try:
                pftableHtml += "<td>%s</td> " % partitionFunctions.get(temperature=t, state=s).partitionfunc
            except:
                pftableHtml += "<td>&nbsp;</td>"
        pftableHtml+= "<tr>"

    pftableHtml +="</tbody></table>"

    return pftableHtml


def getFiles4specie(id):
    """
    """

    # get Files
    files = Files.objects.filter(specie=id)
    return files


    
def checkQuery(postvars):
    """
    Creates TAP-XSAMS query and return it as a string
    In addition some html code for the query page is generated
    INPUT: posted variables
    """
    tapxsams = "SELECT ALL WHERE "
    tapcdms = tapxsams
    
    htmlcode = ""
    # Check if species have been selected
    if 'speciesIDs' in postvars:
        id_list = postvars.getlist('speciesIDs')
    else :
        id_list = None

    if not id_list:
        htmlcode += "<a href='#' onclick=\"load_page('SelectMolecule');\" ><p class='warning' >SPECIES: nothing selected => Click here to select species!</p></a>"
        idlist = []
    else:
        mols = getSpeciesList(id_list)

#        foreach (specie in mols):
        inchikeylist = mols.values_list('inchikey',flat=True)
        idlist = mols.values_list('id',flat=True)

#        tapxsams += " InchiKey in ('%s') " % "' OR '".join( map(str, inchikeylist))
        tapxsams += "(" + " OR ".join([" InchiKey = '" + ikey + "'" for ikey in inchikeylist]) + ")"
        tapcdms += "(" + " OR ".join([" MoleculeSpeciesID = %s " % ikey  for ikey in idlist]) + ")"

    htmlcode += "<ul class='vlist'>"
    htmlcode += "<li><a href='#' onclick=\"$('#a_form_species').click();$('#a_form_species').addClass('activeLink');\">"
    
    htmlcode += " MoleculeSpeciesID in ( %s ) " % ', '.join ( map(str, idlist))
    htmlcode += "</li>"
        
    # CHECK Frequency range
    if 'UnitNu' in postvars:
        unitNu = postvars['UnitNu']
#        htmlcode += "<p class='info'>AND RadTransFrequencyUnit = %s </p>" % unitNu
    else:
        unitNu = "GHz"

    # Units are stored in MHz
    if unitNu == "GHz":
        unitfactor = 1000.0
    else:
        unitfactor = 1.0

    if ('T_SEARCH_FREQ_FROM' in postvars) & ('T_SEARCH_FREQ_TO' in postvars):
        htmlcode += "<li><a href='#' onclick=\"$('#a_form_transitions').click();$('#a_form_transitions').addClass('activeLink');\">AND Frequency between %s %s AND %s %s </a></li>" % (postvars['T_SEARCH_FREQ_FROM'], unitNu, postvars['T_SEARCH_FREQ_TO'], unitNu)
            
    if 'T_SEARCH_FREQ_FROM' in postvars :
        try:
            freqfrom = unitfactor * float(postvars['T_SEARCH_FREQ_FROM'])
        except ValueError:
            Error = "Lower Frequency is not a number "
            freqfrom = 0

        if (freqfrom>0):
            angstromupper =  2.99792458E12 / freqfrom
            tapxsams += " AND RadTransWavelength < %lf " % angstromupper
            tapcdms += " AND RadTransWavelength < %lf " % angstromupper

        #tapxsams += " AND RadTransFrequency > %lf " % freqfrom

    if 'T_SEARCH_FREQ_TO' in postvars :
        try:
            freqto = unitfactor * float(postvars['T_SEARCH_FREQ_TO'])
        except ValueError:
            Error = "Lower Frequency is not a number "
            freqto = 0

        if (freqto>0):
            angstromlower = 2.99792458E12 / freqto            
            tapxsams += " AND RadTransWavelength > %lf " % angstromlower
            tapcdms += " AND RadTransWavelength > %lf " % angstromlower

        #tapxsams += " AND RadTransFrequency < %s " % freqto

    if ('T_SEARCH_FREQ_FROM' not in postvars) & ('T_SEARCH_FREQ_TO' not in postvars):
        htmlcode += "<a href='#' onclick=\"$('#a_form_transitions').click();$('#a_form_transitions').addClass('activeLink');\">"
        htmlcode += "<p style='background-color:#FFFF99' class='important'>FREQUENCY RANGE: not specified => no restrictions</p></a>"
                                                                                                                                                                           
    # CHECK Intensity
    if ('T_SEARCH_INT' in postvars) & (postvars['T_SEARCH_INT']>-10):
        htmlcode += "<li><a href='#' onclick=\"$('#a_form_transitions').click();$('#a_form_transitions').addClass('activeLink');\">AND Intensity (lg-units) > %s </a></li>" % postvars['T_SEARCH_INT']
       # tapxsams += " AND RadTransProbabilityIdealisedIntensity > %s " % postvars['T_SEARCH_INT']
        tapcdms += " AND RadTransProbabilityIdealisedIntensity > %s " % postvars['T_SEARCH_INT']
    else:
        htmlcode += """<a href='#' onclick=\"$('#a_form_transitions').click();$('#a_form_transitions').addClass('activeLink');\"> 
                       <p style='background-color:#FFFF99' class='important'>INTENSITY LIMIT: not specified => no restrictions</p>
                       </a>\n """

    htmlcode += "</ul>"

    if 'database' in postvars:
        if postvars['database'] in ['cdms','jpl']:
            tap=tapcdms
        else:
            tap=tapxsams
    else:
        tap=tapcdms
        
#    return tapxsams, htmlcode
    return tap, htmlcode



def geturl(url, timeout=None):
    """
    Usage: {% geturl url [timeout] %}

    Examples:
    {% geturl "http://example.com/path/to/content/" %}
    {% geturl object.urlfield 1 %} 
    """
    import socket
    from urllib2 import urlopen
    socket_default_timeout = socket.getdefaulttimeout()
    if timeout is not None:
        try:
            socket_timeout = float(timeout)
        except ValueError:
            raise template.TemplateSyntaxError, "timeout argument of geturl tag, if provided, must be convertible to a float"
        try:
            socket.setdefaulttimeout(socket_timeout)
        except ValueError:
            raise template.TemplateSyntaxError, "timeout argument of geturl tag, if provided, cannot be less than zero"
    try:
        try: 
            content = urlopen(url).read()
        finally: # reset socket timeout
            if timeout is not None:
                socket.setdefaulttimeout(socket_default_timeout) 
    except:
        content = ''        
    return content


def applyStylesheet(inurl, xsl = None):
    """
    Applies a xslt-stylesheet to the given url
    """
    from django.conf import settings
    from lxml import etree as e
    if xsl:
        xsl=e.XSLT(e.parse(open(xsl)))
    else:
        xsl=e.XSLT(e.parse(open('/home/endres/Projects/vamdc/nodes/cdms/node/convertXSAMS2html.xslt')))

    from urllib2 import urlopen

    try: data = urlopen(inurl)

    except Exception,err:
        raise ValidationError('Could not open given URL: %s'%err)

    # Save XML-File to temporary directory
    filename = settings.TMPDIR+"/xsams_download.xsams"

    for row in data.info().headers:
      p = row.find("filename=")
      if p>-1:
        filename = settings.TMPDIR+"/"+row[p+9:].rstrip()

    local_file = open(filename, "w")
    local_file.write(data.read())
    local_file.close()

    try: xml=e.parse(filename)
    except Exception,err:
        raise ValidationError('Could not parse XML file: %s'%err)
    

    try: result = str(xsl(xml))
    except Exception,err:
        raise ValidationError('Could not transform XML file: %s'%err)
    
    return  result 

def applyStylesheet2File(infile, xsl = None):
    """
    Applies a xslt-stylesheet to the given file
    """
    from django.conf import settings
    from lxml import etree as e

    xsl = settings.BASE_PATH + '/nodes/cdms/static/xsl/convertXSAMS2html.xslt'
    xsl = settings.BASE_PATH + "/nodes/cdms/static/xsl/convertXSAMS2Rad3d.xslt"

    if xsl:
        xsl=e.XSLT(e.parse(open(xsl)))
    else:
        xsl=e.XSLT(e.parse(open('/home/endres/Projects/vamdc/nodes/cdms/node/convertXSAMS2html.xslt')))
        
    from urllib2 import urlopen

    try: xml=e.parse(infile)
    except Exception,err:
        raise ValidationError('Could not parse XML file: %s'%err)
    

    try: result = str(xsl(xml))
    except Exception,err:
        raise ValidationError('Could not transform XML file: %s'%err)
    
    return  result


def getHtmlNodeList():
    """
    """
    from other.registry import getNodeList
    
    response = ""

    try:
        nodes = getNodeList()
    except Exception,err:
        response+= "<br><br>Error while getting list of nodes!: <br> %s " % err
        nodes = []


    response += "<div class='vlist'><ul>"

    response += """<li id='nodehead' class='' style='border-width:1px;border-style:hidden;background-color:#F0F0F0;padding:0.5em;margin:5px;'>
                           <div class='' style='background-color:blue;'>
                              <div class='nodename float_left' style='font-weight:bold;width:20em;background-color2:grey'>%s</div>                                                         
                              <div class='status float_left' style='width:8em'>Status</div>
                              <div class='numspecies float_left' style='width:8em'> %s</div>
                              <div class='nummols float_left' style='width:8em'> %s</div>
                              <div class='numstates float_left' style='width:8em'> %s</div>
                              <div class='numradtrans float_left' style='width:8em'> %s</div>
                              <div class='numtrunc float_left' style='width:8em'> %s</div>
                           </div>
                      </li>""" % ("Database","# Species","# Molecules","# States","# Trans","% Trunc.")

    for node in nodes:

        response += """<li id='node%s' class='vamdcnode' style='width:%s;border-width:1px;border-style:solid;border-color:black;padding:0.5em;margin:5px;background-color:#fafaff'>
                           <div class='nodeurl' style='display:none' id='%s'>%s </div>
                           <div class='url' style='display:none'></div>
                           <div class='' style=''>
                              <div class='nodename float_left' style='font-weight:bold;width:20em;background-color2:grey'>%s</div>                                                         
                              <div class='status float_left' style='width:8em'></div>
                              <div class='numspecies float_left' style='width:8em'> %s</div>
                              <div class='nummols float_left' style='width:8em'> %s</div>
                              <div class='numstates float_left' style='width:8em'> %s</div>
                              <div class='numradtrans float_left' style='width:8em'> %s</div>
                              <div class='numtrunc float_left' style='width:8em'> %s</div>
                           </div>
                           <div class='species' style='clear:both'></div> 
                      </li>""" % (node["name"],u'98%',node["name"], node["url"],node["name"],"0","0","0","0","0")

    response += "</ul></div>"
    return response


def doHeadRequest(url, timeout = 20):
    """
    Does a HEAD request on the given url.
    A list of 'vamdc' - statistic objects is returned
    """
    from urlparse import urlparse
    from httplib import HTTPConnection
    
    urlobj = urlparse(url)

    try:
        conn = HTTPConnection(urlobj.netloc, timeout = timeout)
        conn.request("HEAD", urlobj.path+"?"+urlobj.query)
        res = conn.getresponse()
    except:
        # error handling has to be included
        vamdccounts = [('error', 'no response')]
        return vamdccounts
        
    if res.status == 200:
        vamdccounts = [item for item in res.getheaders() if item[0][0:5]=='vamdc']
        content = [item for item in res.getheaders() if item[0][0:7]=='content']
    else:
        vamdccounts =  []

    return vamdccounts
    
def getNodeStatistic(baseurl, inchikey, url = None):
    """
    Queries the VAMDC databases via the given baseurl and the inchikey.
    Via a HEAD request statistics is obtained from the result

    Returns: VAMDC statistic as htmlcode (for ajax Requests)
    """

    url=url.replace('rad3d','XSAMS')
    url=url.replace('png','XSAMS')
    url=url.replace('xspcat','XSAMS')
    url=url.replace('comfort','XSAMS')
    url=url.replace('spcat','XSAMS')
    url=url.replace('mrg','XSAMS')
    
    
    if not url:
        query = "sync?REQUEST=doQuery&LANG=VSS1&FORMAT=XSAMS&QUERY=SELECT+All+WHERE++InchiKey='%s'" % inchikey
        url = baseurl.rstrip()+query

    vamdccounts = doHeadRequest(url)
    vc = {}
    vc['url']=url
    
    response = "<ul>"
    if len(vamdccounts)>0:

        for item in vamdccounts:
            response += "<li>%s: %s " % item
            vc[item[0].replace('-','')]=item[1]

        response += "<li><INPUT TYPE=\"button\" NAME=\"T_SHOW\" ONCLICK=\"$('#queryresult').html('Processing ...');docShowSubpage('form_result');ajaxQuery('ajaxQuery','"+url+"')\" VALUE = \"Show Data\" >"
        response += "<INPUT TYPE=\"button\" NAME=\"T_SHOW\" ONCLICK=\""+url+"\" VALUE = \"Download Data\" ></li>"
    else:
        response += "<li>Nothing found"

    response += "</ul>"
    
    return response, vc


def getspecies(url):

    from lxml import etree
    from urllib2 import urlopen

    url=url.replace('rad3d','XSAMS')
    url=url.replace('png','XSAMS')
    url=url.replace('xspcat','XSAMS')
    url=url.replace('spcat','XSAMS')

    try:
        content = urlopen(url)
    except:
        return "url - error: " + url

    try:
        xml = etree.XML(content.read())
        prefixmap = {'xsams' : xml.nsmap[None]}
    except:
        return "ERROR"
    
    xp = "//xsams:Molecule"
    response = ""

    html = "<table class='full'><tbody>"
    try:
        for m in xml.xpath(xp ,namespaces=prefixmap):
            try:
                stoichiometricformula = m.xpath('./xsams:MolecularChemicalSpecies/xsams:StoichiometricFormula', namespaces=prefixmap)[0].text
                chemicalname = m.xpath('./xsams:MolecularChemicalSpecies/xsams:ChemicalName/xsams:Value', namespaces=prefixmap)[0].text
                structuralformula = m.xpath('./xsams:MolecularChemicalSpecies/xsams:OrdinaryStructuralFormula/xsams:Value', namespaces=prefixmap)[0].text
                inchikey = m.xpath('./xsams:MolecularChemicalSpecies/xsams:InChIKey', namespaces=prefixmap)[0].text
                comment = m.xpath('./xsams:MolecularChemicalSpecies/xsams:Comment', namespaces=prefixmap)[0].text
            
                response += "%s %s %s %s \n" % (structuralformula, stoichiometricformula, chemicalname, comment)
                html += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> \n" % (structuralformula, stoichiometricformula, chemicalname, comment)
            except:
                pass
    except:
        return "ERROR 2"

    html += "</tbody></table>"
    return  html
