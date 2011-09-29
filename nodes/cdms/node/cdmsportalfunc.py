from models import *


def getSpeciesList(spids = None):
    """
    """
    molecules = Species.objects.filter(origin=5,archiveflag=0).exclude(molecule__numberofatoms__exact='Atomic')

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
    slist = SourcesIDRefs.objects.filter(eId=id).distinct()
    sourceids = slist.values_list('rId',flat=True)

    # get Sources
    sources = Sources.objects.filter(pk__in=sourceids)
    return sources


def getDatasets4specie(id):
    """
    """

    # get Datasets
    datasets = Datasets.objects.filter(species=id)
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

#        tapxsams += " MoleculeInchiKey in ('%s') " % "' OR '".join( map(str, inchikeylist))
        tapxsams += "(" + " OR ".join([" MoleculeInchiKey = '" + ikey + "'" for ikey in inchikeylist]) + ")"

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
            
        tapxsams += " AND RadTransFrequency > %lf " % freqfrom

    if 'T_SEARCH_FREQ_TO' in postvars :
        try:
            freqto = unitfactor * float(postvars['T_SEARCH_FREQ_TO'])
        except ValueError:
            Error = "Lower Frequency is not a number "
            freqto = 0

        tapxsams += " AND RadTransFrequency < %s " % freqto

    if ('T_SEARCH_FREQ_FROM' not in postvars) & ('T_SEARCH_FREQ_TO' not in postvars):
        htmlcode += "<a href='#' onclick=\"$('#a_form_transitions').click();$('#a_form_transitions').addClass('activeLink');\">"
        htmlcode += "<p style='background-color:#FFFF99' class='important'>FREQUENCY RANGE: not specified => no restrictions</p></a>"
                                                                                                                                                                           
    # CHECK Intensity
    if 'T_SEARCH_INT' in postvars:
        htmlcode += "<li><a href='#' onclick=\"$('#a_form_transitions').click();$('#a_form_transitions').addClass('activeLink');\">AND Intensity (lg-units) > %s </a></li>" % postvars['T_SEARCH_INT']
        tapxsams += " AND RadTransProbabilityIdealisedIntensity > %s " % postvars['T_SEARCH_INT']
    else:
        htmlcode += """<a href='#' onclick=\"$('#a_form_transitions').click();$('#a_form_transitions').addClass('activeLink');\"> 
                       <p style='background-color:#FFFF99' class='important'>INTENSITY LIMIT: not specified => no restrictions</p>
                       </a>\n """

    htmlcode += "</ul>"


    
    return tapxsams, htmlcode



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
    # from django.shortcuts import render_to_response
    # from django.template import RequestContext
    # from django.http import HttpResponseRedirect, HttpResponse
    # from django.forms import Form,FileField,URLField,TextInput
    # from django.core.exceptions import ValidationError
    
    from lxml import etree as e
    if xsl:
        xsl=e.XSLT(e.parse(open(xsl)))
    else:
        xsl=e.XSLT(e.parse(open('/home/endres/Projects/vamdc/nodes/cdms/node/convertXSAMS2html.xslt')))

    from urllib2 import urlopen

    try: data = urlopen(inurl)

    except Exception,err:
        raise ValidationError('Could not open given URL: %s'%err)
    
    try: xml=e.parse(data)
    except Exception,err:
        raise ValidationError('Could not parse XML file: %s'%err)

    try: result = xsl(xml)
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


    for node in nodes:
        response += """<fieldset> <div class='vamdcnode'>
                     <h4> %s </h4>
                     <div class='nodeurl' id='%s'>%s </div>
                     </div></fieldset>""" % (node["name"], node["name"], node["url"])


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
        # conn.request("HEAD", "/DjCDMS/tap/sync?REQUEST=doQuery&LANG=VSS1&FORMAT=XSAMS&QUERY=SELECT+All+WHERE++MoleculeInchiKey='QGZKDVFQNNGYKY-HNQPUXNCSA-N'")
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
    
def getNodeStatistic(baseurl, inchikey):
    """
    Queries the VAMDC databases via the given baseurl and the inchikey.
    Via a HEAD request statistics is obtained from the result

    Returns: VAMDC statistic as htmlcode (for ajax Requests)
    """
    query = "sync?REQUEST=doQuery&LANG=VSS1&FORMAT=XSAMS&QUERY=SELECT+All+WHERE++MoleculeInchiKey='%s'" % inchikey
    vamdccounts = doHeadRequest(baseurl.rstrip()+query)

    response = "<ul>"
    if len(vamdccounts)>0:
        for item in vamdccounts:
            response += "<li>%s: %s " % item
    else:
        response += "<li>Nothing found"

    response += "</ul>"
    
    # response += "<br><br>"+ baseurl + query
    return response
    # return "Fetching Data for url %s and inchikey %s " % (baseurl, inchikey)
