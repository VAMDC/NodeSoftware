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
from forms import *

#from django.views.decorators.csrf import csrf_protect
#@csrf_protect

class QUERY(object ):
    """
    """
#    baseurl = "http://cdms.ph1.uni-koeln.de:8090/DjCDMS/tap/sync?REQUEST=doQuery&LANG=VSS1&FORMAT=XSAMS&QUERY="
     #sync?REQUEST=doQuery&LANG=VSS2&FORMAT=XSAMS&QUERY="
    requeststring = "sync?REQUEST=doQuery&LANG=VSS2&FORMAT=XSAMS&QUERY="

    def __init__(self, data, baseurl = "http://cdms.ph1.uni-koeln.de/DjJPLdev/tap/", qformat = None):
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

        try: self.database = self.data.get('database','jpl')
        except: self.database='jpl'
        
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
                self.url = self.baseurl + self.requeststring + QueryDict(self.query).urlencode()
            
            except:
                self.query = ""
                self.url = None

        if len(self.orderby)>0 and 'ORDERBY' not in self.url:
            self.url += '&ORDERBY=%s' % self.orderby
            
        try:
            self.speciesIDs = self.data.getlist('speciesIDs')
        except:
            self.speciesIDs = []

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

def general(request):
    c=RequestContext(request,{})
    return render_to_response('cdmsportal/general.html', c)

def help(request):
    c=RequestContext(request,{})
    return render_to_response('cdmsportal/help.html', c)

        
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

def tools(request):
    """
    """
    print >> sys.stderr, request.method
    if request.method == 'POST':
        form = XsamsConversionForm(request.POST, request.FILES)
        if form.is_valid():
            
            print >> sys.stderr, "IS VALID"
            response=HttpResponse(form.cleaned_data['result'],mimetype='text/csv')
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
    species_list = getSpeciesList()
    c=RequestContext(request,{"action" : "catalog", "species_list" : species_list})
    return render_to_response('cdmsportal/selectSpecies.html', c)

def catalog(request, id=None):
    """
    Creates the documentation page for a specie
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


def showResultsOld(request):
    """
    """

    postvars = QUERY(request.POST)

    if postvars.url:
        if  postvars.format=='xsams':
            try:
                result = applyStylesheet(postvars.url, xsl = settings.BASE_PATH + '/nodes/cdms/static/xsl/convertXSAMS2html.xslt')
            except Exception,err:
                result = err
        elif  postvars.format=='rad3d':
            result = "<pre>" + str(applyStylesheet(postvars.url, xsl = settings.BASE_PATH + "/nodes/cdms/static/xsl/convertXSAMS2Rad3d.xslt")) + "</pre>"
        elif postvars.format=='png':
            result = "<img class='full' width='100%' src="+postvars.url+" alt='Stick Spectrum'>"
        else:
            result = "<pre>" + geturl(postvars.url) + "</pre>"
    else:
        result = "<p> Invalid request </p>"

    try:
        c=RequestContext(request,{"postvars": postvars, "result" : result})
    except UnicodeError, e:
        c=RequestContext(request,{"postvars": postvars, "result" : result.decode('utf-8')})
        return render_to_response('cdmsportal/showResults.html', c)

    except Exception, err:
        c=RequestContext(request,{"postvars": postvars, "result" : err})

    try:
        return render_to_response('cdmsportal/showResults.html', c)
    except UnicodeError, e:
        c=RequestContext(request,{"postvars": postvars, "result" : result.decode('utf-8')})
        return render_to_response('cdmsportal/showResults.html', c)
    except Exception, err:
        c=RequestContext(request,{"postvars": postvars, "result" : err})
        return render_to_response('cdmsportal/showResults.html', c)




def showResults(request):
    """
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
            QUERYs, htmlcode = checkQuery(request.POST)
            response_dict.update({'QUERY' : QUERYs, 'htmlcode' : htmlcode, 'message' : " Tach "})
        elif request.POST['function'] == 'getVAMDCstats':
            htmlcode = getHtmlNodeList()
            response_dict.update({'htmlcode' : htmlcode, 'message' : " Statistics "})
        elif request.POST['function'] == 'ajaxQuery':
            ##### TEST TEST TEST TEST ###########
            # get result and return it via ajax
            #print >> sys.stderr, "url = " +request.POST['url']
            # just apply the stylesheet if a complete url has been posted

            baseurl = request.POST.get('nodeurl','http://cdms.ph1.uni-koeln.de/DjJPLdev/tap/')
            
            if 'url2' in request.POST:
                htmlcode = str(applyStylesheet(request.POST['url2'], xsl = settings.BASE_PATH + '/nodes/cdms/static/xsl/convertXSAMS2html.xslt'))
            else:    
                postvars = QUERY(request.POST,baseurl = baseurl)
                print >> sys.stderr, "postvars.url = " +postvars.url
                if postvars.url:
                    if  postvars.format.lower()=='xsams':
                        htmlcode = str(applyStylesheet(postvars.url, xsl = settings.BASE_PATH + '/nodes/jpl/static/xsl/convertXSAMS2html.xslt'))
                    elif  postvars.format=='rad3d':
                        htmlcode = "<pre>" + str(applyStylesheet(postvars.url, xsl = settings.BASE_PATH + "/nodes/jpl/static/xsl/convertXSAMS2Rad3d.xslt")) + "</pre>"
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
            #postvars.url=postvars.url.replace('png','XSAMS').replace('spcat','XSAMS').replace('rad3d','XSAMS').replace('xspcat','XSAMS')

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
                result =  getspecies(url)
            except:
                result = "<p> Invalid request </p>"
        
            response_dict.update({'htmlcode' : result, 'message' : " Species ",})
        else:
            response_dict.update({'QUERY' : QUERYs, 'htmlcode' : "<p> HALLO </p>", 'message' : " Tach "})
    else:
        response_dict.update({'QUERY' : "", 'htmlcode' : "Error: No function name posted! ", 'message' : "Error: No function name posted! "})
       
    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')


def specieslist(request):
    """
    Create the species selection - page for the admin-site from the species (model) stored in the database
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/DjJPL/cdms/login/?next=%s' % request.path)

    species_list = getSpeciesList()
    c=RequestContext(request,{"action" : "catalog", "species_list" : species_list})
    return render_to_response('cdmsadmin/selectSpecies.html', c)


def queryspecies(request, baseurl = "http://cdms.ph1.uni-koeln.de/DjJPLdev/tap/"):
    
    requeststring = "sync?REQUEST=doQuery&LANG=VSS2&FORMAT=XSAMS&QUERY=SELECT+SPECIES"
    url = baseurl + requeststring
    
    try:
        #result = "<pre>" + getspecies(url) + "</pre>"
        result =  getspecies(url)
    except:
        result = "<p> Invalid request </p>"
    
    c=RequestContext(request,{"result" : result})
    return render_to_response('cdmsportal/showResults.html', c)

        
def molecule(request):

    if request.method == 'GET':
        try:
            molecule = Molecules.objects.get(pk=request.GET.get("id",0))
            form = MoleculeForm(instance=molecule)
        except Molecules.DoesNotExist:
            form = MoleculeForm()
            
    elif request.method == 'POST':
        molecule = Molecules.objects.get(pk=request.POST.get("id",0))        
        form = MoleculeForm(request.POST,instance=molecule)
        if form.is_valid():
            form.save()
        
    else:
        form = MoleculeForm()

    return render_to_response('cdmsadmin/molecules.html', {
        'form': form,
        })


def specie(request,id=None):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/DjJPLdev/cdms/login/?next=%s' % request.path)
    
    specie=None
    if id: #request.method == 'GET':
        try:
            specie = Species.objects.get(pk=id)
            form = SpecieForm(instance=specie)
        except Species.DoesNotExist:
            form = SpecieForm()
            
    elif request.method == 'POST':
        specie = Species.objects.get(pk=request.POST.get("id",0))        
        form = SpecieForm(request.POST,instance=specie)
        if form.is_valid():
            form.save()
        
    else:
        form = SpecieForm()

    if specie and specie.id:
        datasets = Datasets.objects.filter(specie = specie.id)
        files = Files.objects.filter(specie = specie.id)
        atoms = AtomArray.objects.filter(specie = specie.id)
        bonds = BondArray.objects.filter(specie = specie.id)
        referenceids = SourcesIDRefs.objects.filter(specie = specie.id).values('referenceid')
        references = Sources.objects.filter(pk__in=referenceids)
        filters = QuantumNumbersFilter.objects.filter(specie = specie.id)

        # query parameters from database
        rotationalConstants = Parameter.objects.filter(specie = specie.id, type = "Rotational Constant").order_by('parameter')
        dipoleMoments = Parameter.objects.filter(specie = specie.id, type =  "Dipole Moment").order_by('parameter')
        partitionFunctions = Parameter.objects.filter(specie = specie.id, type =  "Partition function").order_by('parameter')
        otherParameters = Parameter.objects.filter(specie = specie.id, type =  "Other").order_by('parameter')

    else:
        datasets = None
        files = None
        atoms = None
        bonds = None
        references = None
        filters = None
        rotationalConstants = None
        dipoleMoments = None
        partitionFunctions = None
        otherParameters = None
        
    return render_to_response('cdmsadmin/species.html', {
        'form': form,
        'dataset_list': datasets,
        'file_list': files,
        'atom_list': atoms,
        'bond_list': bonds,
        'reference_list': references,
        'filter_list': filters,
        'rotconstant_list': rotationalConstants,
        'dipolemoment_list': dipoleMoments,
        'otherparameter_list': otherParameters,
        'partitionfunction_list': partitionFunctions,
        })


def filters(request,id = None):
    FilterFormSet = modelformset_factory(QuantumNumbersFilter, form=FilterForm, can_delete=True, extra=1)

    if id: #request.method == 'GET':
        #specieid = request.GET.get("specieid",0)
        
        try:
            #filters = QuantumNumbersFilter.objects.filter(species=specieid)
            filters = QuantumNumbersFilter.objects.filter(specie=id)
            formset = FilterFormSet(queryset = filters)
        except Species.DoesNotExist:
            formset = FilterFormSet()
            
    elif request.method == 'POST':
        formset = FilterFormSet(request.POST, request.FILES)
        if formset.is_valid():
            # do something with the formset.cleaned_data
            pass
    else:
        formset = FilterFormSet()
    return render_to_response('cdmsadmin/filters.html', {'formset': formset})



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
