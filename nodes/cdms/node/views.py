# -*- coding: utf-8 -*-

# This is where you would add additional functionality to your node, 
# bound to certain URLs in urls.py
import sys
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
import json as simplejson

from django.conf import settings

from cdmsportalfunc import *
from forms import *
import os
from django.views.decorators.cache import cache_page
#from django.views.decorators.csrf import csrf_protect
#@csrf_protect

FILENAME_XSAMS2HTML = settings.XSLT_DIR + 'convertXSAMS2html.xslt'
FILENAME_XSAMS2RAD3D = settings.XSLT_DIR + 'convertXSAMS2Rad3d.xslt'
FILENAME_MERGERADEX = settings.XSLT_DIR + 'speciesmergerRadex_1.0_v0.3.xslt'


class QUERY(object ):
    """
    """
#    baseurl = "http://cdms.ph1.uni-koeln.de:8090/DjCDMS/tap/sync?REQUEST=doQuery&LANG=VSS1&FORMAT=XSAMS&QUERY="
     #sync?REQUEST=doQuery&LANG=VSS2&FORMAT=XSAMS&QUERY="
    requeststring = "sync?REQUEST=doQuery&LANG=VSS2&FORMAT=XSAMS&"

    def __init__(self, data, baseurl = settings.BASE_URL+settings.TAP_URLPATH, qformat = None):
        self.isvalid = True
        self.errormsg = ''
        self.baseurl = baseurl.rstrip()  # remove white spaces from the right side
        self.format = qformat
        
        try:
            self.data = data # dict(data)
        except Exception,e:
            self.isvalid = False
            self.errormsg = 'Could not read argument dict: %s'%e

        if self.isvalid: self.validate()

    def validate(self):

        try: self.database = self.data.get('database','cdms')
        except: self.database='cdms'
        
        try: self.freqfrom = self.data.get('T_SEARCH_FREQ_FROM',0)
        except: self.freqfrom = 0
        try: self.freqto = self.data.get('T_SEARCH_FREQ_TO',0)
        except: self.freqto = 0
        try: self.minint = self.data.get('T_SEARCH_INT',-10)
        except: self.freqto = -10

        try: self.orderby = self.data.get('T_SORT','')
        except: self.orderby = ''

        try: self.explines = self.data.get('T_SHOWEXPLINES','merge')
        except: self.explines = 'merge'

        if not self.format:
            try: self.format = self.data.get('T_TYPE','XSAMS')
            except: self.format = 'XSAMS'

        try: self.url = self.data.get('queryURL','')
        except: self.url = ''

        print >> sys.stderr, "queryURL = " + self.url
        
        if len(self.url)==0:
            try:
                self.query = self.data.get('QUERY',"").rstrip()
            except:
                self.query = ""
            if self.query.strip() == 'SELECT ALL WHERE':
                self.query = 'SELECT SPECIES'
            try:
                self.url = self.baseurl + self.requeststring + QueryDict("QUERY="+self.query).urlencode()
            except:
                self.url = None

            print >> sys.stderr, "query = " + self.query
            print >> sys.stderr, "url = " + self.url

        if len(self.orderby)>0 and 'ORDERBY' not in self.url:
            self.url += '&ORDERBY=%s' % self.orderby

        # speciesID identifies only CDMS/JPL species
        try:
            self.speciesIDs = self.data.getlist('speciesIDs')
        except:
            self.speciesIDs = []

        # inchikey is used to identify isotopologs
        try:
            self.inchikey = self.data.getlist('inchikey')
        except:
            self.inchikey = []

        # Molecules are currently identified via StoichiometricFormula 
        try:
            self.molecule = self.data.getlist('molecule')
        except:
            self.molecule = []

        if self.format == 'spcat':
            if self.explines == 'merge':
                self.url = self.url.replace('XSAMS','mrg').replace("ALL","RadiativeTransitions")
            else:
                self.url = self.url.replace('XSAMS','spcat').replace("ALL","RadiativeTransitions")

        # this is slightly different to spcat and uses correct qn labels
        if self.format == 'comfort':
            self.url = self.url.replace('XSAMS','xspcat').replace("ALL","RadiativeTransitions")

        if self.format == 'png':
            self.url = self.url.replace('XSAMS','png').replace("ALL","RadiativeTransitions")

        # used only for radex:
        if self.format == 'rad3d':
            self.spec_url=self.data.get('spec_url','')
            self.spec_speciesid = self.data.get('spec_speciesid','')
            self.col_url = self.data.get('col_url','')
            self.col_speciesid = self.data.get('col_speciesid','')

#        print >> sys.stderr, self.query
        print >> sys.stderr, self.format
        print >> sys.stderr, self.url
        print >> sys.stderr, self.database


def index(request):
    c=RequestContext(request,{})
#    return render_to_response('tap/index.html', c)
    return render_to_response('cdmsportal/home.html', c)


def contact(request):
    c=RequestContext(request,{})
    return render_to_response('cdmsportal/contact.html', c)

@cache_page(60 * 15)
def general(request):
    c=RequestContext(request,{})
    return render_to_response('cdmsportal/general.html', c)

def help(request):
    c=RequestContext(request,{})
    return render_to_response('cdmsportal/help.html', c)

        
def queryPage(request):
    """
    Creates the Form to define query parameters;
    Species are already defined and should be posted to this page
    """
    postvars = request.POST
    id_list = request.POST.getlist('speciesIDs')
    inchikey_list = request.POST.getlist('inchikey')
    stoichio_list = request.POST.getlist('molecule')
    
    species_list = get_species_list(id_list, database = -5)
    isotopolog_list = Species.objects.filter(inchikey__in=inchikey_list)
    molecule_list = Species.objects.filter(molecule__stoichiometricformula__in=stoichio_list)
            
    c=RequestContext(request,{"postvar" : postvars,
                              "speciesid_list": id_list,
                              "inchikey_list" : inchikey_list,
                              "stoichio_list": stoichio_list,
                              "species_list" : species_list,
                              "isotopolog_list" : isotopolog_list,
                              "molecule_list" : molecule_list,
                              })
    
    return render_to_response('cdmsportal/queryForm.html', c)


def query_form(request):
    """
    Create the species selection - page from the species (model) stored in the database
    """
    #species_list = get_species_list()

    id_list = request.POST.getlist('speciesIDs')
    inchikey_list = request.POST.getlist('inchikey')
    stoichio_list = request.POST.getlist('molecule')
    c=RequestContext(request,{"action" : "queryPage",
                              "speciesid_list": id_list,
                              "inchikey_list" : inchikey_list,
                              "stoichio_list": stoichio_list,
                              })
    return render_to_response('cdmsportal/querySpeciesAjax.html', c)


def tools(request):
    """
    """
    print >> sys.stderr, request.method
    if request.method == 'POST':
        form = XsamsConversionForm(request.POST, request.FILES)
        if form.is_valid():
            
            print >> sys.stderr, "IS VALID"
            response=HttpResponse(form.cleaned_data['result'],content_type='text/csv')
            response['Content-Disposition'] = \
                'attachment; filename=%s.%s'% (form.cleaned_data.get('infile') or 'output', form.cleaned_data.get('format') )
            return response
        else:
            print >> sys.stderr, "IS NOT VALID"

    else:
        form = XsamsConversionForm()

    #return render_to_response('upload.html', {'form': form})

    
    c=RequestContext(request,{'form':form})
    return render_to_response('cdmsportal/tools.html', c)


def selectSpecie(request):
    """
    Create the species selection - page from the species (model) stored in the database
    """
    species_list = get_species_list()
    c=RequestContext(request,{"action" : "catalog", "species_list" : species_list})
#    return render_to_response('cdmsportal/selectSpeciesAjax.html', c)
    return render_to_response('cdmsportal/selectSpecies.html', c)

def selectSpecie2(request):
    """
    Create the species selection - page from the species (model) stored in the database
    """
    #species_list = get_species_list()
    c=RequestContext(request,{"action" : "catalog"})
    return render_to_response('cdmsportal/selectSpeciesAjax.html', c)



def html_list(request, content='species'):
    """
    Renders species, molecules, or isotopologs as html_list,
    which can be included into webpages via ajax request.

    content: string ('species' - default, 'molecules', 'isotopologs'
             which specifies which information will be returned.

    Returns html_string 
    """
    if content == 'molecules':
        molecules_list = get_molecules_list()
        c=RequestContext(request,{"action" : "catalog",
                                  "species_list" : [],
                                  "molecules_list" : molecules_list,
                                  "isotopolog_list" : [],})
        
        return render_to_response('cdmsportal/species_table.html', c)

    elif content == 'isotopologs':
        isotopolog_list = get_isotopologs_list()
        c=RequestContext(request,{"action" : "catalog",
                                  "species_list" : [],
                                  "molecules_list" : [],
                                  "isotopolog_list" : isotopolog_list,})

        return render_to_response('cdmsportal/species_table.html', c)

    else:
        species_list = get_species_list()
        c=RequestContext(request,{"action" : "catalog",
                                  "species_list" : species_list,
                                  "molecules_list" : [],
                                  "isotopolog_list" : [],})
    
    return render_to_response('cdmsportal/species_table.html', c)

@cache_page(60*15)
def json_list(request, content='species'):
    """
    Creates a list of species available in the database.
    if field database is posted, the list is restricted to species with
    origin == database

    database: corresponds to origin - field in db (0:jpl, 5:cdms, <0: all)

    returns type(<json>) list of species with species data.
    """
    try:
        db = int(request.POST.get('database',5))
    except ValueError:
        db = 5
    
    response_dict={}
    species_list=[]
    for specie in get_species_list(database = db):
        try:
            s = {'id':specie.id,
                 'molecule':specie.molecule.id,
                 'structuralformula':specie.molecule.structuralformula,
                 'stoichiometricformula':specie.molecule.stoichiometricformula,
                 'moleculesymbol':specie.molecule.symbol,
                 #'atom':specie.atom,             
                 'speciestag':specie.speciestag,
                 'name':specie.name,
                 'trivialname':specie.molecule.trivialname,
                 'isotopolog':specie.isotopolog,
                 'state':specie.state,
                 'state_html':specie.state_html(),
                 'inchikey':specie.inchikey,
                 'contributor':specie.contributor,
                 'version':specie.version,
                 'dateofentry':str(specie.dateofentry),
                 }
        except:
            pass
        species_list.append(s)
    response_dict.update({'species' : species_list,'database' : db})
       
    return HttpResponse(simplejson.dumps(response_dict), content_type='application/json')


def catalog(request, id=None):
    """
    Creates the documentation page for a specie

    id: Database id of the specie
    """

    if id == None:
        # get the species id from posted values
        id = request.POST.get("T_EID",0)
        # if nothing has been posted, get the first specie by tag-number
        if id == 0:
            specie = Species.objects.all().order_by('speciestag')[0]
            id = specie.id

    # query specie from database
    specie = getSpecie(id)
    
    # query sources from database
    sources = getSources4specie(id)

    # query datasets from database
    datasets = getDatasets4specie(id)

    # query parameters from database
    rotationalConstants = getParameters4specie(id, "Rotational Constant")
    dipoleMoments = getParameters4specie(id, "Dipole Moment")
    #partitionFunctions = getParameters4specie(id, "Partition function")
    otherParameters = getParameters4specie(id, "Other")

    pfhtml = getPartitionf4specie(id)
    nuclear_spin_isomers = NuclearSpinIsomers.objects.filter(specie=id)
    for nsi in nuclear_spin_isomers:
        pfhtml += "<br><br>" + getPartitionf4specie(id,nsi=nsi)
            
    # query files from database
    files = getFiles4specie(id)
        
    c=RequestContext(request,{"specie" : specie,
                              "sources" : sources,
                              "datasets" : datasets,
                              "files" : files,
                              "rotationalconstants" : rotationalConstants,
                              "dipolemoments" : dipoleMoments,
                              "pfhtml" : pfhtml,
                              "otherparameters" : otherParameters  })
    
    return render_to_response('cdmsportal/showDocumentation.html', c)




def showResults(request):
    """
    Returns the 'Result' - page. The result itself is retrieved via ajax request.
    """

    postvars = QUERY(request.POST)

    result=""
    if postvars.database == 'vamdc':
        readyfunc='ajaxGetNodeList();ajaxQueryNodeContent();'
    else:
        readyfunc='ajaxQueryNodeContent();'
    
    try:
        c=RequestContext(request,{"postvars": postvars, "result" : result, "readyfunc":readyfunc})
    except UnicodeError, e:
        c=RequestContext(request,{"postvars": postvars, "result" : result.decode('utf-8')})
        return render_to_response('cdmsportal/showResults2.html', c)

    except Exception, err:
        c=RequestContext(request,{"postvars": postvars, "result" : err})

    try:
        return render_to_response('cdmsportal/showResults2.html', c)
    except UnicodeError, e:
        c=RequestContext(request,{"postvars": postvars, "result" : result.decode('utf-8')})
        return render_to_response('cdmsportal/showResults2.html', c)
    except Exception, err:
        c=RequestContext(request,{"postvars": postvars, "result" : err})
        return render_to_response('cdmsportal/showResults2.html', c)



def ajaxRequest(request):
    """
    """
    postvars = request.POST
    response_dict = {}
    if 'function' in request.POST:

        if request.POST['function'] == 'checkQuery':
            QUERYs, htmlcode = check_query(request.POST)
            response_dict.update({'QUERY' : QUERYs, 'htmlcode' : htmlcode, 'message' : " Tach "})
        elif request.POST['function'] == 'getVAMDCstats':
            htmlcode, nodes = getHtmlNodeList()            
            response_dict.update({'htmlcode' : htmlcode, 'nodes': nodes, 'message' : " Statistics "})
        elif request.POST['function'] == 'ajaxQuery':
            ##### TEST TEST TEST TEST ###########
            # get result and return it via ajax
            #print >> sys.stderr, "url = " +request.POST['url']
            # just apply the stylesheet if a complete url has been posted

            baseurl = request.POST.get('nodeurl', settings.BASE_URL + settings.TAP_URLPATH)
            
            if 'url2' in request.POST:
                htmlcode = str(applyStylesheet(request.POST['url2'],
                                               xsl = FILENAME_XSAMS2HTML))
            else:    
                postvars = QUERY(request.POST,baseurl = baseurl)
                print >> sys.stderr, "postvars.url = " +postvars.url
                if postvars.url:
                    if  postvars.format.lower()=='xsams':
                        htmlcode = str(applyStylesheet(postvars.url,
                                                       xsl = FILENAME_XSAMS2HTML))
                    elif  postvars.format=='rad3dx':
                        htmlcode = "<pre>" + str(applyStylesheet(postvars.url,
                                                                 xsl = FILENAME_XSAMS2HTML)) + "</pre>"
                    elif postvars.format=='rad3d':
                        #ouput = str(applyRadex(postvars.url, xsl = FILENAME_MERGERADEX))
#                        url4="http://batz.lpma.jussieu.fr:8080/tapservice_11_12/TAP/sync?LANG=VSS2&REQUEST=doQuery&FORMAT=XSAMS&QUERY=select+*+where+%28reactant0.InchiKey+%3D+%27UGFAIRIUMAVXCW-UHFFFAOYSA-N%27%29"
                        url4="http://dev.vamdc.org/basecol/tapservice_12_07/TAP/sync?LANG=VSS2&REQUEST=doQuery&FORMAT=XSAMS&QUERY=select+*+where+%28reactant0.InchiKey+%3D+%27UGFAIRIUMAVXCW-UHFFFAOYSA-N%27%29"

                        print >> sys.stderr, "col: %s\nspec: %s\n" % (postvars.col_url, postvars.spec_url)
                        output = str(applyRadex(postvars.spec_url, species1=postvars.spec_speciesid, species2=postvars.col_speciesid, inurl2=postvars.col_url))
                        
                        htmlcode = "<pre>" + output + "</pre>"
                    elif postvars.format=='png':
                        htmlcode = "<img class='full' width='100%' src="+postvars.url+" alt='Stick Spectrum'>"
                    else:
                        htmlcode = "<pre>" + str(geturl(postvars.url)) + "</pre>"
                else:
                    htmlcode = "<p> Invalid request </p>"

            response_dict.update({'QUERY': "QUERY", 'htmlcode' : htmlcode, 'message' : " Statistics "})
            
        elif request.POST['function'] == 'getNodeStatistic':
            # get url of the node which should have been posted
            nodeurl = request.POST.get('nodeurl',"")
            inchikey = request.POST.get('inchikey',"")

    
            postvars = QUERY(request.POST, baseurl = nodeurl, qformat='XSAMS')

            print >> sys.stderr," NODESTATURL: "+ postvars.url
            # fetch statistic for this node
            if nodeurl:
                htmlcode, vc = getNodeStatistic(nodeurl, inchikey, url = postvars.url)
            else:
                htmlcode = ""
                vc={}

            try:
                numspecies = vc['vamdccountspecies']
            except:
                numspecies = '0'
            
            response_dict.update({'htmlcode' : htmlcode, 'message' : " Statistics ",})
            response_dict.update(vc)
        elif request.POST['function'] == 'queryspecies':
            nodeurl = request.POST.get('nodeurl',"")
            inchikey = request.POST.get('inchikey',"")
            
            postvars = QUERY(request.POST, baseurl = nodeurl, qformat='XSAMS')
            
            url = postvars.url.replace('ALL','SPECIES').replace('RadiativeTransitions','SPECIES')
            url=url.replace('rad3d','XSAMS')
            url=url.replace('xspcat','XSAMS')
            url=url.replace('spcat','XSAMS')
            url=url.replace('mrg','XSAMS')
            url=url.replace('png','XSAMS')
            url=url.replace('comfort','XSAMS')
            print >> sys.stderr, "SPECQUERY: "+url
            try:
                result, speciesdata =  getspecies(url)
            except:
                result, speciesdata = "<p> Invalid request </p>", []
        
            response_dict.update({'htmlcode' : result, 'speciesdata': speciesdata, 'message' : " Species ",})
        else:
            response_dict.update({'QUERY' : QUERYs, 'htmlcode' : "<p> HALLO </p>", 'message' : " Tach "})
    else:
        response_dict.update({'QUERY' : "",
                              'htmlcode' : "Error: No function name posted! ",
                              'message' : "Error: No function name posted! "})
       
    return HttpResponse(simplejson.dumps(response_dict), content_type='application/json')


def specieslist(request):
    """
    Create the species selection - page for the admin-site from the species (model) stored in the database
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect(settings.BASE_URL+settings.PORTAL_URLPATH +'login/?next=%s' % request.path)

    species_list = get_species_list()
    c=RequestContext(request,{"action" : "catalog", "species_list" : species_list})
    return render_to_response('cdmsadmin/selectSpecies.html', c)


def queryspecies(request, baseurl = settings.BASE_URL + settings.TAP_URLPATH):
    
    requeststring = "sync?REQUEST=doQuery&LANG=VSS2&FORMAT=XSAMS&QUERY=SELECT+SPECIES"
    url = baseurl + requeststring
    
    try:
        #result = "<pre>" + getspecies(url) + "</pre>"
        result =  getspecies(url)
    except:
        result = "<p> Invalid request </p>"
    
    c=RequestContext(request,{"result" : result})
    return render_to_response('cdmsportal/showResults.html', c)

        
def getfile(request,id):
    """
    reads the content from an ascii-file from the database
    and returns the file

    id: Database id of the file
    """
    f = Files.objects.get(pk=id)
    response=HttpResponse(f.asciifile,content_type='text/txt')
    
    response['Content-Disposition'] = 'attachment; filename=%s'%(f.name)

    return response


def download_data(request):
    postvars = request.POST

    baseurl = request.POST.get('nodeurl', settings.BASE_URL + settings.TAP_URLPATH)
            
    if 'url2' in request.POST:
        return HttpResponseRedirect(request.POST['url2'])
    else:    
        postvars = QUERY(request.POST,baseurl = baseurl)
        if postvars.url:
            if  postvars.format.lower()=='xsams':
                return HttpResponseRedirect(postvars.url)

def cdms_lite_download(request):
    """
    Returns the cdms_lite (sqlite3) database file
    """
#    data = open(os.path.join(settings.PROJECT_PATH,'/var/cdms/v1_0/NodeSoftware/nodes/cdms/cdms_lite_notrans.db.gz'),'r').read()
#    return HttpResponseRedirect(settings.BASE_URL+settings.PORTAL_URLPATH +'login/?next=%s' % request.path)
    return HttpResponseRedirect(settings.BASE_URL+'/static/cdms/cdms_lite.db.gz')

