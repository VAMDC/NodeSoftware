# -*- coding: utf-8 -*-

# This is where you would add additional functionality to your node, 
# bound to certain URLs in urls.py
import sys
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from django.utils import simplejson

from django.conf import settings

from cdmsportalfunc import *


class QUERY(object):
    """
    """
#    baseurl = "http://cdms.ph1.uni-koeln.de:8090/DjCDMS/tap/sync?REQUEST=doQuery&LANG=VSS1&FORMAT=XSAMS&QUERY="
    baseurl = "http://cdms.ph1.uni-koeln.de/DjCDMSdev/tap/sync?REQUEST=doQuery&LANG=VSS2&FORMAT=XSAMS&QUERY="

    def __init__(self, data):
        self.isvalid = True
        self.errormsg = ''
        try:
            self.data = data # dict(data)
        except Exception,e:
            self.isvalid = False
            self.errormsg = 'Could not read argument dict: %s'%e

        if self.isvalid: self.validate()

    def validate(self):
        
        try: self.freqfrom = self.data.get('T_SEARCH_FREQ_FROM',0)
        except: self.freqfrom = 0
        try: self.freqto = self.data.get('T_SEARCH_FREQ_TO',0)
        except: self.freqto = 0
        try: self.minint = self.data.get('T_SEARCH_INT',-10)
        except: self.freqto = -10

        try: self.format = self.data.get('T_TYPE','XSAMS')
        except: self.format = 'XSAMS'

        try:
            self.query = self.data.get('QUERY',"").rstrip()
            self.url = self.baseurl + QueryDict(self.query).urlencode()
            
        except:
            self.query = ""
            self.url = None
        
        try:
            self.speciesIDs = self.data.getlist('speciesIDs')
        except:
            self.speciesIDs = []

        if self.format == 'spcat':
            self.url = self.url.replace('XSAMS','spcat').replace("ALL","RadiativeTransitions")

        # this is slightly different to spcat and uses correct qn labels
        if self.format == 'comfort':
            self.url = self.url.replace('XSAMS','xspcat').replace("ALL","RadiativeTransitions")

        if self.format == 'png':
            self.url = self.url.replace('XSAMS','png').replace("ALL","RadiativeTransitions")

        print >> sys.stderr, self.format
        print >> sys.stderr, self.url



def index(request):
    c=RequestContext(request,{})
#    return render_to_response('tap/index.html', c)
    return render_to_response('cdmsportal/home.html', c)


def contact(request):
    c=RequestContext(request,{})
    return render_to_response('cdmsportal/contact.html', c)
        
        
def queryPage(request):
    test = request.POST
    id_list = request.POST.getlist('speciesIDs')
    
    species_list = getSpeciesList(id_list)
    c=RequestContext(request,{"postvar" : test, "speciesid_list": id_list, "species_list" : species_list})
    return render_to_response('cdmsportal/queryForm.html', c)


def queryForm(request):
    """
    Create the species selection - page from the species (model) stored in the database
    """
    species_list = getSpeciesList()
    c=RequestContext(request,{"action" : "queryPage", "species_list" : species_list})
    return render_to_response('cdmsportal/querySpecies.html', c)

def selectSpecie(request):
    """
    Create the species selection - page from the species (model) stored in the database
    """
    species_list = getSpeciesList()
    c=RequestContext(request,{"action" : "catalog", "species_list" : species_list})
    return render_to_response('cdmsportal/selectSpecies.html', c)

def catalog(request):
    """
    Creates the documentation page for a specie
    """

    # get the species id from posted values
    id = request.POST.get("T_EID",0)

    # query specie from database
    specie = getSpecie(id)
    
    # query sources from database
    sources = getSources4specie(id)

    # query datasets from database
    datasets = getDatasets4specie(id)

    # query parameters from database
    rotationalConstants = getParameters4specie(id, "Rotational Constant")
    dipoleMoments = getParameters4specie(id, "Dipole Moment")
    partitionFunctions = getParameters4specie(id, "Partition function")
    otherParameters = getParameters4specie(id, "Other")
    
    # query files from database
    files = getFiles4specie(id)
        
    c=RequestContext(request,{"specie" : specie,
                              "sources" : sources,
                              "datasets" : datasets,
                              "files" : files,
                              "rotationalconstants" : rotationalConstants,
                              "dipolemoments" : dipoleMoments,
                              "partitionfunctions" : partitionFunctions,
                              "otherparameters" : otherParameters  })
    
    return render_to_response('cdmsportal/showDocumentation.html', c)


def showResults(request):
    """
    """

    postvars = QUERY(request.POST)

    if postvars.url:
        if  postvars.format=='xsams':
            result = applyStylesheet(postvars.url, xsl = None)
        elif  postvars.format=='rad3d':
            result = "<pre>" + str(applyStylesheet(postvars.url, xsl = "/var/www/vamdcdev/nodes/cdms/static/xsl/convertXSAMS2Rad3d.xslt")) + "</pre>"
        elif postvars.format=='png':
            result = "<img class='full' width='100%' src="+postvars.url+" alt='Stick Spectrum'>"
        else:
            result = "<pre>" + geturl(postvars.url) + "</pre>"
    else:
        result = "<p> Invalid request </p>"
    
    c=RequestContext(request,{"postvars": postvars, "result" : result})
    return render_to_response('cdmsportal/showResults.html', c)



def ajaxRequest(request):
    """
    """
    postvars = request.POST
    response_dict = {}
    if 'function' in request.POST:

        if request.POST['function'] == 'checkQuery':
            QUERY, htmlcode = checkQuery(request.POST)
            response_dict.update({'QUERY' : QUERY, 'htmlcode' : htmlcode, 'message' : " Tach "})
        elif request.POST['function'] == 'getVAMDCstats':
            htmlcode = getHtmlNodeList()
            response_dict.update({'htmlcode' : htmlcode, 'message' : " Statistics "})
        elif request.POST['function'] == 'getNodeStatistic':
            # get url of the node which should have been posted
            nodeurl = request.POST.get('nodeurl',"")
            inchikey = request.POST.get('inchikey',"")

            # fetch statistic for this node
            if nodeurl:
                htmlcode = getNodeStatistic(nodeurl, inchikey)
            else:
                htmlcode = ""
            
            response_dict.update({'htmlcode' : htmlcode, 'message' : " Statistics "})
        else:
            response_dict.update({'QUERY' : QUERY, 'htmlcode' : "<p> HALLO </p>", 'message' : " Tach "})
    else:
        response_dict.update({'QUERY' : "", 'htmlcode' : "Error: No function name posted! ", 'message' : "Error: No function name posted! "})
       
    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')



from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.forms import Form,FileField,URLField,TextInput
from django.core.exceptions import ValidationError

from lxml import etree as e
#xsl=e.XSLT(e.parse(open('/home/endres/Projects/vamdc/nodes/cdms/node/convertXSAMS2html.xslt')))
xsl=e.XSLT(e.parse(open(settings.BASE_PATH + '/nodes/cdms/static/xsl/convertXSAMS2html.xslt')))

from urllib2 import urlopen

class ConversionForm(Form):
    infile = FileField(label='Input file',required=False)
    inurl = URLField(label='Input URL',required=False,widget=TextInput(attrs={'size': 50, 'title': 'Paste here a URL that delivers an XSAMS document.',}))

    def clean(self):
        infile = self.cleaned_data.get('infile')
        inurl = self.cleaned_data.get('inurl')
        if (infile and inurl):
            raise ValidationError('Give either input file or URL!')

        if inurl:
            try: data = urlopen(inurl)
            except Exception,err:
                raise ValidationError('Could not open given URL: %s'%err)
        elif infile: data = infile
        else:
            raise ValidationError('Give either input file or URL!')

        try: xml=e.parse(data)
        except Exception,err:
            raise ValidationError('Could not parse XML file: %s'%err)
        try: self.cleaned_data['sme'] = xsl(xml)
        except Exception,err:
            raise ValidationError('Could not transform XML file: %s'%err)

        return self.cleaned_data

def xsams2html(request):
    if request.method != 'POST':
        ConvForm = ConversionForm()
    else:
        ConvForm = ConversionForm(request.POST, request.FILES)
        if ConvForm.is_valid():
            response=HttpResponse(ConvForm.cleaned_data['sme'],mimetype='text/csv')
            response['Content-Disposition'] = \
                'attachment; filename=%s.sme'% (ConvForm.cleaned_data.get('infile') or 'output')
            return response

    return render_to_response('cdmsportal/xsams2sme.html',
            RequestContext(request,dict(conversion=ConvForm)))
