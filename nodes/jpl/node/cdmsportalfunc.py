#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
from models import *
from django.core.exceptions import ValidationError

def get_species_list(spids = None, database = 0):
    """
    """
    # cdms only
    if database < 0:
        molecules = Species.objects.filter(archiveflag=0).order_by('speciestag')
    else:
        molecules = Species.objects.filter(origin=database,archiveflag=0).order_by('speciestag')
    #molecules = Species.objects.filter(origin=0,archiveflag=0).exclude(molecule__numberofatoms__exact='Atomic').order_by('molecule__stoichiometricformula','speciestag')
    #molecules = Species.objects.filter(archiveflag=0).exclude(molecule__numberofatoms__exact='Atomic').order_by('molecule__stoichiometricformula','speciestag')

    if spids is not None:
        molecules = molecules.filter(pk__in=spids)
        
    return molecules

def get_molecules_list(stoichios = None):
    """
    returns list of molecules
    """
    molecules = Molecules.objects.filter().order_by('stoichiometricformula')
    if stoichios is not None:
        molecules = molecules.filter(stoichiometricformula__in=stoichios)
    return molecules
    
def get_isotopologs_list(inchikeys = None):
    """
    Returns list of isotopologues 
    """
    species = Species.objects.filter(archiveflag=0)

    if inchikeys is not None:
        species = species.filter(inchikey__in=inchikeys)
        
    isotopologs = species.values('inchikey','isotopolog','molecule__stoichiometricformula','molecule__trivialname').distinct().order_by('molecule__stoichiometricformula')
    
    return isotopologs
    
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


def getPartitionf4specie(id, nsi=None, format='html'):
    """
    Queries the partition functions for this specie and creates a html-table.
    (This is done because it seems to be simpler than using a template; issue: ordering)

    id: Database - ID of the specie

    returns:
       string with html-table as content
    """

    if nsi is None:
        nsiid=None
        tablename = ''
    else:
        nsiid = nsi.id
        tablename = "Partitionfunctions for %s states only" % nsi.name
    partitionFunctions = Partitionfunctions.objects.filter(specie=id)
    temps=partitionFunctions.values_list("temperature", flat=True).distinct().order_by("temperature")
    states=partitionFunctions.values_list("state", flat=True).distinct().order_by("state")
    pftableHtml = "<table class='full'>"
    pftableHtml += "<caption><div class='float_left'>%s</div></caption>" % tablename
    pftableHtml += "<thead><tr><th>&nbsp;</th>"

    for s in states:
        pftableHtml += "<th> %s </th>" % s

    pftableHtml += "</tr></thead><tbody>"
    
    for t in temps:
        pftableHtml+= "<tr><th scope='row' class='sub'> Q(%s /K) </th>" % t
        for s in states:
            try:
                pftableHtml += "<td>%s</td> " % partitionFunctions.get(temperature=t, nsi=nsiid, state=s).partitionfunc
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


    
def check_query(postvars):
    """
    Creates TAP-XSAMS query and return it as a string
    In addition some html code for the query page is generated
    INPUT: posted variables
    """
    tapxsams = "SELECT ALL WHERE "
    tapcdms = tapxsams
    
    htmlcode = ""
    # Check if species have been selected
    id_list = postvars.getlist('speciesIDs')
    inchikeys = postvars.getlist('inchikey')
    molecules = postvars.getlist('molecule') # are identified via stoichiometric formula

    ###################################
    # CREATE QUERY STRING FOR SPECIES
    ###################################
    spec_array=[]
    htmlcode += "<ul class='vlist'>"
    htmlcode += "<li>"

    if len(id_list)+len(inchikeys)+len(molecules)>0:
        #mols = get_species_list(id_list)

        #inchikeylist = mols.values_list('inchikey',flat=True)
        #idlist = mols.values_list('id',flat=True)

        #tapxsams += "(" + " OR ".join([" InchiKey = '" + ikey + "'" for ikey in inchikeylist]) + ")"

        if len(id_list)>0:
            spec_array.append( " OR ".join([" SpeciesID = %s " % ikey  for ikey in id_list]) )
            
        if len(inchikeys)>0:
            spec_array.append( " OR ".join([" InchiKey = '%s' " % ikey  for ikey in inchikeys]) )

        if len(molecules)>0:
            spec_array.append( " OR ".join([" MoleculeStoichiometricFormula = '%s' " % ikey  for ikey in molecules]) )

        
        tapxsams += "(" + " OR ".join(spec_array) + ")"
        tapcdms += "(" + " OR ".join(spec_array) + ")"

        htmlcode += "<a href='#' onclick=\"$('#a_form_species').click();$('#a_form_species').addClass('activeLink');\">"
        htmlcode += "(" + " OR ".join(spec_array) + ")"
    else:
        htmlcode += "<a href='#' onclick=\"load_page('queryForm');\" ><font style='color:red'>SPECIES: nothing selected => Click here to select species!</font></a>"
        

    htmlcode += "</li>"


    #######################################
    # CREATE QUERY STRING FOR TRANSITIONS
    #######################################
    transition_filter = False

    ## FREQUECY RANGE ##
    if 'UnitNu' in postvars:
        unitNu = postvars['UnitNu']
    else:
        unitNu = "GHz"

    # Units are stored in MHz
    if unitNu == "GHz":
        unitfactor = 1000.0
    else:
        unitfactor = 1.0

    # Get Frequency Limits
    try:
        freqfrom = unitfactor * float(postvars['T_SEARCH_FREQ_FROM'])
        if (freqfrom>0):
            angstromupper =  2.99792458E12 / freqfrom
            tapxsams += " AND RadTransWavelength < %lf " % angstromupper
            tapcdms += " AND RadTransWavelength < %lf " % angstromupper
            transition_filter = True
    except KeyError:
        freqfrom = None
    except ValueError:
        Error = "Lower Frequency is not a number "
        freqfrom = None
    except:
        pass
    
    try:
        freqto = unitfactor * float(postvars['T_SEARCH_FREQ_TO'])
        if (freqto>0):
            angstromlower = 2.99792458E12 / freqto            
            tapxsams += " AND RadTransWavelength > %lf " % angstromlower
            tapcdms += " AND RadTransWavelength > %lf " % angstromlower
        else:
            # do not return anything (freqto <= 0 should always be false)
            tapxsams += " AND RadTransWavelength < 0 " 
            tapcdms += " AND RadTransWavelength < 0 " 
            
        transition_filter = True
    except KeyError:
        freqto = None
    except ValueError:
        Error = "Lower Frequency is not a number "
        freqto = None
    except:
        pass

    if ((freqfrom is not None) &( freqto is not None)):
        htmlcode += "<li><a href='#' onclick=\"$('#a_form_transitions').click();$('#a_form_transitions').addClass('activeLink');\">AND Frequency between %s %s AND %s %s </a></li>" % (postvars['T_SEARCH_FREQ_FROM'], unitNu, postvars['T_SEARCH_FREQ_TO'], unitNu)
    elif (freqfrom is not None):
        htmlcode += "<li><a href='#' onclick=\"$('#a_form_transitions').click();$('#a_form_transitions').addClass('activeLink');\">AND Frequency > %s %s </a></li>" % (postvars['T_SEARCH_FREQ_FROM'], unitNu)
    elif (freqto is not None):
        htmlcode += "<li><a href='#' onclick=\"$('#a_form_transitions').click();$('#a_form_transitions').addClass('activeLink');\">AND Frequency < %s %s </a></li>" % (postvars['T_SEARCH_FREQ_TO'], unitNu)
        
                                                                                                                                                                           
    ## INTENSITY LIMITS 
    try:
        lgint = float(postvars['T_SEARCH_INT'])
        transition_filter = True
    except KeyError:
        lgint = None
    except ValueError:
        lgint = None

    try:
        if postvars['IntUnit']=='A':
            htmlfield = 'Einstein A value'
            xsamsfield = 'RadTransProbabilityA'
        else:
            htmlfield = 'Intensity (lg-units)'            
            xsamsfield = 'RadTransProbabilityIdealisedIntensity'
    except:
        htmlfield = 'Intensity (lg-units)'            
        xsamsfield = 'RadTransProbabilityIdealisedIntensity'
        
    if (lgint is not None): #'T_SEARCH_INT' in postvars) & (postvars['T_SEARCH_INT']>-10):
        htmlcode += "<li><a href='#' onclick=\"$('#a_form_transitions').click();$('#a_form_transitions').addClass('activeLink');\">AND %s > %s </a></li>" % (htmlfield, postvars['T_SEARCH_INT'])
       # tapxsams += " AND RadTransProbabilityIdealisedIntensity > %s " % postvars['T_SEARCH_INT']
        tapcdms += " AND %s > %s " % (xsamsfield, postvars['T_SEARCH_INT'])
        tapxsams += " AND %s > %s " % (xsamsfield, postvars['T_SEARCH_INT'])
#    else:
#        htmlcode += """<li><a href='#' onclick=\"$('#a_form_transitions').click();$('#a_form_transitions').addClass('activeLink');\"> 
#                       <p style='background-color:#FFFF99' class='important'>INTENSITY LIMIT: not specified => no restrictions</p>
#                       </a></li>\n """


    ## PROCESS CLASS (HFS-FILTERS)
    try:
        hfs = postvars['T_SEARCH_HFSCODE']
        if hfs:
            transition_filter=True
            tapcdms += " AND RadTransCode = '%s' " % (hfs)
            tapxsams += " AND RadTransCode = '%s' " % (hfs)
        else:
            hfs = None
    except KeyError:
        hfs = None

    if (hfs is not None): 
        htmlcode += "<li><a href='#' onclick=\"$('#a_form_transitions').click();$('#a_form_transitions').addClass('activeLink');\">AND Process code  in ( '%s' ) </a></li>" % (hfs)
       # tapxsams += " AND RadTransProbabilityIdealisedIntensity > %s " % postvars['T_SEARCH_INT']

    

    if not transition_filter: #if ((freqfrom is None) & (freqto is None)):
        htmlcode += "<li><a href='#' onclick=\"$('#a_form_transitions').click();$('#a_form_transitions').addClass('activeLink');\">"
#        htmlcode += "<p style='background-color:#FFFF99' class='important'>No restrictions on transitions</p></a></li>"
        htmlcode += "<i>All transitions</i></a></li>"
    #######################################
    # CREATE QUERY STRING FOR STATES
    #######################################
    state_filter = False
    ## STATE ENERGY FILTER
    try:
        energyfrom = float(postvars['T_SEARCH_ENERGY_FROM'])
        tapxsams += " AND StateEnergy > %lf " % energyfrom
        tapcdms += " AND StateEnergy > %lf " % energyfrom
        state_filter = True
    except KeyError:
        energyfrom = None
    except ValueError:
        energyfrom = None
        
    try:
        energyto = float(postvars['T_SEARCH_ENERGY_TO'])
        tapxsams += " AND StateEnergy < %lf " % energyto
        tapcdms += " AND StateEnergy < %lf " % energyto
        state_filter = True
    except KeyError:
        energyto = None
    except ValueError:
        energyto = None

    ## NUCLEAR SPIN ISOMER FILTER
    try:
        nsi = postvars['T_SEARCH_NSI']
        if nsi:
            tapxsams += " AND MoleculeStateNSIName = '%s' " % nsi
            tapcdms += " AND MoleculeStateNSIName = '%s' " % nsi
            state_filter = True
        else:
            nsi = None
    except KeyError:
        nsi = None
        

    if not state_filter:
        htmlcode += "<li><a href='#' onclick=\"$('#a_form_states').click();$('#a_form_states').addClass('activeLink');\">"
        htmlcode += "<i>All states</i></a></li>"
    else:
        if ((energyfrom is not None) &( energyto is not None)):
            htmlcode += "<li><a href='#' onclick=\"$('#a_form_states').click();$('#a_form_states').addClass('activeLink');\">AND Energy between %s %s AND %s %s </a></li>" % (postvars['T_SEARCH_ENERGY_FROM'], 'cm<sup>-1</sup>', postvars['T_SEARCH_ENERGY_TO'], 'cm<sup>-1</sup>')
        elif (energyfrom is not None):
            htmlcode += "<li><a href='#' onclick=\"$('#a_form_states').click();$('#a_form_states').addClass('activeLink');\">AND Energy > %s %s </a></li>" % (postvars['T_SEARCH_ENERGY_FROM'], 'cm<sup>-1</sup>')
        elif (energyto is not None):
            htmlcode += "<li><a href='#' onclick=\"$('#a_form_states').click();$('#a_form_states').addClass('activeLink');\">AND Energy < %s %s </a></li>" % (postvars['T_SEARCH_ENERGY_TO'], 'cm<sup>-1</sup>')
        

        if nsi is not None:
            htmlcode += "<li><a href='#' onclick=\"$('#a_form_states').click();$('#a_form_states').addClass('activeLink');\">AND Nuclear Spin Isomer = '%s' </a></li>" % (nsi)

    #######################################
    # RETURN QUERY STRING DEPENDEND ON DB
    #######################################
    if 'database' in postvars:
        if postvars['database'] in ['cdms','jpl']:
            tap=tapcdms
        else:
            tap=tapxsams
    else:
        tap=tapcdms

    if tap.find('WHERE  AND')>-1:
        tap = tap.replace('WHERE  AND ','WHERE ')
    htmlcode += "</ul>"
        
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


def applyRadex(inurl, xsl = settings.XSLT_DIR + 'speciesmergerRadex_1.0_v1.0.xslt', species1=None, species2=None, inurl2=None):
    """
    Applies a xslt-stylesheet to the given url
    """
    from django.conf import settings
    from lxml import etree as e
    if xsl:
        xsl=e.XSLT(e.parse(open(xsl)))
    else:
        xsl=e.XSLT(e.parse(open(settings.XSLT_DIR + 'speciesmergerRadex_1.0_v1.0.xslt')))

    from urllib2 import urlopen


    # download and save first query-result
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

    if inurl2:
        try: datacol = urlopen(inurl2)

        except Exception,err:
            raise ValidationError('Could not open given URL: %s'%err)

        # Save XML-File to temporary directory
        filename2 = settings.TMPDIR+"/xsams_col_download.xsams"

        for row in datacol.info().headers:
            p = row.find("filename=")
            if p>-1:
                filename2 = settings.TMPDIR+"/"+row[p+9:].rstrip()
        
        local_file = open(filename2, "w")
        local_file.write(datacol.read())
        local_file.close()
   

        try: result = str(xsl(xml, species1="'%s'" % species1, species2="'%s'" % species2, colfile="'%s'" % filename2)) #"/var/cdms/v1_0/NodeSoftware/nodes/cdms/test/basecol_co.xml"))
        except Exception,err:
            raise ValidationError('Could not transform XML file: %s'%err)
    else:
        try: result = str(xsl(xml, species1="'%s'" % species1))
        except Exception,err:
            raise ValidationError('Could not transform XML file: %s'%err)

    return result

def applyStylesheet(inurl, xsl = None):
    """
    Applies a xslt-stylesheet to the given url
    """
    from django.conf import settings
    from lxml import etree as e
    if xsl:
        xsl=e.XSLT(e.parse(open(xsl)))
    else:
        xsl=e.XSLT(e.parse(open(settings.XSLT_DIR + 'convertXSAMS2html.xslt')))

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

    #xsl = settings.XSLT_DIR + 'convertXSAMS2html.xslt'
    #xsl = settings.XSLT_DIR + 'convertXSAMS2Rad3d.xslt"

    if xsl:
        xsl=e.XSLT(e.parse(open(xsl)))
    else:
        xsl=e.XSLT(e.parse(open(settings.XSLT_DIR + 'convertXSAMS2html.xslt')))
        
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

    response += """<li id='nodehead' class='' style='height:7em;border-width:1px;border-style:hidden;background-color:#F0F0F0;padding:0.5em;margin:5px;'>
                              <div class='nodename float_left' style='font-weight:bold;width:15em;background-color2:grey'>%s
                              </div>                                                         
                              <div class='status float_left' style='width:4em'>
                                <svg xmlns='http://www.w3.org/2000/svg'>
                                  <text id='headdb' transform='rotate(270, 12, 0) translate(-60,0)'>%s</text>
                                </svg>
                              </div>
                              <div class='numspecies float_left' style='width:4em'>
                                <svg xmlns='http://www.w3.org/2000/svg'>
                                  <text id='headdb' transform='rotate(270, 12, 0) translate(-60,0)'>%s</text>
                                </svg>
                              </div>
                              <div class='nummols float_left' style='width:4em'>
                                <svg xmlns='http://www.w3.org/2000/svg'>
                                  <text id='headdb' transform='rotate(270, 12, 0) translate(-60,0)'>%s</text>
                                </svg>
                              </div>
                              <div class='numstates float_left' style='width:4em'>
                                <svg xmlns='http://www.w3.org/2000/svg'>
                                  <text id='headdb' transform='rotate(270, 12, 0) translate(-60,0)'>%s</text>
                                </svg>
                              </div>
                              <div class='numradtrans float_left' style='width:4em'>
                                <svg xmlns='http://www.w3.org/2000/svg'>
                                  <text id='headdb' transform='rotate(270, 12, 0) translate(-60,0)'>%s</text>
                                </svg>
                              </div>
                              <div class='numcollisions float_left' style='width:4em'>
                                <svg xmlns='http://www.w3.org/2000/svg'>
                                  <text id='headdb' transform='rotate(270, 12, 0) translate(-60,0)'>%s</text>
                                </svg>
                              </div>
                              <div class='numtrunc float_left' style='width:4em'>
                                <svg xmlns='http://www.w3.org/2000/svg'>
                                  <text id='headdb' transform='rotate(270, 12, 0) translate(-60,0)'>%s</text>
                                </svg>
                              </div>
                      </li>""" % ("Database","Status", "# Species","# Molecules","# States","# Trans","# Collis.","% Trunc.")

    for node in nodes:

        response += """<li id='node%s' class='vamdcnode' style='width:%s;border-width:1px;border-style:solid;border-color:black;padding:0.5em;margin:5px;background-color:#fafaff'>
                           <div class='nodeurl' style='display:none' id='%s'>%s </div>
                           <div class='url' style='display:none'></div>
                           <div class='' style=''>
                              <div class='nodename float_left' style='font-weight:bold;width:15em;background-color2:grey'>%s</div>                                                         
                              <div class='status float_left' style='width:4em'></div>
                              <div class='numspecies float_left' style='width:4em'> %s</div>
                              <div class='nummols float_left' style='width:4em'> %s</div>
                              <div class='numstates float_left' style='width:4em'> %s</div>
                              <div class='numradtrans float_left' style='width:4em'> %s</div>
                              <div class='numcollisions float_left' style='width:4em'> %s</div>
                              <div class='numtrunc float_left' style='width:4em'> %s</div>
                           </div>
                           <div class='species' style='clear:both'></div> 
                      </li>""" % (node["name"],u'98%',node["name"], node["url"],node["name"],"0","0","0","0","0","0")

    response += "</ul></div>"
    return response, nodes


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
        vamdccounts = [] #[('error', 'no response')]
        return vamdccounts
        
    if res.status == 200:
        vamdccounts = [item for item in res.getheaders() if item[0][0:5]=='vamdc']
        content = [item for item in res.getheaders() if item[0][0:7]=='content']
    elif res.status == 204:
        vamdccounts = [ ("vamdc-count-species",0),
                        ("vamdc-count-states",0),
                        ("vamdc-truncated",0),
                        ("vamdc-count-molecules",0),
                        ("vamdc-count-sources",0),
                        ("vamdc-approx-size",0),
                        ("vamdc-count-radiative",0),
                        ("vamdc-count-atoms",0)]
    else:
        vamdccounts =  [("vamdc-count-species",0),
                        ("vamdc-count-states",0),
                        ("vamdc-truncated",0),
                        ("vamdc-count-molecules",0),
                        ("vamdc-count-sources",0),
                        ("vamdc-approx-size",0),
                        ("vamdc-count-radiative",0),
                        ("vamdc-count-atoms",0)]

    return vamdccounts
    
def getNodeStatistic(baseurl, inchikey, url = None):
    """
    Queries the VAMDC databases via the given baseurl and the inchikey.
    Via a HEAD request statistics is obtained from the result

    Returns: VAMDC statistic as htmlcode (for ajax Requests)
    """

    orig_url = url
    
    url=url.replace('rad3d','XSAMS')
    url=url.replace('png','XSAMS')
    url=url.replace('xspcat','XSAMS')
    url=url.replace('comfort','XSAMS')
    url=url.replace('spcat','XSAMS')
    url=url.replace('mrg','XSAMS')
    
    if not url:
        query = "sync?REQUEST=doQuery&LANG=VSS1&FORMAT=XSAMS&QUERY=SELECT+All+WHERE++InchiKey='%s'" % inchikey
        url = baseurl.rstrip()+query
        orig_url=url
    try:
        vamdccounts = doHeadRequest(url)
    except:
        vamdccounts = []
        
    vc = {}
    vc['url']=orig_url
    
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

    chkbox = "<input type='checkbox' class='idselector'>"

    html = "<table class='full'><tbody>"
    data = []
    try:
        for m in xml.xpath(xp ,namespaces=prefixmap):
            try:
                speciesid = m.xpath('@speciesID', namespaces=prefixmap)[0]
                try:
                    stoichiometricformula = m.xpath('./xsams:MolecularChemicalSpecies/xsams:StoichiometricFormula', namespaces=prefixmap)[0].text
                except:
                    stoichiometricformula = ""
                try:
                    chemicalname = m.xpath('./xsams:MolecularChemicalSpecies/xsams:ChemicalName/xsams:Value', namespaces=prefixmap)[0].text
                except:
                    chemicalname = ""
                try:
                    structuralformula = m.xpath('./xsams:MolecularChemicalSpecies/xsams:OrdinaryStructuralFormula/xsams:Value', namespaces=prefixmap)[0].text
                except:
                    structuralformula = ""
                try:
                    inchikey = m.xpath('./xsams:MolecularChemicalSpecies/xsams:InChIKey', namespaces=prefixmap)[0].text
                except:
                    inchikey = ""
                try:
                    comment = m.xpath('./xsams:MolecularChemicalSpecies/xsams:Comment', namespaces=prefixmap)[0].text
                except:
                    comment = ""
            
                response += "%s %s %s %s \n" % (structuralformula, stoichiometricformula, chemicalname, comment)
                html += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> \n" % (chkbox, speciesid, structuralformula, stoichiometricformula, chemicalname, comment)
                data.append({'speciesid':speciesid,
                             'stoichiometricformula':stoichiometricformula,
                             'chemicalname':chemicalname,
                             'structuralformula':structuralformula,
                             'inchikey':inchikey,
                             'comment':comment,
                             'url':url,})
            except Exception, e:
                print >> sys.stderr, "ERROR %s" % e #pass
    except:
        return "ERROR 2"

    html += "</tbody></table>"
    return  html, data
